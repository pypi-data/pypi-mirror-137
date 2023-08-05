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

"""Run the specified tests after all the others."""

import argparse
import os
import re
import subprocess
import sys

from typing import List, NamedTuple, Optional  # noqa: H301


VERSION = "0.1.0"


class Config(NamedTuple):
    """Runtime configuration for the tox_delay tool."""

    envlist: List[str]
    parallel: Optional[str]
    tox_args: List[str]


def parse_args() -> Config:
    """Parse the command-line arguments."""
    parser = argparse.ArgumentParser(prog="tox_delay")
    parser.add_argument(
        "--features", action="store_true", help="display information about supported features"
    )
    parser.add_argument(
        "-p",
        "--parallel",
        type=str,
        help="environments to run in parallel (not the delayed ones)",
    )
    parser.add_argument(
        "-e",
        "--envlist",
        type=str,
        help="the environments to delay",
    )
    parser.add_argument(
        "tox_args",
        type=str,
        nargs="*",
        help="additional arguments to pass to both tox invocations",
    )

    args = parser.parse_args()

    if args.features:
        print(f"Features: tox-delay={VERSION} parallel=1.0")
        sys.exit(0)

    if args.envlist is None:
        sys.exit("No envlist specified (-e/--envlist)")

    return Config(
        envlist=args.envlist.split(","),
        parallel=args.parallel,
        tox_args=args.tox_args,
    )


def main() -> None:
    """Parse command-line arguments, do stuff."""
    cfg = parse_args()
    tox_cmd = [sys.executable, "-m", "tox"]

    skip_env = dict(os.environ)
    skip_env["TOX_SKIP_ENV"] = "^" + "|".join(re.escape(testenv) for testenv in cfg.envlist) + "$"
    parallel_opts = ["-p", cfg.parallel] if cfg.parallel is not None else []
    subprocess.check_call(tox_cmd + parallel_opts + cfg.tox_args, env=skip_env)

    env_opts = ["-e", ",".join(cfg.envlist)]
    subprocess.check_call(tox_cmd + env_opts + cfg.tox_args)


if __name__ == "__main__":
    main()
