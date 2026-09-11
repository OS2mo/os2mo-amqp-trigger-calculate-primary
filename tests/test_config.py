# SPDX-FileCopyrightText: Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
"""Tests for the settings in `calculate_primary.config`."""

import pytest

from calculate_primary.config import Settings


def test_delay_event_default(load_settings_overrides: dict[str, str]) -> None:
    """`delay_event` falls back to its own default when neither is set."""
    settings = Settings()
    assert settings.delay_event == 10
    assert settings.delay_amqp is None


@pytest.mark.envvar({"DELAY_AMQP": "42"})
def test_delay_amqp_sets_delay_event(load_settings_overrides: dict[str, str]) -> None:
    """The deprecated `delay_amqp` is honoured when `delay_event` is unset."""
    settings = Settings()
    assert settings.delay_event == 42


@pytest.mark.envvar({"DELAY_AMQP": "42", "DELAY_EVENT": "7"})
def test_delay_event_takes_precedence(
    load_settings_overrides: dict[str, str],
) -> None:
    """`delay_event` wins when both are set."""
    settings = Settings()
    assert settings.delay_event == 7
