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


"""Search for tweets that have no likes recorded."""


__all__ = ["TweetsWithoutLikesFinderThread"]


import sqlalchemy
import sqlalchemy.sql.expression

from .incompletedatafinderthread import IncompleteDataFinderThread
from ..database.models import Tweet


class TweetsWithoutLikesFinderThread(IncompleteDataFinderThread):
    """Search for tweets that have no likes recorded."""

    # The query below selects the `id` of Tweets that have a
    # like_count > 0, but do not have any `liked_by` relationship

    _sqlquery = (
        sqlalchemy
        .select(Tweet.id)
        .where(
            sqlalchemy.sql.expression.and_(
                Tweet.like_count > 0,
                sqlalchemy.sql.expression.not_(
                    Tweet.liked_by.any()
                )
            )
        )
    )
