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

"""Detect a UTF-8-capable locale for running child processes in.

Sometimes it is useful for a program to be able to run a child process and
more or less depend on its output being valid UTF-8. This can usually be
accomplished by setting one or more environment variables, but there is
the question of what to set them to - what UTF-8-capable locale is present
on this particular system? This is where the `utf8_locale` module comes in.
"""

from .detect import (
    VERSION,  # noqa: H301
    UTF8_LANGUAGES,
    UTF8_ENCODINGS,
    LOCALE_VARIABLES,
    detect_utf8_locale,
    get_preferred_languages,
    get_utf8_env,
    get_utf8_vars,
)

__all__ = [
    "VERSION",
    "UTF8_LANGUAGES",
    "UTF8_ENCODINGS",
    "LOCALE_VARIABLES",
    "detect_utf8_locale",
    "get_preferred_languages",
    "get_utf8_env",
    "get_utf8_vars",
]
