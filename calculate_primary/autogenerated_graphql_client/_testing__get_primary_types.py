from typing import List
from uuid import UUID

from .base_model import BaseModel


class TestingGetPrimaryTypes(BaseModel):
    classes: "TestingGetPrimaryTypesClasses"


class TestingGetPrimaryTypesClasses(BaseModel):
    objects: List["TestingGetPrimaryTypesClassesObjects"]


class TestingGetPrimaryTypesClassesObjects(BaseModel):
    validities: List["TestingGetPrimaryTypesClassesObjectsValidities"]


class TestingGetPrimaryTypesClassesObjectsValidities(BaseModel):
    uuid: UUID
    user_key: str


TestingGetPrimaryTypes.update_forward_refs()
TestingGetPrimaryTypesClasses.update_forward_refs()
TestingGetPrimaryTypesClassesObjects.update_forward_refs()
TestingGetPrimaryTypesClassesObjectsValidities.update_forward_refs()
