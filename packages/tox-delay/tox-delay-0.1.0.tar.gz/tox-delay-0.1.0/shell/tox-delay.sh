#!/bin/sh
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

set -e

tox_delay_version='0.1.0'

version()
{
	echo "tox-delay $tox_delay_version"
}

usage()
{
	cat <<'EOUSAGE'
Usage:	tox-delay [-p value] -e envlist -- [tox options]
	tox-delay --features | -h | --help | -V | --version

	-e	specify the list of environments to delay the run for
	-h	display program usage information and exit
	-p	run the first batch of environments in parallel
	-V	display program version information and exit

	--features	display the list of supported features
EOUSAGE
}

features()
{
	echo "Features: tox-delay=$tox_delay_version parallel=1.0"
}

escape_name()
{
	local name="$1"

	printf -- '%s\n' "$name" | sed -Ee 's/[^A-Za-z0-9_-]/\\&/g'
}

build_escaped_envlist()
{
	local envlist="$1" res='^('

	while :; do
		local comp="${envlist%%,*}" rest="${envlist#*,}"
		if [ "$comp" = "$envlist" ]; then
			break
		fi
		envlist="$rest"

		if [ -z "$comp" ]; then
			echo 'Empty environment name in the envlist' 1>&2
			exit 1
		fi
		res="$res$(escape_name "$comp")|"
	done

	res="$res$(escape_name "$envlist"))\$"
	printf -- '%s\n' "$res"
}

unset show_features show_help show_version envlist parallel

while getopts 'e:hp:V-:' o; do
	case "$o" in
		e)
			envlist="$OPTARG"
			;;

		h)
			show_help=1
			;;

		p)
			parallel="$OPTARG"
			;;

		V)
			show_version=1
			;;

		-)
			case "$OPTARG" in
				features)
					show_features=1
					;;

				help)
					show_help=1
					;;

				version)
					show_version=1
					;;

				*)
					echo "Unrecognized long option '--$OPTARG'" 1>&2
					usage 1>&2
					exit 1
					;;
			esac
			;;

		*)
			usage 1>&2
			exit 1
			;;
	esac
done

shift $((OPTIND - 1))

[ -z "$show_version" ] || version
[ -z "$show_features" ] || features
[ -z "$show_help" ] || usage
[ -z "$show_version$show_features$show_help" ] || exit 0

if [ -z "$envlist" ]; then
	echo 'No environments specified (-e/--envlist)' 1>&2
	exit 1
fi

escaped="$(build_escaped_envlist "$envlist")"
env TOX_SKIP_ENV="$escaped" tox ${parallel+-p "$parallel"} "$@"

tox -e "$envlist" "$@"
