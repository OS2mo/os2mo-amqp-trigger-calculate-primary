from datetime import datetime
from uuid import UUID

from ._testing__create_class import TestingCreateClass
from ._testing__create_class import TestingCreateClassClassCreate
from ._testing__create_employee import TestingCreateEmployee
from ._testing__create_employee import TestingCreateEmployeeEmployeeCreate
from ._testing__create_engagement import TestingCreateEngagement
from ._testing__create_engagement import TestingCreateEngagementEngagementCreate
from ._testing__create_facet import TestingCreateFacet
from ._testing__create_facet import TestingCreateFacetFacetCreate
from ._testing__create_org_unit import TestingCreateOrgUnit
from ._testing__create_org_unit import TestingCreateOrgUnitOrgUnitCreate
from ._testing__get_employee_engagements import TestingGetEmployeeEngagements
from ._testing__get_employee_engagements import TestingGetEmployeeEngagementsEngagements
from ._testing__get_engagement import TestingGetEngagement
from ._testing__get_engagement import TestingGetEngagementEngagements
from ._testing__get_facet_by_user_key import TestingGetFacetByUserKey
from ._testing__get_facet_by_user_key import TestingGetFacetByUserKeyFacets
from ._testing__update_engagement import TestingUpdateEngagement
from ._testing__update_engagement import TestingUpdateEngagementEngagementUpdate
from .async_base_client import AsyncBaseClient
from .get_employee_engagements import GetEmployeeEngagements
from .get_employee_engagements import GetEmployeeEngagementsEngagements
from .get_employee_engagements_at import GetEmployeeEngagementsAt
from .get_employee_engagements_at import GetEmployeeEngagementsAtEngagements
from .get_engagement_person import GetEngagementPerson
from .get_engagement_person import GetEngagementPersonEngagements
from .get_facet_classes_by_user_key import GetFacetClassesByUserKey
from .input_types import ClassCreateInput
from .input_types import EmployeeCreateInput
from .input_types import EngagementCreateInput
from .input_types import EngagementUpdateInput
from .input_types import FacetCreateInput
from .input_types import OrganisationUnitCreateInput
from .update_engagement import UpdateEngagement
from .update_engagement import UpdateEngagementEngagementUpdate


def gql(q: str) -> str:
    return q


class GraphQLClient(AsyncBaseClient):
    async def get_engagement_person(self, uuid: UUID) -> GetEngagementPersonEngagements:
        query = gql(
            """
            query GetEngagementPerson($uuid: UUID!) {
              engagements(filter: {uuids: [$uuid], from_date: null, to_date: null}) {
                objects {
                  validities(start: null, end: null) {
                    person {
                      uuid
                    }
                  }
                }
              }
            }
            """
        )
        variables: dict[str, object] = {"uuid": uuid}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetEngagementPerson.parse_obj(data).engagements

    async def get_employee_engagements_at(
        self, uuid: UUID, at: datetime
    ) -> GetEmployeeEngagementsAtEngagements:
        query = gql(
            """
            query GetEmployeeEngagementsAt($uuid: UUID!, $at: DateTime!) {
              engagements(
                filter: {employee: {uuids: [$uuid]}, from_date: null, to_date: null}
              ) {
                objects {
                  current(at: $at) {
                    uuid
                    user_key
                    fraction
                    engagement_type_response {
                      current(at: $at) {
                        uuid
                      }
                    }
                    primary_response {
                      current(at: $at) {
                        uuid
                      }
                    }
                    validity {
                      from
                      to
                    }
                  }
                }
              }
            }
            """
        )
        variables: dict[str, object] = {"uuid": uuid, "at": at}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetEmployeeEngagementsAt.parse_obj(data).engagements

    async def get_employee_engagements(
        self, uuid: UUID
    ) -> GetEmployeeEngagementsEngagements:
        query = gql(
            """
            query GetEmployeeEngagements($uuid: UUID!) {
              engagements(
                filter: {employee: {uuids: [$uuid]}, from_date: null, to_date: null}
              ) {
                objects {
                  validities(start: null, end: null) {
                    uuid
                    validity {
                      from
                      to
                    }
                    primary_response {
                      validities(start: null, end: null) {
                        uuid
                      }
                    }
                  }
                }
              }
            }
            """
        )
        variables: dict[str, object] = {"uuid": uuid}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetEmployeeEngagements.parse_obj(data).engagements

    async def get_facet_classes_by_user_key(
        self, user_key: str
    ) -> GetFacetClassesByUserKey:
        query = gql(
            """
            query GetFacetClassesByUserKey($user_key: String!) {
              classes(
                filter: {facet: {user_keys: [$user_key]}, from_date: null, to_date: null}
              ) {
                objects {
                  validities {
                    user_key
                    uuid
                  }
                }
              }
              facets(filter: {user_keys: [$user_key], from_date: null, to_date: null}) {
                objects {
                  validities {
                    uuid
                  }
                }
              }
            }
            """
        )
        variables: dict[str, object] = {"user_key": user_key}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return GetFacetClassesByUserKey.parse_obj(data)

    async def update_engagement(
        self, input: EngagementUpdateInput
    ) -> UpdateEngagementEngagementUpdate:
        query = gql(
            """
            mutation UpdateEngagement($input: EngagementUpdateInput!) {
              engagement_update(input: $input) {
                uuid
              }
            }
            """
        )
        variables: dict[str, object] = {"input": input}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return UpdateEngagement.parse_obj(data).engagement_update

    async def _testing__get_engagement(
        self, uuid: UUID
    ) -> TestingGetEngagementEngagements:
        query = gql(
            """
            query _Testing_GetEngagement($uuid: UUID!) {
              engagements(filter: {uuids: [$uuid], from_date: null, to_date: null}) {
                objects {
                  validities(start: null, end: null) {
                    primary_response {
                      validities(start: null, end: null) {
                        uuid
                      }
                    }
                    fraction
                  }
                }
              }
            }
            """
        )
        variables: dict[str, object] = {"uuid": uuid}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return TestingGetEngagement.parse_obj(data).engagements

    async def _testing__get_employee_engagements(
        self, uuid: UUID
    ) -> TestingGetEmployeeEngagementsEngagements:
        query = gql(
            """
            query _Testing_GetEmployeeEngagements($uuid: UUID!) {
              engagements(
                filter: {employee: {uuids: [$uuid]}, from_date: null, to_date: null}
              ) {
                objects {
                  validities(start: null, end: null) {
                    uuid
                    validity {
                      from
                      to
                    }
                    primary_response {
                      validities(start: null, end: null) {
                        uuid
                      }
                    }
                  }
                }
              }
            }
            """
        )
        variables: dict[str, object] = {"uuid": uuid}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return TestingGetEmployeeEngagements.parse_obj(data).engagements

    async def _testing__get_facet_by_user_key(
        self, user_key: str
    ) -> TestingGetFacetByUserKeyFacets:
        query = gql(
            """
            query _Testing_GetFacetByUserKey($user_key: String!) {
              facets(filter: {user_keys: [$user_key], from_date: null, to_date: null}) {
                objects {
                  validities {
                    uuid
                  }
                }
              }
            }
            """
        )
        variables: dict[str, object] = {"user_key": user_key}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return TestingGetFacetByUserKey.parse_obj(data).facets

    async def _testing__create_employee(
        self, input: EmployeeCreateInput
    ) -> TestingCreateEmployeeEmployeeCreate:
        query = gql(
            """
            mutation _Testing_CreateEmployee($input: EmployeeCreateInput!) {
              employee_create(input: $input) {
                uuid
              }
            }
            """
        )
        variables: dict[str, object] = {"input": input}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return TestingCreateEmployee.parse_obj(data).employee_create

    async def _testing__create_engagement(
        self, input: EngagementCreateInput
    ) -> TestingCreateEngagementEngagementCreate:
        query = gql(
            """
            mutation _Testing_CreateEngagement($input: EngagementCreateInput!) {
              engagement_create(input: $input) {
                uuid
              }
            }
            """
        )
        variables: dict[str, object] = {"input": input}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return TestingCreateEngagement.parse_obj(data).engagement_create

    async def _testing__create_org_unit(
        self, input: OrganisationUnitCreateInput
    ) -> TestingCreateOrgUnitOrgUnitCreate:
        query = gql(
            """
            mutation _Testing_CreateOrgUnit($input: OrganisationUnitCreateInput!) {
              org_unit_create(input: $input) {
                uuid
              }
            }
            """
        )
        variables: dict[str, object] = {"input": input}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return TestingCreateOrgUnit.parse_obj(data).org_unit_create

    async def _testing__update_engagement(
        self, input: EngagementUpdateInput
    ) -> TestingUpdateEngagementEngagementUpdate:
        query = gql(
            """
            mutation _Testing_UpdateEngagement($input: EngagementUpdateInput!) {
              engagement_update(input: $input) {
                uuid
              }
            }
            """
        )
        variables: dict[str, object] = {"input": input}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return TestingUpdateEngagement.parse_obj(data).engagement_update

    async def _testing__create_facet(
        self, input: FacetCreateInput
    ) -> TestingCreateFacetFacetCreate:
        query = gql(
            """
            mutation _Testing_CreateFacet($input: FacetCreateInput!) {
              facet_create(input: $input) {
                uuid
              }
            }
            """
        )
        variables: dict[str, object] = {"input": input}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return TestingCreateFacet.parse_obj(data).facet_create

    async def _testing__create_class(
        self, input: ClassCreateInput
    ) -> TestingCreateClassClassCreate:
        query = gql(
            """
            mutation _Testing_CreateClass($input: ClassCreateInput!) {
              class_create(input: $input) {
                uuid
              }
            }
            """
        )
        variables: dict[str, object] = {"input": input}
        response = await self.execute(query=query, variables=variables)
        data = self.get_data(response)
        return TestingCreateClass.parse_obj(data).class_create
