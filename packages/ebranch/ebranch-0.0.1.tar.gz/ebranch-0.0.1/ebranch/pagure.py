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

import json
import requests


def get_pkg_branches(pkg: str) -> list[str]:
    r = requests.get(f"https://src.fedoraproject.org/api/0/rpms/{pkg}/git/branches")
    r.raise_for_status()
    return json.loads(r.text)["branches"]


def is_pkg_branched(pkg: str, branch: str) -> bool:
    return branch in get_pkg_branches(pkg)
