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
import subprocess

REPOS = {
    "epel8": [
        "c8s-baseos",
        "c8s-appstream",
        "c8s-extras",
        "c8s-powertools",
        "c8s-epel",
    ],
    "epel9": ["c9s-baseos", "c9s-appstream", "c9s-crb", "c9s-epel"],
}


def build_req_available_p(req: str, repos: list[str]) -> bool:
    repos_str = ",".join(repos)
    r = subprocess.run(
        f"dnf --disablerepo=* --enablerepo={repos_str} repoquery --whatprovides '{req}'",
        capture_output=True,
        shell=True,
    )
    r.check_returncode()

    # if there's no match, stdout is empty
    return bool(r.stdout)


def dedup_build_reqs(reqs: list[tuple[str, str]]) -> dict[str, list[str]]:
    res = {}
    for src, buildreq in reqs:
        res.setdefault(src, []).append(buildreq)
    return res


def filter_build_reqs(reqs: list[str], repos: list[str]) -> list[str]:
    return [
        (get_srpm_providing(req), req)
        for req in reqs
        if not build_req_available_p(req, repos)
    ]


def get_pkg_build_reqs(pkg: str, repo: str = "rawhide-source") -> list[str]:
    r = subprocess.run(
        f"dnf --disablerepo=* --enablerepo={repo} repoquery --requires {pkg}",
        capture_output=True,
        shell=True,
    )

    r.check_returncode()
    return r.stdout.decode().splitlines()


def get_pkg_missing_build_reqs(
    pkg: str, branch: str, repos: list[str] = [], ref_repo: str = "rawhide-source"
) -> list[str]:
    reqs = get_pkg_build_reqs(pkg, ref_repo)
    if not repos:
        repos = REPOS[branch]
    return filter_build_reqs(reqs, repos)


def get_srpm_providing(req: str, repo: str = "rawhide") -> str:
    qf = "--qf '%{source_name}'"
    r = subprocess.run(
        f"dnf --disablerepo=* --enablerepo={repo} repoquery {qf} --whatprovides '{req}'",
        capture_output=True,
        shell=True,
    )
    r.check_returncode()
    return r.stdout.decode().splitlines()[0]


def report_missing_build_reqs(
    pkg: str, branch: str, repos: list[str] = [], ref_repo: str = "rawhide-source"
) -> dict[str, dict]:
    res = get_pkg_missing_build_reqs(pkg, branch, repos, ref_repo)
    dedup_reqs = dedup_build_reqs(res)
    return {pkg: {"build": dedup_reqs}}


def unfold_report(report: dict[str, dict]) -> dict[str, dict]:
    expanded_report = {}
    for pkg in report:
        pkg_data = report[pkg]
        expanded_report[pkg] = pkg_data
        if pkg_data.get("skip", False):
            # package marked as not to be processed
            continue
        buildreqs = pkg_data.get("build", {})
        for buildreq in buildreqs:
            if buildreq in report:
                continue
            expanded_report[buildreq] = {}
    return expanded_report


def unfold_report_serialized(report_file: str):
    report = load_report(report_file)
    expanded_report = unfold_report(report)
    save_report(expanded_report, report_file)
    return expanded_report


def iterate_report(
    report: dict[str, dict],
    branch: str,
    repos: list[str] = [],
    ref_repo: str = "rawhide-source",
) -> dict[str, dict]:
    expanded_report = {}
    for pkg in report:
        pkg_data = report[pkg]
        expanded_report[pkg] = pkg_data
        if pkg_data.get("skip", False):
            # package marked as not to be processed
            continue
        if not "build" in pkg_data:
            pkg_report = report_missing_build_reqs(pkg, branch, repos, ref_repo)
            new_pkg_data = pkg_report[pkg]
            expanded_report[pkg] = {**pkg_data, **new_pkg_data}
    return expanded_report


def iterate_report_serialized(
    report_file: str,
    branch: str,
    repos: list[str] = [],
    ref_repo: str = "rawhide-source",
) -> dict[str, dict]:
    import sys

    existing_report = load_report(report_file)
    expanded_report = iterate_report(existing_report, branch, repos, ref_repo)
    if existing_report == expanded_report:
        print("Report unchanged", file=sys.stderr)
    elif len(existing_report) > len(expanded_report):
        print("ERROR: new report is shorter, cowardly refusing to save it", file=sys.stderr)
    else:
        save_report(expanded_report, report_file)
    return expanded_report


def load_report(report_file: str) -> dict[str, dict]:
    import io
    import os
    import sys

    if not os.path.exists(report_file):
        return {}
    try:
        with io.open(report_file, "r") as fp:
            try:
                report = json.load(fp)
            except json.decoder.JSONDecodeError:
                report = {}
    except BaseException as e:
        print(f"{e.strerror}: {report_file}", file=sys.stderr)
        report = {}
    return report


def save_report(report: dict[str, dict], report_file: str):
    import io
    import sys

    try:
        with io.open(report_file, "w") as fp:
            json.dump(report, fp, indent=2)
    except BaseException as e:
        print(f"{e.strerror}: {report_file}", file=sys.stderr)


def report_missing_serialized(
    pkg: str,
    branch: str,
    report_file: str = "",
    repos: list[str] = [],
    ref_repo: str = "rawhide-source",
    update: str = False,
) -> dict[str, dict]:
    existing_report = load_report(report_file) if report_file else {}
    if pkg in existing_report and not update:
        return existing_report
    else:
        pkg_report = report_missing_build_reqs(pkg, branch, repos, ref_repo)
        if pkg in existing_report:
            existing_report[pkg].update(pkg_report[pkg])
        else:
            existing_report.update(pkg_report)
        save_report(existing_report, report_file)
        return existing_report
