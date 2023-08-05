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

"""Test the full tox_delay operation."""

import os
import pathlib
import sys
import tempfile

from unittest import mock

from typing import Any, List  # noqa: H301

from tox_delay import __main__ as tmain


TOX_INI = """
[tox]
envlist =
  nothing
  to see here
  move along
"""


def run_test_mock(parallel: bool) -> None:
    """Run tox_delay, mocking the actual Tox execution."""

    invoked: List[str] = []

    def mock_check_call(*args: List[str], **kwargs: Any) -> None:
        """See what happens."""
        print(f"check_call: args {args!r}")
        print(f"check_call: kwargs {kwargs!r}")

        if not invoked:
            assert args[0] == [sys.executable, "-m", "tox"] + (
                ["-p", "all"] if parallel else []
            ) + ["--", "-k", "chosen"]
            assert kwargs["env"]["TOX_SKIP_ENV"] == "^second|fou\\$rth\\.$"
            invoked.append("skipped")
        elif len(invoked) == 1:
            assert args[0] == [
                sys.executable,
                "-m",
                "tox",
                "-e",
                "second,fou$rth.",
                "--",
                "-k",
                "chosen",
            ]
            assert "env" not in kwargs
            invoked.append("real")
        else:
            raise Exception("why a third time?")

    with tempfile.TemporaryDirectory() as tempd_obj:
        tempd = pathlib.Path(tempd_obj)
        try:
            os.chdir(tempd)
            (tempd / "tox.ini").write_text(TOX_INI, encoding="UTF-8")
            with mock.patch.object(
                sys,
                "argv",
                new=["tox_delay", "-e", "second,fou$rth."]
                + (["-p", "all"] if parallel else [])
                + ["--", "--", "-k", "chosen"],
            ):
                with mock.patch("subprocess.check_call", new=mock_check_call):
                    tmain.main()
        finally:
            os.chdir("/")

    assert invoked == ["skipped", "real"]


def test_mock_non_parallel() -> None:
    """Run tox_delay without -p, but with some arguments."""
    run_test_mock(False)


def test_mock_parallel() -> None:
    """Run tox_delay with -p and with some arguments."""
    run_test_mock(True)
