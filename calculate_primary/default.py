# SPDX-FileCopyrightText: Magenta ApS
#
# SPDX-License-Identifier: MPL-2.0
from typing import Any
from typing import Self

import structlog

from calculate_primary.common import MOPrimaryEngagementUpdater
from calculate_primary.model import ClassDict
from calculate_primary.model import EngagementDict

logger = structlog.stdlib.get_logger()


class DefaultPrimaryEngagementUpdater(MOPrimaryEngagementUpdater):
    @classmethod
    async def create(cls, *args, **kwargs) -> Self:
        this = await super().create(*args, **kwargs)

        this.check_filters = []
        this.calculate_filters = []

        return this

    async def _find_primary_types(self):
        """
        Read the engagement types from MO and match them up against the three
        known types in the OPUS->MO import.
        :param helper: An instance of mora-helpers.
        :return: A dict matching up the engagement types with LoRa class uuids.
        """
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
            list[ClassDict], Any
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
        primary_list = [primary_dict["fixed_primary"], primary_dict["primary"]]

        return primary_dict, primary_list

    def _find_primary(self, mo_engagements: list[EngagementDict]):
        if not mo_engagements:
            return None

        # The primary engagement is the engagement with the highest occupation rate.
        # - The occupation rate is found as 'fraction' on the engagement.
        #
        # If two engagements have the same occupation rate, the tie is broken by
        # picking by user-key.
        primary_engagement = max(
            mo_engagements,
            # Sort first by fraction, then reversely by user_key integer
            key=lambda eng: (eng.get("fraction") or 0, eng["user_key"]),
        )
        return primary_engagement["uuid"]
