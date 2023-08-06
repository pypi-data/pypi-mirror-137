#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#   Copyright (C) 2020 Christoph Fink, University of Helsinki
#
#   This program is free software; you can redistribute it and/or
#   modify it under the terms of the GNU General Public License
#   as published by the Free Software Foundation; either version 3
#   of the License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, see <http://www.gnu.org/licenses/>.


"""Return a BLAKE2 hash of data, in integer representation."""


__all__ = ["integer_hash"]


import hashlib


def integer_hash(data):
    """Return a BLAKE2 hash of data, in integer representation."""
    if not isinstance(data, str):
        data = str(data)
    return int.from_bytes(
        hashlib.blake2b(data.encode("UTF-8"), digest_size=7).digest(), "big"
    )
