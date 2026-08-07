from datetime import datetime
from typing import List
from typing import Optional
from uuid import UUID

from pydantic import Field

from .base_model import BaseModel


class GetEmployeeEngagements(BaseModel):
    engagements: "GetEmployeeEngagementsEngagements"


class GetEmployeeEngagementsEngagements(BaseModel):
    objects: List["GetEmployeeEngagementsEngagementsObjects"]


class GetEmployeeEngagementsEngagementsObjects(BaseModel):
    validities: List["GetEmployeeEngagementsEngagementsObjectsValidities"]


class GetEmployeeEngagementsEngagementsObjectsValidities(BaseModel):
    uuid: UUID
    validity: "GetEmployeeEngagementsEngagementsObjectsValiditiesValidity"
    primary_response: Optional[
        "GetEmployeeEngagementsEngagementsObjectsValiditiesPrimaryResponse"
    ]


class GetEmployeeEngagementsEngagementsObjectsValiditiesValidity(BaseModel):
    from_: datetime = Field(alias="from")
    to: Optional[datetime]


class GetEmployeeEngagementsEngagementsObjectsValiditiesPrimaryResponse(BaseModel):
    validities: List[
        "GetEmployeeEngagementsEngagementsObjectsValiditiesPrimaryResponseValidities"
    ]


class GetEmployeeEngagementsEngagementsObjectsValiditiesPrimaryResponseValidities(
    BaseModel
):
    uuid: UUID


GetEmployeeEngagements.update_forward_refs()
GetEmployeeEngagementsEngagements.update_forward_refs()
GetEmployeeEngagementsEngagementsObjects.update_forward_refs()
GetEmployeeEngagementsEngagementsObjectsValidities.update_forward_refs()
GetEmployeeEngagementsEngagementsObjectsValiditiesValidity.update_forward_refs()
GetEmployeeEngagementsEngagementsObjectsValiditiesPrimaryResponse.update_forward_refs()
GetEmployeeEngagementsEngagementsObjectsValiditiesPrimaryResponseValidities.update_forward_refs()
