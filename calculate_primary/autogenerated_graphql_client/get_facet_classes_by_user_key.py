from typing import List
from uuid import UUID

from .base_model import BaseModel


class GetFacetClassesByUserKey(BaseModel):
    classes: "GetFacetClassesByUserKeyClasses"
    facets: "GetFacetClassesByUserKeyFacets"


class GetFacetClassesByUserKeyClasses(BaseModel):
    objects: List["GetFacetClassesByUserKeyClassesObjects"]


class GetFacetClassesByUserKeyClassesObjects(BaseModel):
    validities: List["GetFacetClassesByUserKeyClassesObjectsValidities"]


class GetFacetClassesByUserKeyClassesObjectsValidities(BaseModel):
    user_key: str
    uuid: UUID


class GetFacetClassesByUserKeyFacets(BaseModel):
    objects: List["GetFacetClassesByUserKeyFacetsObjects"]


class GetFacetClassesByUserKeyFacetsObjects(BaseModel):
    validities: List["GetFacetClassesByUserKeyFacetsObjectsValidities"]


class GetFacetClassesByUserKeyFacetsObjectsValidities(BaseModel):
    uuid: UUID


GetFacetClassesByUserKey.update_forward_refs()
GetFacetClassesByUserKeyClasses.update_forward_refs()
GetFacetClassesByUserKeyClassesObjects.update_forward_refs()
GetFacetClassesByUserKeyClassesObjectsValidities.update_forward_refs()
GetFacetClassesByUserKeyFacets.update_forward_refs()
GetFacetClassesByUserKeyFacetsObjects.update_forward_refs()
GetFacetClassesByUserKeyFacetsObjectsValidities.update_forward_refs()
