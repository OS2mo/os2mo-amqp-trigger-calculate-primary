from typing import List
from uuid import UUID

from .base_model import BaseModel


class TestingGetFacetByUserKey(BaseModel):
    facets: "TestingGetFacetByUserKeyFacets"


class TestingGetFacetByUserKeyFacets(BaseModel):
    objects: List["TestingGetFacetByUserKeyFacetsObjects"]


class TestingGetFacetByUserKeyFacetsObjects(BaseModel):
    validities: List["TestingGetFacetByUserKeyFacetsObjectsValidities"]


class TestingGetFacetByUserKeyFacetsObjectsValidities(BaseModel):
    uuid: UUID


TestingGetFacetByUserKey.update_forward_refs()
TestingGetFacetByUserKeyFacets.update_forward_refs()
TestingGetFacetByUserKeyFacetsObjects.update_forward_refs()
TestingGetFacetByUserKeyFacetsObjectsValidities.update_forward_refs()
