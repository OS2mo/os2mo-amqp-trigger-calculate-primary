# SPDX-FileCopyrightText: Magenta ApS
#
# SPDX-License-Identifier: MPL-2.0
import datetime
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import call

import hypothesis.strategies as st
import pytest
from hypothesis import HealthCheck
from hypothesis import given
from hypothesis import settings

from calculate_primary.common import MOPrimaryEngagementUpdater


class AttrDict(dict):
    """Enable dot.notation access for a dict object.

    Example:
        script_result = AttrDict({"exit_code": 0})
        assert script_result.exit_code == 0
    """

    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__  # type: ignore
    __delattr__ = dict.__delitem__  # type: ignore


class MOPrimaryEngagementUpdaterTest(MOPrimaryEngagementUpdater):
    @classmethod
    async def create(cls, settings, mora_helper):
        return await super().create(settings, mora_helper)

    async def _find_primary_types(self):
        primary_dict = {
            "fixed_primary": "fixed_primary_uuid",
            "primary": "primary_uuid",
            "non_primary": "non_primary_uuid",
            "special_primary": "special_primary_uuid",
        }
        primary_list = [
            primary_dict["fixed_primary"],
            primary_dict["primary"],
            primary_dict["special_primary"],
        ]
        return primary_dict, primary_list

    def _find_primary(self, mo_engagements):
        return mo_engagements[0]["uuid"]


@pytest.fixture
async def recalculate_updater(dummy_settings) -> MOPrimaryEngagementUpdaterTest:
    updater = await MOPrimaryEngagementUpdaterTest.create(dummy_settings, AsyncMock())
    updater.helper._mo_post.return_value = AttrDict(
        {
            "status_code": 200,
        }
    )
    updater._ensure_primary = MagicMock(wraps=updater._ensure_primary)
    return updater


async def test_recalculate_no_engagements(
    recalculate_updater: MOPrimaryEngagementUpdaterTest,
):
    """Test that no engagements mean no changes and no attempted updates."""
    assert await recalculate_updater.recalculate_user("user_uuid") == {"user_uuid": 0}
    recalculate_updater._ensure_primary.assert_not_called()


@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(st.sampled_from(["primary_uuid", "fixed_primary_uuid"]))
async def test_recalculate_single_engagement_already_primary(
    recalculate_updater: MOPrimaryEngagementUpdaterTest, old_primary
):
    """Test that a primary engagement is still primary after recalculate."""
    cut_dates = [
        datetime.datetime(2930, 1, 1),
        datetime.datetime(9999, 12, 30, 0, 0),
    ]
    recalculate_updater.helper.find_cut_dates.return_value = cut_dates

    engagement = {"uuid": "engagement_uuid", "primary": {"uuid": old_primary}}

    async def _read_engagement(user_uuid, date):
        return [engagement]

    recalculate_updater._read_engagement = _read_engagement

    assert await recalculate_updater.recalculate_user("user_uuid") == {"user_uuid": 0}
    recalculate_updater._ensure_primary.assert_called_with(
        engagement, old_primary, {"from": "2930-01-01", "to": None}
    )
    recalculate_updater.helper._mo_post.assert_not_called()


@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(st.sampled_from(["non_primary_uuid", "unrelated_uuid"]))
async def test_recalculate_single_engagement_becoming_primary(
    recalculate_updater: MOPrimaryEngagementUpdaterTest, old_primary
):
    """Test that a non-primary engagement becomes primary after recalculate."""
    cut_dates = [
        datetime.datetime(2930, 1, 1),
        datetime.datetime(9999, 12, 30, 0, 0),
    ]
    recalculate_updater.helper.find_cut_dates.return_value = cut_dates

    engagement = {"uuid": "engagement_uuid", "primary": {"uuid": old_primary}}

    async def _read_engagement(user_uuid, date):
        return [engagement]

    recalculate_updater._read_engagement = _read_engagement

    assert await recalculate_updater.recalculate_user("user_uuid") == {"user_uuid": 1}
    recalculate_updater._ensure_primary.assert_called_with(
        engagement, "primary_uuid", {"from": "2930-01-01", "to": None}
    )
    recalculate_updater.helper._mo_post.assert_called_with(
        "details/edit",
        {
            "type": "engagement",
            "uuid": "engagement_uuid",
            "data": {
                "primary": {"uuid": "primary_uuid"},
                "validity": {"from": "2930-01-01", "to": None},
            },
        },
    )


async def test_recalculate_multiple_engagements(
    recalculate_updater: MOPrimaryEngagementUpdaterTest,
):
    """Test that non-primary engagements yield one primary after recalculate.

    Note: which one is subject to the _find_primary method, the test one simply
          picks the first one in the provided list.
    """
    engagements = [
        {"uuid": "engagement_uuid_1", "primary": {"uuid": "non_primary_uuid"}},
        {"uuid": "engagement_uuid_2", "primary": {"uuid": "non_primary_uuid"}},
    ]

    cut_dates = [
        datetime.datetime(2930, 1, 1),
        datetime.datetime(9999, 12, 30, 0, 0),
    ]
    recalculate_updater.helper.find_cut_dates.return_value = cut_dates

    async def _read_engagement(user_uuid, date):
        return engagements

    recalculate_updater._read_engagement = _read_engagement

    assert await recalculate_updater.recalculate_user("user_uuid") == {"user_uuid": 1}
    recalculate_updater._ensure_primary.assert_has_calls(
        [
            call(engagements[0], "primary_uuid", {"from": "2930-01-01", "to": None}),
            call(
                engagements[1],
                "non_primary_uuid",
                {"from": "2930-01-01", "to": None},
            ),
        ]
    )
    # Only one call, as non_primary is already non_primary
    recalculate_updater.helper._mo_post.assert_called_with(
        "details/edit",
        {
            "type": "engagement",
            "uuid": "engagement_uuid_1",
            "data": {
                "primary": {"uuid": "primary_uuid"},
                "validity": {"from": "2930-01-01", "to": None},
            },
        },
    )


async def test_recalculate_multiple_engagements_wrong_primary(
    recalculate_updater: MOPrimaryEngagementUpdaterTest,
):
    """Test that opposite primary engagements yield two after changes.

    Note: which one is subject to the _find_primary method, the test one simply
          picks the first one in the provided list.
    """
    engagements = [
        {"uuid": "engagement_uuid_1", "primary": {"uuid": "non_primary_uuid"}},
        {"uuid": "engagement_uuid_2", "primary": {"uuid": "primary_uuid"}},
    ]

    cut_dates = [
        datetime.datetime(2930, 1, 1),
        datetime.datetime(9999, 12, 30, 0, 0),
    ]
    recalculate_updater.helper.find_cut_dates.return_value = cut_dates

    async def _read_engagement(user_uuid, date):
        return engagements

    recalculate_updater._read_engagement = _read_engagement

    assert await recalculate_updater.recalculate_user("user_uuid") == {"user_uuid": 2}
    recalculate_updater._ensure_primary.assert_has_calls(
        [
            call(engagements[0], "primary_uuid", {"from": "2930-01-01", "to": None}),
            call(
                engagements[1],
                "non_primary_uuid",
                {"from": "2930-01-01", "to": None},
            ),
        ]
    )
    # Two calls, as primary is flipped for each
    recalculate_updater.helper._mo_post.assert_has_calls(
        [
            call(
                "details/edit",
                {
                    "type": "engagement",
                    "uuid": "engagement_uuid_1",
                    "data": {
                        "primary": {"uuid": "primary_uuid"},
                        "validity": {"from": "2930-01-01", "to": None},
                    },
                },
            ),
            call(
                "details/edit",
                {
                    "type": "engagement",
                    "uuid": "engagement_uuid_2",
                    "data": {
                        "primary": {"uuid": "non_primary_uuid"},
                        "validity": {"from": "2930-01-01", "to": None},
                    },
                },
            ),
        ]
    )


async def test_recalculate_multiple_engagements_fixed_primary(
    recalculate_updater: MOPrimaryEngagementUpdaterTest,
):
    """Test that fixed primaries overrule normal primary calculation.

    Note: which one is subject to the _find_primary method, the test one simply
          picks the first one in the provided list.
    """
    engagements = [
        {"uuid": "engagement_uuid_1", "primary": {"uuid": "non_primary_uuid"}},
        {"uuid": "engagement_uuid_2", "primary": {"uuid": "fixed_primary_uuid"}},
    ]

    cut_dates = [
        datetime.datetime(2930, 1, 1),
        datetime.datetime(9999, 12, 30, 0, 0),
    ]
    recalculate_updater.helper.find_cut_dates.return_value = cut_dates

    async def _read_engagement(user_uuid, date):
        return engagements

    recalculate_updater._read_engagement = _read_engagement

    assert await recalculate_updater.recalculate_user("user_uuid") == {"user_uuid": 0}
    recalculate_updater._ensure_primary.assert_has_calls(
        [
            call(
                engagements[0],
                "non_primary_uuid",
                {"from": "2930-01-01", "to": None},
            ),
            call(
                engagements[1],
                "fixed_primary_uuid",
                {"from": "2930-01-01", "to": None},
            ),
        ]
    )
    recalculate_updater.helper._mo_post.assert_not_called()
