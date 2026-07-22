from typing import List
from typing import Optional
from uuid import UUID

from .base_model import BaseModel


class TestingGetEngagement(BaseModel):
    engagements: "TestingGetEngagementEngagements"


class TestingGetEngagementEngagements(BaseModel):
    objects: List["TestingGetEngagementEngagementsObjects"]


class TestingGetEngagementEngagementsObjects(BaseModel):
    validities: List["TestingGetEngagementEngagementsObjectsValidities"]


class TestingGetEngagementEngagementsObjectsValidities(BaseModel):
    primary_response: Optional[
        "TestingGetEngagementEngagementsObjectsValiditiesPrimaryResponse"
    ]
    fraction: Optional[int]


class TestingGetEngagementEngagementsObjectsValiditiesPrimaryResponse(BaseModel):
    validities: List[
        "TestingGetEngagementEngagementsObjectsValiditiesPrimaryResponseValidities"
    ]


class TestingGetEngagementEngagementsObjectsValiditiesPrimaryResponseValidities(
    BaseModel
):
    uuid: UUID


TestingGetEngagement.update_forward_refs()
TestingGetEngagementEngagements.update_forward_refs()
TestingGetEngagementEngagementsObjects.update_forward_refs()
TestingGetEngagementEngagementsObjectsValidities.update_forward_refs()
TestingGetEngagementEngagementsObjectsValiditiesPrimaryResponse.update_forward_refs()
TestingGetEngagementEngagementsObjectsValiditiesPrimaryResponseValidities.update_forward_refs()
