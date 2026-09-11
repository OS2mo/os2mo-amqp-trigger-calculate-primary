# SPDX-FileCopyrightText: Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0

from fastapi import FastAPI
from fastramqpi.events import GraphQLEvents
from fastramqpi.events import Listener
from fastramqpi.main import FastRAMQPI

from calculate_primary import events
from calculate_primary.config import Settings
from calculate_primary.depends import GraphQLClient
from calculate_primary.main import setup_updater


def create_app() -> FastAPI:
    settings = Settings()
    fastramqpi = FastRAMQPI(
        application_name="calculate_primary",
        settings=settings.fastramqpi,
        graphql_version=22,
        graphql_client_cls=GraphQLClient,
        graphql_events=GraphQLEvents(
            declare_listeners=[
                Listener(
                    namespace="mo",
                    user_key="calculate_primary",
                    routing_key="engagement",
                    path="/events/mo/engagement",
                    parallelism=1,
                )
            ]
        ),
    )

    # The event fetchers are started at priority 1000, and immediately begin
    # calling the event handlers, which depend on the updater. Therefore the
    # updater must be set up before them.
    fastramqpi.add_lifespan_manager(setup_updater(settings, fastramqpi), priority=500)
    fastramqpi.add_context(settings=settings)

    app = fastramqpi.get_app()
    app.include_router(events.router)

    return app
