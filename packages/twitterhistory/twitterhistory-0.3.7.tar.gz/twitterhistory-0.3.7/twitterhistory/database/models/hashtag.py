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

"""A Twitter Hashtag ORM data model."""


__all__ = ["Hashtag"]


import dataclasses

import sqlalchemy
import sqlalchemy.orm

from .base import Base


@dataclasses.dataclass
class Hashtag(Base):
    """A hashtag ORM data model."""

    hashtag = sqlalchemy.Column(sqlalchemy.Text, primary_key=True)
    tweets = sqlalchemy.orm.relationship(
        "Tweet", secondary="hashtag_tweet_associations", back_populates="hashtags"
    )
    users = sqlalchemy.orm.relationship(
        "User", secondary="hashtag_user_associations", back_populates="hashtags"
    )


class HashtagTweetAssociation(Base):
    """A many-to-many relation table between hashtags and tweets."""

    hashtag_hashtag = sqlalchemy.Column(
        sqlalchemy.Text, sqlalchemy.ForeignKey("hashtags.hashtag"), primary_key=True
    )
    # hashtag = sqlalchemy.orm.relationship("Hashtag", back_populates="tweets")
    tweet_id = sqlalchemy.Column(
        sqlalchemy.BigInteger, sqlalchemy.ForeignKey("tweets.id"), primary_key=True
    )
    # tweet = sqlalchemy.orm.relationship("Tweet", back_populates="hashtags")


class HashtagUserAssociation(Base):
    """A many-to-many relation table between hashtags and users."""

    hashtag_hashtag = sqlalchemy.Column(
        sqlalchemy.Text, sqlalchemy.ForeignKey("hashtags.hashtag"), primary_key=True
    )
    # hashtag = sqlalchemy.orm.relationship("Hashtag", back_populates="users")
    user_id = sqlalchemy.Column(
        sqlalchemy.BigInteger, sqlalchemy.ForeignKey("users.id"), primary_key=True
    )
    # user = sqlalchemy.orm.relationship("User", back_populates="hashtags")
