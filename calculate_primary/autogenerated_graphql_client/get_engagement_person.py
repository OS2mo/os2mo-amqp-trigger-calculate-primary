from typing import List
from uuid import UUID

from .base_model import BaseModel


class GetEngagementPerson(BaseModel):
    engagements: "GetEngagementPersonEngagements"


class GetEngagementPersonEngagements(BaseModel):
    objects: List["GetEngagementPersonEngagementsObjects"]


class GetEngagementPersonEngagementsObjects(BaseModel):
    validities: List["GetEngagementPersonEngagementsObjectsValidities"]


class GetEngagementPersonEngagementsObjectsValidities(BaseModel):
    person: List["GetEngagementPersonEngagementsObjectsValiditiesPerson"]


class GetEngagementPersonEngagementsObjectsValiditiesPerson(BaseModel):
    uuid: UUID


GetEngagementPerson.update_forward_refs()
GetEngagementPersonEngagements.update_forward_refs()
GetEngagementPersonEngagementsObjects.update_forward_refs()
GetEngagementPersonEngagementsObjectsValidities.update_forward_refs()
GetEngagementPersonEngagementsObjectsValiditiesPerson.update_forward_refs()
