# SPDX-FileCopyrightText: Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from typing import Literal
from typing import TypedDict


class EngagementPrimaryDict(TypedDict):
    uuid: str


class EngagementTypeDict(TypedDict):
    uuid: str


# because of `from` being a reserved keyword, we must use this syntax
ValidityDict = TypedDict("ValidityDict", {"from": str, "to": str | None})


class EngagementDict(TypedDict):
    uuid: str
    user_key: str
    fraction: int | None
    engagement_type: EngagementTypeDict
    primary: EngagementPrimaryDict | None
    validity: ValidityDict


class EngagementEditPayloadData(TypedDict):
    primary: EngagementPrimaryDict
    validity: ValidityDict


class EngagementEditPayload(TypedDict):
    type: Literal["engagement"]
    uuid: str
    data: EngagementEditPayloadData


class ClassDict(TypedDict):
    uuid: str
    user_key: str
