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

import click
import json
import requests
import sys
from . import dnf, pagure


@click.group()
def cli():
    pass


@cli.command(help="lists build requirements for a package")
@click.argument("pkgname")
@click.option("-r", "--ref-repo", default="rawhide-source", show_default=True)
def build_reqs(pkgname: str, ref_repo: str):
    click.echo(dnf.get_pkg_build_reqs(pkgname, ref_repo))


@cli.command(help="checks if a package is branched")
@click.argument("pkgname")
@click.argument("branch")
def is_branched(pkgname: str, branch: str):
    try:
        if pagure.is_pkg_branched(pkgname, branch):
            click.echo(f"{pkgname} is branched for {branch}")
        else:
            click.echo(f"{pkgname} is NOT branched for {branch}")
            sys.exit(1)
    except requests.exceptions.HTTPError as error:
        if error.response.status_code == 404:
            click.echo(f"{pkgname} does not exist in dist-git")
            sys.exit(2)


@cli.command(help="lists branches for a package")
@click.argument("pkgname")
def ls_branches(pkgname: str):
    try:
        click.echo(json.dumps(pagure.get_pkg_branches(pkgname)))
    except requests.exceptions.HTTPError as error:
        if error.response.status_code == 404:
            click.echo(f"{pkgname} does not exist in dist-git")
            sys.exit(2)


@cli.command(help="lists missing build requirements to build for a branch")
@click.argument("pkgname")
@click.argument("branch")
@click.option("-f", "--report-file", envvar="EBRANCH_FILE", default="")
@click.option(
    "-r",
    "--ref-repo",
    envvar="EBRANCH_REF",
    default="rawhide-source",
    show_default=True,
)
@click.option("--update/--no-update", default=False, show_default=True)
def missing_build_reqs(
    pkgname: str, branch: str, report_file: str, ref_repo: str, update: bool
):
    import subprocess

    try:
        click.echo(
            json.dumps(
                dnf.report_missing_serialized(
                    pkgname,
                    branch,
                    report_file=report_file,
                    ref_repo=ref_repo,
                    update=update,
                ),
                indent=2,
            )
        )
    except subprocess.CalledProcessError as error:
        click.echo(error.stderr)
        sys.exit(2)


@cli.command(help="adds new missing BRs to the top-level list")
@click.argument("report_file")
def unfold_report(report_file: str):
    click.echo(
        json.dumps(
            dnf.unfold_report_serialized(
                report_file,
            ),
            indent=2,
        )
    )


@cli.command(help="computes missing BRs for new top-level packages")
@click.argument("report_file")
@click.argument("branch")
@click.option(
    "-r",
    "--ref-repo",
    envvar="EBRANCH_REF",
    default="rawhide-source",
    show_default=True,
)
def iterate_report(report_file: str, branch: str, ref_repo: str):
    click.echo(
        json.dumps(
            dnf.iterate_report_serialized(report_file, branch, ref_repo=ref_repo),
            indent=2,
        )
    )
