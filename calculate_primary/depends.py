# SPDX-FileCopyrightText: Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from typing import Annotated

from fastapi import Depends
from fastramqpi.ramqp.depends import from_context
from fastramqpi.depends import from_user_context

from calculate_primary.common import MOPrimaryEngagementUpdater
from calculate_primary.config import _Settings
from calculate_primary.autogenerated_graphql_client import GraphQLClient as _GraphQLClient


GraphQLClient = Annotated[_GraphQLClient, Depends(from_context("graphql_client"))]
Settings = Annotated[_Settings, Depends(from_user_context("settings"))]
Updater = Annotated[MOPrimaryEngagementUpdater, Depends(from_user_context("updater"))]
