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
"""The u8loc command-line tool."""

import argparse
import dataclasses
import os
import sys

from typing import Callable, Dict, List, NamedTuple  # noqa: H301

from . import detect


@dataclasses.dataclass(frozen=True)
class Config:
    """Runtime configuration for the u8loc command-line tool."""

    preferred: bool


@dataclasses.dataclass(frozen=True)
class QueryConfig(Config):
    """Runtime configuration for `u8loc -q variable`."""

    query: str


@dataclasses.dataclass(frozen=True)
class RunConfig(Config):
    """Runtime configuration for `u8loc -r program [arg...]`."""

    run_program: List[str]


class QueryDef(NamedTuple):
    """A parameter for the -q option."""

    name: str
    early: bool
    handler: Callable[[QueryConfig, Dict[str, str]], None]
    descr: str


def query_env(cfg: QueryConfig, env: Dict[str, str]) -> None:
    """Output the value of an environment variable."""
    value = env.get(cfg.query)
    if value is None:
        sys.exit(f"Internal error: query_env(): no value for {cfg.query!r} in {env!r}")

    print(value)


def query_list(_cfg: QueryConfig, _env: Dict[str, str]) -> None:
    """List the available query options."""
    for qdef in sorted(QUERY_HANDLERS_LIST):
        print(f"{qdef.name:20s} - {qdef.descr}")


def query_preferred(_cfg: QueryConfig, _env: Dict[str, str]) -> None:
    """Display the list of preferred languages as per the locale variables."""
    print("\n".join(detect.get_preferred_languages()))


QUERY_HANDLERS_LIST = [
    QueryDef(
        name="LC_ALL", early=False, handler=query_env, descr="The LC_ALL environment variable"
    ),
    QueryDef(
        name="LANGUAGE", early=False, handler=query_env, descr="The LANGUAGE environment variable"
    ),
    QueryDef(
        name="list", early=True, handler=query_list, descr="List the available query parameters"
    ),
    QueryDef(
        name="preferred",
        early=True,
        handler=query_preferred,
        descr="List the preferred languages as per the locale variables",
    ),
]

QUERY_HANDLERS = {qdef.name: qdef for qdef in QUERY_HANDLERS_LIST}


def parse_args() -> Config:
    """Parse the u8loc tool's command-line options."""
    parser = argparse.ArgumentParser(prog="u8loc")
    parser.add_argument(
        "-p",
        dest="preferred",
        action="store_true",
        help="use a locale specified in the LANG and LC_* variables if appropriate",
    )
    parser.add_argument(
        "-q",
        dest="query",
        type=str,
        choices=sorted(QUERY_HANDLERS.keys()),
        help="output the value of an environment variable",
    )
    parser.add_argument(
        "-r",
        dest="run",
        action="store_true",
        help="run the specified program in a UTF-8-friendly environment",
    )
    parser.add_argument(
        "--features",
        action="store_true",
        help="display the features supported by the program and exit",
    )
    parser.add_argument(
        "program", type=str, nargs="*", help="the program to run if -r is specified"
    )

    args = parser.parse_args()

    if args.features:
        print(f"Features: u8loc={detect.VERSION} query-env=0.1 query-preferred=0.1 run=0.1")
        sys.exit(0)

    if int(args.query is not None) + int(args.run) != 1:
        sys.exit("Exactly one of -q or -r must be specified.")

    if args.query:
        return QueryConfig(preferred=args.preferred, query=args.query)

    if args.run:
        if not args.program:
            sys.exit("No program to run specified")
        return RunConfig(preferred=args.preferred, run_program=args.program)

    raise NotImplementedError(f"Did not expect to reach the end of parse_args() with {args!r}")


def main() -> None:
    """The main routine for the u8loc command-line tool."""
    cfg = parse_args()

    if isinstance(cfg, QueryConfig) and QUERY_HANDLERS[cfg.query].early:
        QUERY_HANDLERS[cfg.query].handler(cfg, {})
        return

    try:
        env = detect.get_utf8_env(
            languages=detect.get_preferred_languages() if cfg.preferred else detect.UTF8_LANGUAGES
        )
    except Exception as err:  # pylint: disable=broad-except
        sys.exit(f"Could not determine an appropriate UTF-8 locale: {err}")

    if isinstance(cfg, RunConfig):
        try:
            os.execvpe(cfg.run_program[0], cfg.run_program, env)
        except Exception as err:  # pylint: disable=broad-except
            sys.exit(f"Could not run '{' '.join(cfg.run_program)}': {err}")

    if isinstance(cfg, QueryConfig):
        QUERY_HANDLERS[cfg.query].handler(cfg, env)
        return

    raise NotImplementedError(f"Did not expect to reach the end of main() with {cfg!r}")


if __name__ == "__main__":
    main()
