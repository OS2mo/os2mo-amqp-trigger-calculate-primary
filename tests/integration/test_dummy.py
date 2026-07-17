# SPDX-FileCopyrightText: Magenta ApS <https://magenta.dk>
# SPDX-License-Identifier: MPL-2.0

import pytest


# TODO: this will be removed in the next commit, it is needed for the pipeline
#   to not fail, because it is not allowed to have 0 integration tests
@pytest.mark.integration_test
def test_dummy():
    assert True
