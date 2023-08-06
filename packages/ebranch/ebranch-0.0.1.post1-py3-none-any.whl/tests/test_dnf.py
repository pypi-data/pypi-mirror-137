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
import subprocess
from ebranch import dnf
from unittest import mock


@pytest.fixture
def mock_repoquery_error(monkeypatch):
    def mock_run(*args, **kwargs):
        response = mock.Mock()
        response.check_returncode.side_effect = subprocess.CalledProcessError(
            returncode=1, cmd=["dnf"]
        )
        return response

    monkeypatch.setattr(subprocess, "run", mock_run)


@pytest.fixture
def mock_repoquery_publicinbox(monkeypatch):
    def mock_run(*args, **kwargs):
        response = mock.Mock()
        response.stdout = b"curl\ne2fsprogs\ngit >= 2.6\nman-db\nperl\nperl(DBD::SQLite)\nperl(Email::Address::XS)\nperl(ExtUtils::MakeMaker)\nperl(IO::Socket::SSL)\nperl(Inline::C)\nperl(Mail::IMAPClient)\nperl(Parse::RecDescent)\nperl(Plack::Middleware::ReverseProxy)\nperl(Plack::Test)\nperl(Search::Xapian)\nperl-generators\npkgconfig(libgit2)\nsqlite\nxapian-core\n"
        return response

    monkeypatch.setattr(subprocess, "run", mock_run)


@pytest.fixture
def mock_whatprovides_bash(monkeypatch):
    def mock_run(*args, **kwargs):
        response = mock.Mock()
        response.stdout = b"bash\n"
        return response

    monkeypatch.setattr(subprocess, "run", mock_run)


@pytest.fixture
def mock_whatprovides_xapian(monkeypatch):
    def mock_run(*args, **kwargs):
        response = mock.Mock()
        response.stdout = b""
        return response

    monkeypatch.setattr(subprocess, "run", mock_run)


def test_build_req_available(mock_whatprovides_bash):
    result = dnf.build_req_available_p("bash", "epel9")
    assert result is True


def test_build_req_unavailable(mock_whatprovides_xapian):
    result = dnf.build_req_available_p("perl(Search::Xapian)", "epel9")
    assert result is False


def test_filter_build_reqs(monkeypatch):
    def mock_srpm_providing(req: str) -> str:
        mock_mapping = {
            "foo": "foobar_source",
            "bar": "foobar_source",
            "baz": "baz_source",
            "spam": "spam_source",
        }
        return mock_mapping[req]

    monkeypatch.setattr(dnf, "get_srpm_providing", mock_srpm_providing)

    def mock_build_req_available(req: str, repos: list[str]) -> bool:
        mock_mapping = {
            "foo": False,
            "bar": False,
            "baz": True,
            "spam": False,
            "ham": True,
            "eggs": True,
        }
        return mock_mapping[req]

    monkeypatch.setattr(dnf, "build_req_available_p", mock_build_req_available)

    result = dnf.filter_build_reqs(["foo", "bar", "baz", "spam", "ham", "eggs"], [])
    assert result == [
        ("foobar_source", "foo"),
        ("foobar_source", "bar"),
        ("spam_source", "spam"),
    ]
    assert dnf.dedup_build_reqs(result) == {
        "foobar_source": ["foo", "bar"],
        "spam_source": ["spam"],
    }


def test_report_iterate(monkeypatch):
    report = {
        "python-b4": {
            "build": {
                "python-dkimpy": [
                    "(python3dist(dkimpy) >= 1 with python3dist(dkimpy) < 2)",
                    "(python3dist(dkimpy) >= 1.0.5 with python3dist(dkimpy) < 1.1)",
                ],
                "python-patatt": [
                    "(python3dist(patatt) < 2~~ with python3dist(patatt) >= 0.4)"
                ],
            }
        },
        "python-dkimpy": {"skip": True},
        "python-patatt": {},
    }
    mock_get_missing = mock.Mock()
    monkeypatch.setattr(dnf, "report_missing_build_reqs", mock_get_missing)
    patatt_brs = {
        "python-patatt": {"build": {"python-pynacl": ["python3dist(pynacl)"]}}
    }
    mock_get_missing.return_value = patatt_brs
    result = dnf.iterate_report(report, "epel9")
    assert result["python-b4"] == report["python-b4"]
    assert result["python-dkimpy"] == report["python-dkimpy"]
    assert result["python-patatt"] == patatt_brs["python-patatt"]
    mock_get_missing.assert_called_once_with(
        "python-patatt", "epel9", [], "rawhide-source"
    )


def test_remote_iterate_serialized(monkeypatch):
    mock_load = mock.Mock()
    mock_iterate = mock.Mock()
    mock_save = mock.Mock()
    monkeypatch.setattr(dnf, "load_report", mock_load)
    monkeypatch.setattr(dnf, "iterate_report", mock_iterate)
    monkeypatch.setattr(dnf, "save_report", mock_save)
    orig_report = {"foo": {"build": {"bar": []}}}
    expanded_report = {"foo": {"build": {"bar": []}}, "bar": {}}
    mock_load.return_value = orig_report
    mock_iterate.return_value = expanded_report
    report_file = "report.json"
    result = dnf.iterate_report_serialized(report_file, "epel9")
    mock_load.assert_called_once_with(report_file)
    mock_iterate.assert_called_once_with(orig_report, "epel9", [], "rawhide-source")
    mock_save.assert_called_once_with(expanded_report, report_file)
    assert result == expanded_report


def test_get_pkg_build_reqs_publicinbox(mock_repoquery_publicinbox):
    result = dnf.get_pkg_build_reqs("public-inbox")
    assert "perl(Search::Xapian)" in result


def test_get_pkg_build_reqs_error(mock_repoquery_error):
    with pytest.raises(subprocess.CalledProcessError):
        dnf.get_pkg_build_reqs("some-random-package")


def test_get_pkg_missing_build_reqs(monkeypatch):
    reqs = ["curl", "perl(Search::Xapian)"]

    def mock_get_reqs(pkg: str, ref_repo: str):
        return reqs

    monkeypatch.setattr(dnf, "get_pkg_build_reqs", mock_get_reqs)

    mock_filter = mock.Mock()
    monkeypatch.setattr(dnf, "filter_build_reqs", mock_filter)

    result = dnf.get_pkg_missing_build_reqs("public-inbox", "epel9")
    mock_filter.assert_called_once_with(reqs, dnf.REPOS["epel9"])


def test_get_srpm_providing(mock_whatprovides_bash):
    result = dnf.get_srpm_providing("bash")
    assert result == "bash"


def test_report_unfold():
    d = {
        "python-b4": {
            "build": {
                "python-dkimpy": [
                    "(python3dist(dkimpy) >= 1 with python3dist(dkimpy) < 2)",
                    "(python3dist(dkimpy) >= 1.0.5 with python3dist(dkimpy) < 1.1)",
                ],
                "python-patatt": [
                    "(python3dist(patatt) < 2~~ with python3dist(patatt) >= 0.4)"
                ],
            }
        },
        "python-patatt": {
            "build": {},
        },
        "python-foo": {
            "build": {
                "python-bar": ["(python3dist(bar)"],
            },
            "skip": True,
        },
    }

    result = dnf.unfold_report(d)

    assert "python-bar" not in result
    assert "python-dkimpy" in result
    assert "python-patatt" in result


def test_report_unfold_serialized(monkeypatch):
    mock_load = mock.Mock()
    mock_unfold = mock.Mock()
    mock_save = mock.Mock()
    monkeypatch.setattr(dnf, "load_report", mock_load)
    monkeypatch.setattr(dnf, "unfold_report", mock_unfold)
    monkeypatch.setattr(dnf, "save_report", mock_save)
    orig_report = {"foo": {"build": {"bar": []}}}
    expanded_report = {"foo": {"build": {"bar": []}}, "bar": {}}
    mock_load.return_value = orig_report
    mock_unfold.return_value = expanded_report
    report_file = "report.json"
    result = dnf.unfold_report_serialized(report_file)
    mock_load.assert_called_once_with(report_file)
    mock_unfold.assert_called_once_with(orig_report)
    mock_save.assert_called_once_with(expanded_report, report_file)
    assert result == expanded_report


def test_report_load_non_existent(monkeypatch):
    from os import path

    mock_exists = mock.Mock()
    monkeypatch.setattr(path, "exists", mock_exists)
    mock_exists.return_value = False
    report_file = "/some/non-existent-file.json"
    result = dnf.load_report(report_file)
    mock_exists.assert_called_once_with(report_file)
    assert result == {}


def test_report_load_no_perm(monkeypatch):
    import io
    from os import path

    mock_exists = mock.Mock()
    monkeypatch.setattr(path, "exists", mock_exists)
    mock_exists.return_value = True
    report_file = "/root/no-access.json"
    mock_open = mock.Mock()
    monkeypatch.setattr(io, "open", mock_open)
    mock_open.side_effect = PermissionError()
    result = dnf.load_report(report_file)
    mock_exists.assert_called_once_with(report_file)
    mock_open.assert_called_once_with(report_file, "r")
    assert result == {}


def test_report_load_invalid(monkeypatch):
    import io
    import json
    from os import path

    mock_exists = mock.Mock()
    monkeypatch.setattr(path, "exists", mock_exists)
    mock_exists.return_value = True
    mock_open = mock.Mock()
    mock_fp = mock.MagicMock()
    monkeypatch.setattr(io, "open", mock_open)
    mock_open.return_value = mock_fp
    mock_load = mock.Mock()
    monkeypatch.setattr(json, "load", mock_load)
    mock_load.side_effect = json.decoder.JSONDecodeError("Expecting value", "", 0)
    report_file = "/some/invalid-json-file.json"
    result = dnf.load_report(report_file)
    mock_exists.assert_called_once_with(report_file)
    assert result == {}


def test_report_load_valid(monkeypatch):
    import io
    import json
    from os import path

    mock_exists = mock.Mock()
    monkeypatch.setattr(path, "exists", mock_exists)
    mock_exists.return_value = True
    mock_open = mock.Mock()
    mock_fp = mock.MagicMock()
    monkeypatch.setattr(io, "open", mock_open)
    mock_open.return_value = mock_fp
    mock_load = mock.Mock()
    monkeypatch.setattr(json, "load", mock_load)
    d = {"pkg": {"build": ["srcdep1", "srcdep2"]}}
    mock_load.return_value = d
    report_file = "/some/valid-json-file.json"
    result = dnf.load_report(report_file)
    mock_exists.assert_called_once_with(report_file)
    assert result == d


def test_report_save_no_perm(monkeypatch):
    import io

    report_file = "/root/no-access.json"
    mock_open = mock.Mock()
    monkeypatch.setattr(io, "open", mock_open)
    mock_open.side_effect = PermissionError()
    dnf.save_report({}, report_file)
    mock_open.assert_called_once_with(report_file, "w")


def test_report_save_ok(monkeypatch):
    import io
    import json

    report_file = "pkg.json"
    mock_open = mock.Mock()
    mock_fp = mock.MagicMock()
    monkeypatch.setattr(io, "open", mock_open)
    mock_open.return_value = mock_fp
    mock_dump = mock.Mock()
    monkeypatch.setattr(json, "dump", mock_dump)
    d = {"pkg": {"build": ["srcdep1", "srcdep2"]}}
    dnf.save_report(d, report_file)
    mock_open.assert_called_once_with(report_file, "w")
    mock_dump.assert_called_once_with(d, mock_fp.__enter__(), indent=2)


def test_report_missing_buildreqs(monkeypatch):
    mock_getter = mock.Mock()
    dkim1 = "(python3dist(dkimpy) >= 1 with python3dist(dkimpy) < 2)"
    dkim2 = "(python3dist(dkimpy) >= 1.0.5 with python3dist(dkimpy) < 1.1)"
    patatt = "(python3dist(patatt) < 2~~ with python3dist(patatt) >= 0.4)"
    mock_getter.return_value = [
        ("python-dkimpy", dkim1),
        ("python-dkimpy", dkim2),
        ("python-patatt", patatt),
    ]
    monkeypatch.setattr(dnf, "get_pkg_missing_build_reqs", mock_getter)

    result = dnf.report_missing_build_reqs("python-b4", "epel9")
    mock_getter.assert_called_once()
    assert result == {
        "python-b4": {
            "build": {
                "python-dkimpy": [dkim1, dkim2],
                "python-patatt": [patatt],
            }
        }
    }


def test_report_missing_serialized_match_no_update(monkeypatch):
    mock_load = mock.Mock()
    monkeypatch.setattr(dnf, "load_report", mock_load)
    mock_save = mock.Mock()
    monkeypatch.setattr(dnf, "save_report", mock_save)
    d = {"pkg": {"build": {"oldsrc1": ["olddep1"], "oldsrc2": ["olddep2"]}}}
    mock_load.return_value = d
    result = dnf.report_missing_serialized(
        "pkg", "epel9", report_file="pkg.json", update=False
    )
    assert result == d
    mock_save.assert_not_called()


def test_report_missing_serialized_no_match_no_update(monkeypatch):
    mock_load = mock.Mock()
    monkeypatch.setattr(dnf, "load_report", mock_load)
    mock_save = mock.Mock()
    monkeypatch.setattr(dnf, "save_report", mock_save)
    d1 = {"pkg": {"build": {"oldsrc1": ["olddep1"], "oldsrc2": ["olddep2"]}}}
    mock_load.return_value = d1
    mock_report = mock.Mock()
    monkeypatch.setattr(dnf, "report_missing_build_reqs", mock_report)
    d2 = {"pkg2": {"build": {"src3": ["dep3a", "dep3b"]}}}
    mock_report.return_value = d2
    result = dnf.report_missing_serialized(
        "pkg2", "epel9", report_file="report.json", update=False
    )
    assert result == {**d1, **d2}
    mock_save.assert_called_once()


def test_report_missing_serialized_match_update(monkeypatch):
    mock_load = mock.Mock()
    monkeypatch.setattr(dnf, "load_report", mock_load)
    mock_save = mock.Mock()
    monkeypatch.setattr(dnf, "save_report", mock_save)
    d1 = {"pkg": {"build": {"oldsrc1": ["olddep1"], "oldsrc2": ["olddep2"]}}}
    mock_load.return_value = d1
    mock_report = mock.Mock()
    monkeypatch.setattr(dnf, "report_missing_build_reqs", mock_report)
    d2 = {"pkg": {"build": {"src3": ["dep3a", "dep3b"]}}}
    mock_report.return_value = d2
    result = dnf.report_missing_serialized(
        "pkg", "epel9", report_file="report.csv", update=True
    )
    assert result == d2
    mock_save.assert_called_once()
