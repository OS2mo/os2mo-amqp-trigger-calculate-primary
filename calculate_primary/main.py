# SPDX-FileCopyrightText: 2019-2020 Magenta ApS
#
# SPDX-License-Identifier: MPL-2.0
"""Event-driven recalculate primary program."""

from contextlib import asynccontextmanager
from typing import cast
from uuid import UUID

from fastramqpi.main import FastRAMQPI
from prometheus_client import Counter
from prometheus_client import Gauge

from calculate_primary.common import MOPrimaryEngagementUpdater
from calculate_primary.common import get_engagement_updater
from calculate_primary.config import Settings
from calculate_primary.depends import GraphQLClient
from calculate_primary.mora_helper_shim import MoraHelper

edit_counter = Counter("recalculate_edit", "Number of edits made")
no_edit_counter = Counter("recalculate_no_edit", "Number of noops made")
last_processing = Gauge(
    "recalculate_last_processing", "Timestamp of the last processing"
)


async def calculate_user(updater: MOPrimaryEngagementUpdater, uuid: UUID) -> None:
    """Recalculate the user given by uuid.

    Called for the side-effect of making calls against MO using the updater.

    Args:
        updater: The calculate primary updater instance.
        uuid: UUID for the user to recalculate.

    Returns:
        None
    """
    print(f"Recalculating user: {uuid}")
    last_processing.set_to_current_time()
    updates = await updater.recalculate_user(uuid)
    # Update edit metrics
    for number_of_edits in updates.values():
        if number_of_edits == 0:
            no_edit_counter.inc()
        edit_counter.inc(number_of_edits)


@asynccontextmanager
async def setup_updater(settings: Settings, fastramqpi: FastRAMQPI):
    """
    Instantiates the correct updater implementation, based on what is configured
    in `settings.integration`.
    """

    context = fastramqpi.get_context()
    assert "graphql_client" in context
    gql_client = cast(GraphQLClient, context["graphql_client"])

    print(f"Acquiring updater: {settings.integration}")
    updater_class = get_engagement_updater(settings.integration)
    print(f"Got class: {updater_class}")
    mora_helper = MoraHelper(gql_client)
    updater: MOPrimaryEngagementUpdater = await updater_class.create(
        settings, mora_helper
    )
    print(f"Got object: {updater}")
    fastramqpi.add_context(updater=updater)

    yield
