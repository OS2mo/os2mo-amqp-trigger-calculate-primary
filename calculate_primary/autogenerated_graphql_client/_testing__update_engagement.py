from uuid import UUID

from .base_model import BaseModel


class TestingUpdateEngagement(BaseModel):
    engagement_update: "TestingUpdateEngagementEngagementUpdate"


class TestingUpdateEngagementEngagementUpdate(BaseModel):
    uuid: UUID


TestingUpdateEngagement.update_forward_refs()
TestingUpdateEngagementEngagementUpdate.update_forward_refs()
