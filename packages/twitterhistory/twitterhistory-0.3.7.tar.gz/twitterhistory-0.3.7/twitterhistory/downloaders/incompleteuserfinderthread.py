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


"""Search for incomplete user records."""


__all__ = ["IncompleteUserFinderThread"]


import sqlalchemy
import sqlalchemy.sql.expression

from .incompletedatafinderthread import IncompleteDataFinderThread
from ..database.models import User


class IncompleteUserFinderThread(IncompleteDataFinderThread):
    """Search for incomplete tweets."""

    _sqlquery = (
        sqlalchemy
        .select(User.id)
        .where(
            sqlalchemy.sql.expression.or_(
                User.username == None,  # noqa: E711
                User.name == None,  # noqa: E711
                User.followers_count == None,  # noqa: E711
                User.following_count == None,  # noqa: E711
                User.tweet_count == None,  # noqa: E711
                User.listed_count == None  # noqa: E711
            )
        )
    )
