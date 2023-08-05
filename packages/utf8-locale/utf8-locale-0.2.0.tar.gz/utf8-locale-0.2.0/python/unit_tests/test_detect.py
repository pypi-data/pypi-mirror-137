"""Test the UTF-8 locale detection functions."""

# Copyright (c) 2020 - 2022  Peter Pentchev <roam@ringlet.net>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.


import json
import os
import pathlib
import subprocess
import unittest

from unittest import mock

from typing import Dict, List, NamedTuple, Optional  # noqa: H301

import ddt  # type: ignore
import pytest

import utf8_locale


class TData(NamedTuple):
    """The test data loaded from the JSON definitions file."""

    locales: List[str]


class TDataHolder:
    """A singleton object holding the test data."""

    # pylint: disable=too-few-public-methods

    data: Optional[TData] = None

    @classmethod
    def load(cls) -> TData:
        """Load the test data from the JSON definitions file."""
        if cls.data is not None:
            return cls.data

        raw = json.loads(
            (pathlib.Path(__file__).absolute().parent.parent.parent / "tests/data.json").read_text(
                encoding="UTF-8"
            )
        )
        assert raw["format"]["version"] == {"major": 0, "minor": 1}

        cls.data = TData(locales=raw["locales"])
        return cls.data


LANG_KEYS = set(["LC_ALL", "LANGUAGE"])

LANG_EXPECTED = [
    (["C", "en"], "C.UTF-8"),
    (["en", "C"], "en_XX.UTF-8"),
    (["es", "bg", "*"], "it_IT.UTF-8"),
    (["en", "bg", "*"], "en_XX.UTF-8"),
    (["es", "*", "en"], "it_IT.UTF-8"),
    (["es", "*", "it"], "de_DE.UTF-8"),
    (["en", "bg", "en"], "en_XX.UTF-8"),
    (["it", "en", "it"], "it_IT.UTF-8"),
    (["xy", "yz", "xy", "en"], "en_XX.UTF-8"),
]


def check_env(env: Dict[str, str]) -> None:
    """Make sure a UTF8-capable environment was setup correctly."""
    # Everything except LANG_KEYS is the same as in os.environ
    assert {key: value for key, value in env.items() if key not in LANG_KEYS} == {
        key: value for key, value in os.environ.items() if key not in LANG_KEYS
    }

    # The rest of this function makes sure that locale(1) and date(1), when
    # run in this environment, output reasonable values
    loc = {
        fields[0]: fields[1].strip('"')
        for fields in (
            line.split("=", 1)
            for line in subprocess.check_output(
                ["locale"], shell=False, env=env, encoding="UTF-8"
            ).splitlines()
        )
    }
    non_lc = set(name for name in loc if not name.startswith("LC_"))
    assert non_lc.issubset(set(("LANG", "LANGUAGE")))
    loc = {name: value for name, value in loc.items() if name.startswith("LC_")}
    values = list(set(loc.values()))
    assert len(values) == 1, values
    assert values[0].lower().endswith(".utf8") or values[0].lower().endswith(".utf-8")

    utc_env = dict(env)
    utc_env["TZ"] = "UTC"
    lines = subprocess.check_output(
        ["date", "-d", "@1000000000", "+%A"],
        shell=False,
        env=utc_env,
        encoding="UTF-8",
    ).splitlines()
    assert lines in [["Sunday"], ["Sonntag"], ["domenica"], ["domingo"]]


def test_utf8_env() -> None:
    """Test get_utf8_env() and, indirectly, detect_utf8_locale()."""
    env = utf8_locale.get_utf8_env()
    check_env(env)

    mod_env = {
        key: value
        for key, value in os.environ.items()
        if key not in ("HOME", "USER", "PS1", "PATH")
    }
    mod_env["TEST_KEY"] = "test value"

    env2 = utf8_locale.get_utf8_env(mod_env)
    # Nothing besides LANG_KEYS has changed
    assert {key: value for key, value in env2.items() if key not in LANG_KEYS} == {
        key: value for key, value in mod_env.items() if key not in LANG_KEYS
    }

    # LANG_KEYS have changed in the same way as before
    assert {key: value for key, value in env2.items() if key in LANG_KEYS} == {
        key: value for key, value in env.items() if key in LANG_KEYS
    }


def mock_locale():  # type: ignore
    """Mock subprocess.check_output("locale -a")."""
    locales = TDataHolder.load().locales
    mock_check_output = mock.Mock(spec=["__call__"])
    mock_check_output.return_value = "".join(item + "\n" for item in locales)
    return mock.patch("subprocess.check_output", new=mock_check_output)


@ddt.ddt
class TestLanguages(unittest.TestCase):
    """Test the language preference handling of detect_utf8_locale()."""

    # pylint: disable=no-self-use

    @ddt.data(*LANG_EXPECTED)
    @ddt.unpack
    def test_language(self, languages: List[str], result: str) -> None:
        """Test detect_utf8_locale() with some languages specified."""
        with mock_locale():  # type: ignore
            assert utf8_locale.detect_utf8_locale(languages=languages) == result

    @ddt.data(*LANG_EXPECTED)
    @ddt.unpack
    def test_language_vars(self, languages: List[str], result: str) -> None:
        """Test detect_utf8_locale() with some languages specified."""
        with mock_locale():  # type: ignore
            assert utf8_locale.get_utf8_vars(languages=languages) == {
                "LC_ALL": result,
                "LANGUAGE": "",
            }

    def test_no_languages(self) -> None:
        """Test detect_utf8_locale() with no languages specified."""
        with mock_locale():  # type: ignore
            with pytest.raises(ValueError):
                utf8_locale.detect_utf8_locale(languages=[])


def test_preferred() -> None:
    """Test the get_preferred_languages() function."""
    env = {
        "LC_ALL": "bg_BG.UTF-8",
        "LC_MONETARY": "en_US.UTF-8",
        "LANG": "en_US.ISO-8859-1",
        "LC_NAME": "ru_RU.UTF-8",
    }
    assert utf8_locale.get_preferred_languages(env) == ["bg", "ru", "en", "C"]

    env["LANG"] = "en_US.UTF-8"
    assert utf8_locale.get_preferred_languages(env) == ["bg", "en", "ru", "C"]
