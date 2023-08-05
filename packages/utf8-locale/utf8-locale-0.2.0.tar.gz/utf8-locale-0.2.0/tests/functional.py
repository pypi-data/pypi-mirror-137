#!/usr/bin/python3
#
# Copyright (c) 2022  Peter Pentchev <roam@ringlet.net>
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
"""Test the operation of the u8loc tool."""

import argparse
import json
import os
import pathlib
import subprocess
import sys
import tempfile

from typing import Dict, List, NamedTuple, Optional  # noqa: H301

import feature_check

from utf8_locale import detect


class TData(NamedTuple):
    """Test data read from the definitions file."""

    locales: List[str]


class TestDetect(NamedTuple):
    """A single test case for detecting a locale."""

    expected: str
    expected_preferred: List[str]
    preferred: bool
    env_add: Optional[Dict[str, str]]


DETECT_CASES = [
    TestDetect(expected="C.UTF-8", expected_preferred=["C"], preferred=False, env_add=None),
    TestDetect(
        expected="C.UTF-8",
        expected_preferred=["it", "C"],
        preferred=False,
        env_add={"LANG": "it_IT.UTF-8", "LANGUAGE": "it"},
    ),
    TestDetect(expected="C.UTF-8", expected_preferred=["C"], preferred=True, env_add=None),
    TestDetect(
        expected="it_IT.UTF-8",
        expected_preferred=["it", "C"],
        preferred=True,
        env_add={"LANG": "it_IT.UTF-8"},
    ),
    TestDetect(
        expected="it_IT.UTF-8",
        expected_preferred=["it", "C"],
        preferred=True,
        env_add={"LANG": "it_IT.UTF-8", "LANGUAGE": "it"},
    ),
    TestDetect(
        expected="en_XX.UTF-8",
        expected_preferred=["en", "it", "C"],
        preferred=True,
        env_add={"LANG": "it_IT.UTF-8", "LANGUAGE": "en", "LC_ALL": "en_XX.UTF-8"},
    ),
    TestDetect(
        expected="C.UTF-8",
        expected_preferred=["no", "C"],
        preferred=True,
        env_add={"LANG": "no_SUCH.UTF-8", "LANGUAGE": "en"},
    ),
]


class Config(NamedTuple):
    """Runtime configuration for the functional test."""

    env: Dict[str, str]
    program: pathlib.Path
    data: TData


def clean_environment() -> Dict[str, str]:
    """Clean up our environment, remove all the pertinent variables."""
    keys = set(detect.LOCALE_VARIABLES)
    if "LC_ALL" not in keys or "LANG" not in keys or "LC_MESSAGES" not in keys:
        sys.exit(f"LOCALE_VARIABLES does not contain some basic values: {keys!r}")
    keys.add("LANGUAGE")

    return {key: value for key, value in os.environ.items() if key not in keys}


def read_test_data() -> TData:
    """Parse the JSON test data definitions file."""
    raw = json.loads(pathlib.Path(__file__).with_name("data.json").read_text(encoding="UTF-8"))
    if raw["format"]["version"] != {"major": 0, "minor": 1}:
        sys.exit("Unexpected format version in the tests/data.json file")

    return TData(locales=raw["locales"])


def parse_args() -> Config:
    """Parse the command-line arguments."""
    parser = argparse.ArgumentParser(prog="u8loc-functional-test")
    parser.add_argument(
        "-p",
        "--program",
        type=pathlib.Path,
        required=True,
        help="the path to the u8loc executable to test",
    )

    args = parser.parse_args()

    program = args.program.absolute()
    if not program.is_file() or not os.access(program, os.X_OK):
        sys.exit(f"Not an executable regular file: {program}")

    return Config(env=clean_environment(), program=program, data=read_test_data())


def create_locale_tool(cfg: Config, tempd: pathlib.Path) -> None:
    """Create a locale(1)-like mock binary for our purposes."""
    # This ought to be read from a file, right?
    locales = "\n".join(cfg.data.locales)

    locale = tempd / "bin/locale"
    locale.parent.mkdir(mode=0o755)
    locale.write_text(
        f"""#!/bin/sh

if [ "$#" -ne 1 ] || [ "$1" != '-a' ]; then
    echo 'Usage: locale -a' 1>&2
    exit 61
fi

cat <<'EOLOC'
{locales}
EOLOC""",
        encoding="UTF-8",
    )
    locale.chmod(0o755)
    print(f"Created {locale}")

    cfg.env["PATH"] = str(locale.parent) + ":" + cfg.env["PATH"]

    print("Running 'locale -a'")
    subprocess.run(["locale", "-a"], check=True, env=cfg.env)

    print("Checking the output of 'locale -a'")
    lines = subprocess.check_output(["locale", "-a"], encoding="UTF-8", env=cfg.env).splitlines()
    if lines != cfg.data.locales:
        sys.exit(f"Bad 'locale -a' output: expected {cfg.data.locales!r}, got {lines!r}")
    if "C.UTF-8" not in lines:
        sys.exit(f"Bad 'locale -a' output: expected 'C.UTF-8' in {lines!r}")

    print("Running 'locale', expecting it to fail")
    rcode = subprocess.run(["locale"], check=False, env=cfg.env).returncode
    if rcode != 61:
        sys.exit(f"'locale' exited with code {rcode}, expected 61")


def test_u8loc(
    cfg: Config,
    args: List[str],
    expected: List[List[str]],
    *,
    env_add: Optional[Dict[str, str]] = None,
) -> None:
    """Run u8loc with the specified arguments, check its output against the expected one."""
    exp_lines = " or ".join(map(str, sorted(map(len, expected)))) + " line"
    if len(expected) != 1 or len(expected[0]) != 1:
        exp_lines += "s"
    print(
        f"Running {cfg.program} with arguments '{' '.join(args)}', "
        f"expecting {exp_lines} of output"
    )

    if env_add is None:
        env = cfg.env
    else:
        env = dict(cfg.env)
        env.update(env_add)
    lines = subprocess.check_output(
        [str(cfg.program)] + args, encoding="UTF-8", env=env
    ).splitlines()
    if lines not in expected:
        sys.exit(f"Expected {expected!r}, got {lines!r}")


def test_printenv(cfg: Config, features: Dict[str, str], test_case: TestDetect) -> None:
    """Run `printenv LC_ALL LANGUAGE` via u8loc."""
    if "run" not in features:
        print("SKIPPING the printenv test, 'run' not in the features list")
        return

    test_u8loc(
        cfg,
        (["-p"] if test_case.preferred else []) + ["-r", "--", "printenv", "LC_ALL", "LANGUAGE"],
        [[test_case.expected, ""]],
        env_add=test_case.env_add,
    )


def test_query(cfg: Config, features: Dict[str, str], test_case: TestDetect) -> None:
    """Run `u8loc -q LC_ALL` and `u8loc -q LANGUAGE`."""
    if "query-env" in features:
        test_u8loc(
            cfg,
            (["-p"] if test_case.preferred else []) + ["-q", "LC_ALL"],
            [[test_case.expected]],
            env_add=test_case.env_add,
        )
        test_u8loc(
            cfg,
            (["-p"] if test_case.preferred else []) + ["-q", "LANGUAGE"],
            [[""]],
            env_add=test_case.env_add,
        )
    else:
        print("SKIPPING the -q LC_ALL and LANGUAGE tests, 'query-env' not in the features list")

    if "query-preferred" in features:
        test_u8loc(
            cfg,
            (["-p"] if test_case.preferred else []) + ["-q", "preferred"],
            [test_case.expected_preferred],
            env_add=test_case.env_add,
        )
    else:
        print("SKIPPING the -q preferred test, 'query-preferred' not in the features list")


def test_query_list(cfg: Config, features: Dict[str, str]) -> None:
    """Make sure `u8loc -q list` returns the expected list."""
    expected = set(["list"])
    if "query-env" in features:
        expected.update(["LC_ALL", "LANGUAGE"])
    if "query-preferred" in features:
        expected.add("preferred")
    print(f"Running {cfg.program} -q list, expecting {len(expected)} lines of output")

    lines = subprocess.check_output(
        [str(cfg.program), "-q", "list"], encoding="UTF-8", env=cfg.env
    ).splitlines()
    words = [line.split()[0] for line in lines]
    if set(words) != expected:
        sys.exit(f"Unexpected `-q list` output: {lines!r}")


def obtain_features(cfg: Config) -> Dict[str, str]:
    """Obtain the list of features supported by the u8loc tool."""
    return feature_check.obtain_features(str(cfg.program))


def main() -> None:
    """Main program: parse command-line arguments, run some tests."""
    cfg = parse_args()
    with tempfile.TemporaryDirectory() as tempd_obj:
        tempd = pathlib.Path(tempd_obj)
        print(f"Using {tempd} as a temporary directory")

        create_locale_tool(cfg, tempd)

        features = obtain_features(cfg)

        test_query_list(cfg, features)

        for test_case in DETECT_CASES:
            test_printenv(cfg, features, test_case)
            test_query(cfg, features, test_case)


if __name__ == "__main__":
    main()
