# SPDX-FileCopyrightText: Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0

from datetime import datetime
from typing import Literal
from uuid import UUID

from os2mo_helpers import mora_helpers
from requests import Response

from calculate_primary.config import Settings
from calculate_primary.model import ClassDict
from calculate_primary.model import EngagementDict
from calculate_primary.model import EngagementEditPayload

# TODO(#70977): right now this is just a wrapper around the real MoraHelper,
#   the next commits will replace this with a GraphQL-based implementation


class MoraHelper:
    _mora_helper: mora_helpers.MoraHelper

    def __init__(self, settings: Settings):
        self._mora_helper = mora_helpers.MoraHelper(
            hostname=settings.fastramqpi.mo_url,
            auth_server=settings.fastramqpi.auth_server,
            client_id=settings.fastramqpi.client_id,
            client_secret=settings.fastramqpi.client_secret.get_secret_value(),
            auth_realm=settings.fastramqpi.auth_realm,
            use_cache=False,
        )

    async def read_user_engagements(
        self,
        user: UUID | str,
        at: datetime,
        only_primary: Literal[True],
        use_cache: Literal[False],
    ) -> list[EngagementDict]:
        assert only_primary, "`only_primary=False` is not supported by this shim"
        assert not use_cache, "`use_cache=True` is not supported by this shim"

        return self._mora_helper.read_user_engagements(
            user,
            at=at,
            only_primary=only_primary,
            use_cache=use_cache,
        )

    async def find_cut_dates(
        self, uuid: str, no_past: Literal[False] = False
    ) -> list[datetime]:
        assert not no_past, "`no_past=True` is not supported by this shim"

        return self._mora_helper.find_cut_dates(uuid, no_past=no_past)

    async def _mo_post(
        self, url: Literal["details/edit"], payload: EngagementEditPayload
    ) -> Response:
        assert url == "details/edit", f"`url={url}` is not supported by this shim"
        assert (
            payload["type"] == "engagement"
        ), "editing types other than `engagement` is not supported by this shim"

        return self._mora_helper._mo_post(url, payload)

    async def read_classes_in_facet(self, facet: str) -> tuple[list[ClassDict], str]:
        return self._mora_helper.read_classes_in_facet(facet)
