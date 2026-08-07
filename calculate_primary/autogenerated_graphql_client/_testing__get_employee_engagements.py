from datetime import datetime
from typing import List
from typing import Optional
from uuid import UUID

from pydantic import Field

from .base_model import BaseModel


class TestingGetEmployeeEngagements(BaseModel):
    engagements: "TestingGetEmployeeEngagementsEngagements"


class TestingGetEmployeeEngagementsEngagements(BaseModel):
    objects: List["TestingGetEmployeeEngagementsEngagementsObjects"]


class TestingGetEmployeeEngagementsEngagementsObjects(BaseModel):
    validities: List["TestingGetEmployeeEngagementsEngagementsObjectsValidities"]


class TestingGetEmployeeEngagementsEngagementsObjectsValidities(BaseModel):
    uuid: UUID
    validity: "TestingGetEmployeeEngagementsEngagementsObjectsValiditiesValidity"
    primary_response: Optional[
        "TestingGetEmployeeEngagementsEngagementsObjectsValiditiesPrimaryResponse"
    ]


class TestingGetEmployeeEngagementsEngagementsObjectsValiditiesValidity(BaseModel):
    from_: datetime = Field(alias="from")
    to: Optional[datetime]


class TestingGetEmployeeEngagementsEngagementsObjectsValiditiesPrimaryResponse(
    BaseModel
):
    validities: List[
        "TestingGetEmployeeEngagementsEngagementsObjectsValiditiesPrimaryResponseValidities"
    ]


class TestingGetEmployeeEngagementsEngagementsObjectsValiditiesPrimaryResponseValidities(
    BaseModel
):
    uuid: UUID


TestingGetEmployeeEngagements.update_forward_refs()
TestingGetEmployeeEngagementsEngagements.update_forward_refs()
TestingGetEmployeeEngagementsEngagementsObjects.update_forward_refs()
TestingGetEmployeeEngagementsEngagementsObjectsValidities.update_forward_refs()
TestingGetEmployeeEngagementsEngagementsObjectsValiditiesValidity.update_forward_refs()
TestingGetEmployeeEngagementsEngagementsObjectsValiditiesPrimaryResponse.update_forward_refs()
TestingGetEmployeeEngagementsEngagementsObjectsValiditiesPrimaryResponseValidities.update_forward_refs()
