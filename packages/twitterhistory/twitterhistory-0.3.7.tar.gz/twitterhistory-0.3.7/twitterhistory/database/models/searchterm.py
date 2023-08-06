#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#   Copyright (C) 2019 Christoph Fink, University of Helsinki
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

"""A Twitter SearchTerm ORM data model."""


__all__ = ["SearchTerm"]


import dataclasses

import sqlalchemy
import sqlalchemy.orm

from .base import Base


@dataclasses.dataclass
class SearchTerm(Base):
    """A search_term ORM data model."""

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    search_term = sqlalchemy.Column(sqlalchemy.Text, unique=True)
    tweets = sqlalchemy.orm.relationship(
        "Tweet",
        secondary="search_term_tweet_associations",
        back_populates="search_terms"
    )


class SearchTermTweetAssociation(Base):
    """A many-to-many relation table between URLs and tweets."""

    search_term_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("search_terms.id"),
        primary_key=True,
    )
    tweet_id = sqlalchemy.Column(
        sqlalchemy.BigInteger,
        sqlalchemy.ForeignKey("tweets.id"),
        primary_key=True
    )

#    search_term = sqlalchemy.orm.relationship(
#        "SearchTerm",
#        back_populates="tweets"
#    )
#    tweet = sqlalchemy.orm.relationship(
#        "Tweet",
#        back_populates="search_terms"
#    )
