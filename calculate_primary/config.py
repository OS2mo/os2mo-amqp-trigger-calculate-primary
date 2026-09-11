# SPDX-FileCopyrightText: Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0

from typing import Any
from typing import Literal
from uuid import UUID

import structlog
from fastramqpi.config import Settings as FastRAMQPISettings
from pydantic import BaseSettings
from pydantic import PositiveInt
from pydantic import root_validator

logger = structlog.stdlib.get_logger()


class Settings(BaseSettings):
    class Config:
        frozen = True
        env_nested_delimiter = "__"

    fastramqpi: FastRAMQPISettings

    integration: Literal["DEFAULT", "OPUS", "SD"]
    dry_run: bool = False
    eng_types_primary_order: list[UUID] = []

    # Wait delay_event seconds before processing events to help avoid race conditions
    # between integrations (see motivation on https://redmine.magenta.dk/issues/61815)
    delay_event: PositiveInt = 10

    # Deprecated name for delay_event, from back when events were delivered over
    # AMQP. Kept so existing deployments do not silently fall back to the
    # default when they upgrade.
    delay_amqp: PositiveInt | None = None

    @root_validator(pre=True)
    def delay_amqp_is_deprecated(cls, values: dict[str, Any]) -> dict[str, Any]:
        """Let the deprecated `delay_amqp` set `delay_event` when it is unset."""
        delay_amqp = values.get("delay_amqp")
        if delay_amqp is None:
            return values
        logger.warning(
            "delay_amqp is deprecated, use delay_event instead",
            delay_amqp=delay_amqp,
        )
        if values.get("delay_event") is None:
            values["delay_event"] = delay_amqp
        return values
