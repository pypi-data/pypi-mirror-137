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

"""Run tox-delay from a temporary directory, examine its output."""

import argparse
import os
import pathlib
import subprocess
import sys
import tempfile

from typing import Dict, List, NamedTuple, Optional, Tuple  # noqa: H301

import feature_check
import utf8_locale


TOX_ENVLIST = [
    ("fou$rth.", "fourth"),
    ("second", "second"),
    ("first", "first"),
    ("third", "third"),
]

TOX_ENVLIST_ORDERED = [TOX_ENVLIST[2], TOX_ENVLIST[1], TOX_ENVLIST[3], TOX_ENVLIST[0]]
assert len(TOX_ENVLIST_ORDERED) == len(TOX_ENVLIST)

TOX_INI = (
    """
[tox]
skipsdist = True
envlist =
"""
    + "\n".join(f"  {name}" for name, _ in TOX_ENVLIST_ORDERED)
    + "".join(
        f"""
[testenv:{name}]
commands =
  python3 -c 'import sys; lst=["{tag}"] + sys.argv[1:] + ["thing-marker"]; print(" ".join(lst))' {{posargs}}
  """  # noqa: E501  # pylint: disable=line-too-long
        for name, tag in TOX_ENVLIST_ORDERED
    )
)


class Config(NamedTuple):
    """Runtime configuration for the tox-delay functional test."""

    executable: Optional[pathlib.Path]
    python: pathlib.Path
    python_env: Dict[str, str]
    utf8_env: Dict[str, str]


def parse_args() -> Config:
    """Parse the command-line options."""

    def validate_python_path(python_path: str) -> str:
        """Split into components, make them absolute paths."""
        components = []
        for comp in python_path.split(":"):
            if not comp:
                sys.exit("No empty strings allowed in the Python path for now")
            path = pathlib.Path(comp).absolute()
            if not path.exists():
                sys.exit(
                    f"No non-existent components like {path!r} allowed in the Python path for now"
                )
            components.append(path)

        return ":".join(map(str, components))

    parser = argparse.ArgumentParser(prog="tox-delay-functional-test")
    parser.add_argument(
        "-e",
        "--executable",
        type=str,
        help="the program executable to run instead of python3 -m tox_delay",
    )
    parser.add_argument(
        "-p", "--python", type=str, default="python3", help="the Python interpreter to use"
    )
    parser.add_argument(
        "-P",
        "--python-path",
        type=str,
        help="paths, if any, to prepend to PYTHONPATH to find tox-delay",
    )

    args = parser.parse_args()

    utf8_env = utf8_locale.get_utf8_env()
    print(f"Using UTF-8 settings: LC_ALL {utf8_env['LC_ALL']!r} LANGUAGE {utf8_env['LANGUAGE']!r}")

    executable = None if args.executable is None else pathlib.Path(args.executable).absolute()
    if executable is not None:
        if not executable.is_file() or not os.access(executable, os.X_OK):
            sys.exit(f"Not an executable file: {executable}")

    python = args.python
    print(f"Trying to find the absolute path to the {python} Python interpreter")
    lines = subprocess.check_output(
        [python, "-c", "import sys; print(sys.executable)"], encoding="UTF-8", env=utf8_env
    ).splitlines()
    if len(lines) != 1:
        sys.exit(f"Unexpected output from 'print sys.executable': {lines!r}")
    ppython = pathlib.Path(lines[0])
    if not ppython.is_absolute() or not ppython.is_file() or not os.access(ppython, os.X_OK):
        sys.exit(f"Not an absolute path to an executable file: {ppython!r}")

    python_env = dict(utf8_env)
    if args.python_path is not None:
        python_path = validate_python_path(args.python_path)
        print(f"Converted {args.python_path!r} into {python_path!r}")

        curpath = python_env.get("PYTHONPATH")
        if curpath is None:
            print("Using it as it is")
            python_env["PYTHONPATH"] = python_path
        else:
            print(f"Combining it with {curpath!r}")
            python_env["PYTHONPATH"] = ":".join((python_path, curpath))

    if "PYTHONPATH" in python_env:
        print(f"Using {python_env.get('PYTHONPATH')!r} as PYTHONPATH")
    else:
        print("Apparently there is no need to set PYTHONPATH at all")

    return Config(executable=executable, python=ppython, python_env=python_env, utf8_env=utf8_env)


def check_tox_delay_features(cfg: Config, tempd: pathlib.Path) -> None:
    """Run `tox-delay --features`, look for a tox-delay one."""

    def get_executable() -> pathlib.Path:
        """Make sure we have a single program to run."""
        if cfg.executable is not None:
            return cfg.executable

        path = tempd / "tdelay"
        print(f"Creating a {path} shell script")

        if "PYTHONPATH" in cfg.python_env:
            python_env = f"env PYTHONPATH='{cfg.python_env['PYTHONPATH']}'"
        else:
            python_env = ""

        path.write_text(
            f"""#!/bin/sh

exec {python_env} '{cfg.python}' -m tox_delay "$@"
""",
            encoding="UTF-8",
        )
        path.chmod(0o755)
        return path

    tdelay = get_executable()
    features = feature_check.obtain_features(str(tdelay))
    tdver = features.get("tox-delay")
    print(f"Got a tox-delay feature version {tdver!r}")
    if tdver is None:
        sys.exit("tox-delay did not report a 'tox-delay' feature")
    if not tdver.startswith("0.1."):
        sys.exit("tox-delay did not report a 'tox-delay' feature with a supported version")


def create_tox_ini(tempd: pathlib.Path) -> None:
    """Create the tox.ini file and show what we did there."""
    path = tempd / "tox.ini"
    path.write_text(TOX_INI, encoding="UTF-8")
    print(f"Wrote something to {path}:")
    print(path.read_text(encoding="UTF-8"))


def check_tox_output(
    cfg: Config,
    tempd: pathlib.Path,
    tox: str,
    envlist: List[Tuple[str, str]],
    *,
    order: Optional[List[Tuple[str, str]]] = None,
    parallel: bool = False,
) -> None:
    """Run tox or tox-delay, check its output."""

    envstr = ",".join(item[0] for item in envlist)
    if tox == "tox" or cfg.executable is None:
        tox_cmd = [str(cfg.python), "-m", tox]
        tox_env = cfg.python_env
    else:
        tox_cmd = [str(cfg.executable)]
        tox_env = cfg.utf8_env

    def cmdline(args: Optional[List[str]] = None) -> List[str]:
        """Build the command line to test."""
        return (
            tox_cmd
            + ["-e", envstr]
            + (["-p", "all"] if parallel else [])
            + (["--"] + args if args is not None else [])
        )

    def check_output(args: Optional[List[str]] = None) -> None:
        """Run the command and check its output."""
        print(
            f"\nRunning {tox} for {envstr}"
            + (" with arguments" if args is not None else "")
            + (" in parallel" if parallel else "")
            + " and examining its output\n"
        )
        cmd = cmdline(args)
        print(cmd)
        lines = subprocess.check_output(cmd, cwd=tempd, encoding="UTF-8", env=tox_env).splitlines()
        found = [line for line in lines if line.endswith(" thing-marker")]
        template = ([] if args is None else args) + ["thing-marker"]
        expected = [
            " ".join([item[1]] + template)
            for item in (envlist if order is None or parallel else order)
        ]
        if found != expected:
            sys.exit(f"Unexpected tox -e {envstr} output: found {found!r} expected {expected!r}")

    posargs = ["this", "and that"]

    print(f"\nRunning {tox} for {envstr} without output capturing\n")
    subprocess.run(
        cmdline(),
        check=True,
        cwd=tempd,
        env=tox_env,
    )
    subprocess.run(
        cmdline(posargs),
        check=True,
        cwd=tempd,
        env=tox_env,
    )

    check_output()
    check_output(posargs)


def test_real_tox(cfg: Config, tempd: pathlib.Path) -> None:
    """Test a couple of actual Tox invocations."""
    print("Making sure Tox itself works")
    check_tox_output(cfg, tempd, "tox", TOX_ENVLIST)


def test_tox_delay(cfg: Config, tempd: pathlib.Path, parallel: bool) -> None:
    """Test a real tox-delay invocation."""
    print(f"Testing tox-delay in {'' if parallel else 'non-'}parallel mode")

    print("Let's see if it can run *all* the environments first")
    check_tox_output(cfg, tempd, "tox_delay", TOX_ENVLIST)

    print("Now let us delay some")
    check_tox_output(
        cfg,
        tempd,
        "tox_delay",
        TOX_ENVLIST_ORDERED[1:3],
        order=[
            TOX_ENVLIST_ORDERED[0],
            TOX_ENVLIST_ORDERED[3],
            TOX_ENVLIST_ORDERED[1],
            TOX_ENVLIST_ORDERED[2],
        ],
        parallel=parallel,
    )

    print("Let us delay others")
    check_tox_output(
        cfg,
        tempd,
        "tox_delay",
        [TOX_ENVLIST_ORDERED[2]],
        order=[
            TOX_ENVLIST_ORDERED[0],
            TOX_ENVLIST_ORDERED[1],
            TOX_ENVLIST_ORDERED[3],
            TOX_ENVLIST_ORDERED[2],
        ],
        parallel=parallel,
    )


def main() -> None:
    """Main program: parse command-line options, run things."""
    cfg = parse_args()

    with tempfile.TemporaryDirectory() as tempd_obj:
        tempd = pathlib.Path(tempd_obj)
        print(f"Using {tempd} as a temporary directory")

        check_tox_delay_features(cfg, tempd)
        create_tox_ini(tempd)

        test_real_tox(cfg, tempd)

        test_tox_delay(cfg, tempd, False)
        test_tox_delay(cfg, tempd, True)

        print("Seems fine")


if __name__ == "__main__":
    main()
