from datetime import datetime
from typing import List
from typing import Optional
from uuid import UUID

from pydantic import Field

from .base_model import BaseModel


class GetEmployeeEngagementsAt(BaseModel):
    engagements: "GetEmployeeEngagementsAtEngagements"


class GetEmployeeEngagementsAtEngagements(BaseModel):
    objects: List["GetEmployeeEngagementsAtEngagementsObjects"]


class GetEmployeeEngagementsAtEngagementsObjects(BaseModel):
    current: Optional["GetEmployeeEngagementsAtEngagementsObjectsCurrent"]


class GetEmployeeEngagementsAtEngagementsObjectsCurrent(BaseModel):
    uuid: UUID
    user_key: str
    fraction: Optional[int]
    engagement_type_response: (
        "GetEmployeeEngagementsAtEngagementsObjectsCurrentEngagementTypeResponse"
    )
    primary_response: Optional[
        "GetEmployeeEngagementsAtEngagementsObjectsCurrentPrimaryResponse"
    ]
    validity: "GetEmployeeEngagementsAtEngagementsObjectsCurrentValidity"


class GetEmployeeEngagementsAtEngagementsObjectsCurrentEngagementTypeResponse(
    BaseModel
):
    current: Optional[
        "GetEmployeeEngagementsAtEngagementsObjectsCurrentEngagementTypeResponseCurrent"
    ]


class GetEmployeeEngagementsAtEngagementsObjectsCurrentEngagementTypeResponseCurrent(
    BaseModel
):
    uuid: UUID


class GetEmployeeEngagementsAtEngagementsObjectsCurrentPrimaryResponse(BaseModel):
    current: Optional[
        "GetEmployeeEngagementsAtEngagementsObjectsCurrentPrimaryResponseCurrent"
    ]


class GetEmployeeEngagementsAtEngagementsObjectsCurrentPrimaryResponseCurrent(
    BaseModel
):
    uuid: UUID


class GetEmployeeEngagementsAtEngagementsObjectsCurrentValidity(BaseModel):
    from_: datetime = Field(alias="from")
    to: Optional[datetime]


GetEmployeeEngagementsAt.update_forward_refs()
GetEmployeeEngagementsAtEngagements.update_forward_refs()
GetEmployeeEngagementsAtEngagementsObjects.update_forward_refs()
GetEmployeeEngagementsAtEngagementsObjectsCurrent.update_forward_refs()
GetEmployeeEngagementsAtEngagementsObjectsCurrentEngagementTypeResponse.update_forward_refs()
GetEmployeeEngagementsAtEngagementsObjectsCurrentEngagementTypeResponseCurrent.update_forward_refs()
GetEmployeeEngagementsAtEngagementsObjectsCurrentPrimaryResponse.update_forward_refs()
GetEmployeeEngagementsAtEngagementsObjectsCurrentPrimaryResponseCurrent.update_forward_refs()
GetEmployeeEngagementsAtEngagementsObjectsCurrentValidity.update_forward_refs()
