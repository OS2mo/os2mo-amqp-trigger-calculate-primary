# SPDX-FileCopyrightText: Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0
from typing import Annotated

from calculate_primary.common import MOPrimaryEngagementUpdater
from fastapi import Depends
from fastramqpi.depends import from_user_context

from calculate_primary.config import _Settings
from calculate_primary.main import 

Settings = Annotated[_Settings, Depends(from_user_context("settings"))]
Updater = Annotated[MOPrimaryEngagementUpdater, Depends(from_user_context("updater"))]
