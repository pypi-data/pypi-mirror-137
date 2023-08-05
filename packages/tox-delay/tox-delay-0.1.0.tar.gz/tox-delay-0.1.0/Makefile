#!/usr/bin/make
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

SH_PROG=	shell/tox-delay
SH_SRC=		shell/tox-delay.sh

MAN1=		tox-delay.1
MAN1GZ=		${MAN1}.gz

PYTHON3?=	python3

BINOWN?=	root
BINGRP?=	root
BINMODE?=	755

SHAREOWN?=	${BINOWN}
SHAREGRP?=	${BINGRP}
SHAREMODE?=	644

INSTALL_PROGRAM?=	install -o '${BINOWN}' -g '${BINGRP}' -m '${BINMODE}'
INSTALL_DATA?=		install -o '${SHAREOWN}' -g '${SHAREGRP}' -m '${SHAREMODE}'

LOCALBASE?=	/usr/local
PREFIX?=	${LOCALBASE}
BINDIR?=	${PREFIX}/bin
MANDIR?=	${PREFIX}/man/man
MAN1DIR?=	${MANDIR}1

all:		${SH_PROG} ${MAN1GZ}

install:	all
		mkdir -p -- '${DESTDIR}${BINDIR}'
		${INSTALL_PROGRAM} -- '${SH_PROG}' '${DESTDIR}${BINDIR}/'
		mkdir -p -- '${DESTDIR}${MAN1DIR}'
		${INSTALL_DATA} -- '${MAN1GZ}' '${DESTDIR}${MAN1DIR}/'

${SH_PROG}:	${SH_SRC}
		install -m 755 -- '${SH_SRC}' '${SH_PROG}'

${MAN1GZ}:	${MAN1}
		gzip -9cn -- '${MAN1}' > '${MAN1GZ}' || { rm -f -- '${MAN1GZ}'; false; }

clean:
		rm -f -- '${SH_PROG}' '${MAN1GZ}'

distclean:	clean
		rm -rf -- .mypy_cache .tox
		find python -type d \
			\( -name '__pycache__' -or -name '*.egg-info' \) \
			-exec rm -rf -- '{}' +

test-all:	test-shellcheck test-sh test-tox-delay

test-sh:	${SH_PROG}
		${PYTHON3} tests/functional.py -e '${SH_PROG}'

test-shellcheck:
		shellcheck -- '${SH_SRC}'

test-tox:
		${PYTHON3} -m tox

test-tox-delay:
		env PYTHONPATH="$${PYTHONPATH:+$$PYTHONPATH:}${CURDIR}/python" \
			${PYTHON3} -B -u -m tox_delay \
			-p all -e unit-tests,functional,functional-installed \
			-- -p all

.PHONY:		all install clean test-sh test-tox test-tox-delay
