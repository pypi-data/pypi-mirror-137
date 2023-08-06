#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# (c) Meta Platforms, Inc. and affiliates.
#
# Fedora-License-Identifier: GPLv2+
# SPDX-2.0-License-Identifier: GPL-2.0+
# SPDX-3.0-License-Identifier: GPL-2.0-or-later
#
# This program is free software.
# For more information on the license, see COPYING.md.
# For more information on free software, see
# <https://www.gnu.org/philosophy/free-sw.en.html>.

import pytest
import requests
from ebranch import pagure
from json import dumps
from unittest import mock


@pytest.fixture
def mock_response_404(monkeypatch):
    def mock_get(*args, **kwargs):
        response = mock.Mock()
        response.status_code = 404
        response.raise_for_status.side_effect = requests.exceptions.HTTPError
        response.text = "<html><body>404</body></html>"
        return response

    monkeypatch.setattr(requests, "get", mock_get)


@pytest.fixture
def mock_response_ebranch(monkeypatch):
    def mock_get(*args, **kwargs):
        response = mock.MagicMock(
            status_code=200, text=dumps({"branches": ["epel9", "rawhide"]})
        )
        return response

    monkeypatch.setattr(requests, "get", mock_get)


def test_get_pkg_branches_ebranch(mock_response_ebranch):
    result = pagure.get_pkg_branches("ebranch")
    assert result == ["epel9", "rawhide"]


def test_get_pkg_branches_404(mock_response_404):
    with pytest.raises(requests.exceptions.HTTPError):
        pagure.get_pkg_branches("no-such-package")


def test_is_pkg_branched_404(mock_response_404):
    with pytest.raises(requests.exceptions.HTTPError):
        pagure.is_pkg_branched("no-such-package", "epel9")
