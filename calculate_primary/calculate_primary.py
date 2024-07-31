# SPDX-FileCopyrightText: Magenta ApS
#
# SPDX-License-Identifier: MPL-2.0
import json
import logging
import sys

import click

from calculate_primary.common import LOGGER_NAME


def get_engagement_updater(integration):
    if integration == "DEFAULT":
        from calculate_primary.default import (
            DefaultPrimaryEngagementUpdater,
        )

        return DefaultPrimaryEngagementUpdater
    if integration == "SD":
        from calculate_primary.sd import SDPrimaryEngagementUpdater

        return SDPrimaryEngagementUpdater
    if integration == "OPUS":
        from calculate_primary.opus import OPUSPrimaryEngagementUpdater

        return OPUSPrimaryEngagementUpdater
    raise NotImplementedError("Unexpected integration: " + str(integration))


@click.command()
@click.option(
    "--integration",
    type=click.Choice(["DEFAULT", "SD", "OPUS"], case_sensitive=False),
    required=True,
    help="Integration to use",
)
@click.option("--dry-run", is_flag=True, type=click.BOOL, help="Make no changes")
@click.option(
    "--mo-url",
    help="OS2mo URL",
    required=True,
    envvar="MO_URL",
)
@click.option(
    "--eng-types-primary-order",
    help="Priority of engagement types. Only relevant for OPUS",
    default="[]",
    envvar="ENG_TYPES_PRIMARY_ORDER",
)
@click.option("--check-all", is_flag=True, type=click.BOOL, help="Check all users")
@click.option("--check-user", type=click.UUID, help="Check one user")
@click.option(
    "--recalculate-all", is_flag=True, type=click.BOOL, help="Recalculate all users"
)
@click.option("--recalculate-user", type=click.UUID, help="Recalculate one user")
def calculate_primary(
    integration, dry_run, mo_url, eng_types_primary_order: str,
    check_all, check_user, recalculate_all, recalculate_user
):
    """Tool to work with primary engagement(s)."""
    # Acquire the configured updater


    updater_class = get_engagement_updater(integration=integration)
    updater = updater_class(dry_run=dry_run, mo_url=mo_url, eng_types_primary_order=json.loads(eng_types_primary_order))

    # Run the specified operation
    if check_all:
        print("Check all")
        updater.check_all()
    if check_user:
        print("Check user")
        updater.check_user(check_user)
    if recalculate_all:
        print("Recalculate all")
        updater.recalculate_all()
    if recalculate_user:
        print("Recalculate user")
        print(updater.recalculate_user(recalculate_user))


if __name__ == "__main__":
    calculate_primary()  # type: ignore
