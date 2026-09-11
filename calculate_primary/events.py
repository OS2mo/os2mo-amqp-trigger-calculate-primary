# SPDX-FileCopyrightText: Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
import asyncio
from uuid import UUID

import structlog
from fastapi import APIRouter
from fastramqpi.events import Event
from more_itertools import only

from calculate_primary import depends
from calculate_primary.main import calculate_user

router = APIRouter()

logger = structlog.stdlib.get_logger()


@router.post("/events/mo/engagement")
async def calculate_engagement(
    event: Event[UUID],
    mo: depends.GraphQLClient,
    updater: depends.Updater,
    settings: depends.Settings,
) -> None:
    engagement_uuid = event.subject

    await asyncio.sleep(settings.delay_event)
    logger.info(
        "Processing event for engagement",
        engagement_uuid=engagement_uuid,
        delay=settings.delay_event,
    )

    result = await mo.get_engagement_person(engagement_uuid)
    result_obj = only(result.objects)
    if result_obj is None:
        logger.info("No related person found.", engagement_uuid=engagement_uuid)
        return
    uuids = {e.uuid for o in result_obj.validities for e in o.person}

    logger.info("Found related person(s)", person_uuids=uuids)
    # An engagement can be associated with multiple employees across its lifespan, although it typically isn't done.
    for person_uuid in uuids:
        await calculate_user(updater, person_uuid)
