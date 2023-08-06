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

"""A Twitter Url ORM data model."""


__all__ = ["Url"]


import dataclasses

import sqlalchemy
import sqlalchemy.orm

from .base import Base


@dataclasses.dataclass
class Url(Base):
    """A url ORM data model."""

    id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
    url = sqlalchemy.Column(sqlalchemy.Text, unique=True, index=True)
    tweets = sqlalchemy.orm.relationship(
        "Tweet", secondary="url_tweet_associations", back_populates="urls"
    )
    users = sqlalchemy.orm.relationship(
        "User", secondary="url_user_associations", back_populates="urls"
    )


class UrlTweetAssociation(Base):
    """A many-to-many relation table between URLs and tweets."""

    url_id = sqlalchemy.Column(
        sqlalchemy.BigInteger, sqlalchemy.ForeignKey("urls.id"), primary_key=True
    )
    tweet_id = sqlalchemy.Column(
        sqlalchemy.BigInteger, sqlalchemy.ForeignKey("tweets.id"), primary_key=True
    )


class UrlUserAssociation(Base):
    """A many-to-many relation table between URLs and users."""

    url_id = sqlalchemy.Column(
        sqlalchemy.BigInteger, sqlalchemy.ForeignKey("urls.id"), primary_key=True
    )
    user_id = sqlalchemy.Column(
        sqlalchemy.BigInteger, sqlalchemy.ForeignKey("users.id"), primary_key=True
    )
