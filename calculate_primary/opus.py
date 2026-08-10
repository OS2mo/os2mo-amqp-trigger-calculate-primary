# SPDX-FileCopyrightText: Magenta ApS
#
# SPDX-License-Identifier: MPL-2.0
import math
from typing import Self
from typing import cast

import structlog

from calculate_primary.common import MOPrimaryEngagementUpdater
from calculate_primary.config import Settings
from calculate_primary.model import ClassDict
from calculate_primary.model import EngagementDict
from calculate_primary.model import PrimaryClassesDict
from calculate_primary.mora_helper_shim import MoraHelper

logger = structlog.stdlib.get_logger()


class OPUSPrimaryEngagementUpdater(MOPrimaryEngagementUpdater):
    @classmethod
    async def create(cls, settings: Settings, mora_helper: MoraHelper) -> Self:
        this: Self = await super().create(settings, mora_helper)

        # Currently primary is set first by engagement type (order given in
        # settings) and secondly by job_id.
        # TODO: Check that configured eng_types exist

        def remove_missing_user_key(
            _user_uuid: str, engagement: EngagementDict
        ) -> bool:
            return "user_key" in engagement

        this.calculate_filters = [
            remove_missing_user_key,
        ]

        return this

    async def _find_primary_types(self) -> tuple[PrimaryClassesDict, list[str]]:
        """
        Read the engagement types from MO and match them up against the three
        known types in the OPUS->MO import.
        :param helper: An instance of mora-helpers.
        :return: A dict matching up the engagement types with LoRa class uuids.
        """
        # These constants are global in all OPUS municipalities (because they are
        # created by the OPUS->MO importer.
        PRIMARY = "primary"
        NON_PRIMARY = "non-primary"
        FIXED_PRIMARY = "explicitly-primary"

        logger.info("Read primary types")
        primary_dict: dict[str, str | None] = {
            "fixed_primary": None,
            "primary": None,
            "non_primary": None,
        }

        primary_types: tuple[
            list[ClassDict], str
        ] = await self.helper.read_classes_in_facet("primary_type")
        for primary_type in primary_types[0]:
            if primary_type["user_key"] == PRIMARY:
                primary_dict["primary"] = primary_type["uuid"]
            if primary_type["user_key"] == NON_PRIMARY:
                primary_dict["non_primary"] = primary_type["uuid"]
            if primary_type["user_key"] == FIXED_PRIMARY:
                primary_dict["fixed_primary"] = primary_type["uuid"]

        if None in primary_dict.values():
            raise Exception("Missing primary types: {}".format(primary_dict))
        primary_list = cast(
            list[str], [primary_dict["fixed_primary"], primary_dict["primary"]]
        )

        return cast(PrimaryClassesDict, primary_dict), primary_list

    def _find_primary(self, mo_engagements: list[EngagementDict]) -> str:
        # The primary engagement is the engagement with the lowest engagement type.
        # - The order of engagement types is given by self.settings.eng_types_primary_order.
        #
        # If two engagements have the same engagement_type, the tie is broken by
        # picking the one with the lowest user-key integer.
        def get_engagement_type_id(engagement: EngagementDict) -> float:
            if (
                engagement["engagement_type"]["uuid"]
                in self.settings.eng_types_primary_order
            ):
                return self.settings.eng_types_primary_order.index(
                    engagement["engagement_type"]["uuid"]  # type: ignore
                )
            return math.inf

        def get_engagement_order(engagement: EngagementDict) -> float:
            try:
                eng_id = int(engagement["user_key"])
                return eng_id
            except Exception as exp:
                logger.warning(
                    "Skippning engangement with non-integer employment_id: {}".format(
                        engagement["user_key"]
                    )
                )
                logger.exception(str(exp))
                return math.inf

        primary_engagement = min(
            mo_engagements,
            # Sort first by engagement_type, then by user_key integer
            key=lambda eng: (get_engagement_type_id(eng), get_engagement_order(eng)),
        )
        return primary_engagement["uuid"]
