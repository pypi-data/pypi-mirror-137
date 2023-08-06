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

"""A Twitter User ORM data model."""


__all__ = ["User"]


import dataclasses

import sqlalchemy
import sqlalchemy.orm

from .base import Base

from ...integer_hash import integer_hash


# https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/place


class Mention(Base):
    """A many-to-many relation table between users and tweets representing mentions."""

    tweet_id = sqlalchemy.Column(
        sqlalchemy.BigInteger, sqlalchemy.ForeignKey("tweets.id"), primary_key=True
    )
    user_id = sqlalchemy.Column(
        sqlalchemy.BigInteger, sqlalchemy.ForeignKey("users.id"), primary_key=True
    )


class Like(Base):
    """A many-to-many relation table between tweets and users representing likes."""

    tweet_id = sqlalchemy.Column(
        sqlalchemy.BigInteger, sqlalchemy.ForeignKey("tweets.id"), primary_key=True
    )
    user_id = sqlalchemy.Column(
        sqlalchemy.BigInteger, sqlalchemy.ForeignKey("users.id"), primary_key=True
    )


# TODO: Like and Mention are basically identical, but inheriting one from the other
# resulted in an SqlAlchemy error:
#       raise exc.NoForeignKeysError(
#           sqlalchemy.exc.NoForeignKeysError: Can't find any foreign key
#           relationships between 'mentions' and 'likes'.
#       )
# How to refactor this in a sensible way?


@dataclasses.dataclass
class User(Base):
    """A Twitter User ORM data model."""

    id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
    username = sqlalchemy.Column(sqlalchemy.Text, index=True)
    name = sqlalchemy.Column(sqlalchemy.Text, index=True)
    description = sqlalchemy.Column(sqlalchemy.Text)
    location = sqlalchemy.Column(sqlalchemy.Text)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), index=True)

    protected = sqlalchemy.Column(sqlalchemy.Boolean)
    verified = sqlalchemy.Column(sqlalchemy.Boolean)

    pinned_tweet_id = sqlalchemy.Column(
        sqlalchemy.BigInteger, sqlalchemy.ForeignKey("tweets.id")
    )
    pinned_tweet = sqlalchemy.orm.relationship("Tweet", foreign_keys=[pinned_tweet_id])

    profile_image_url_id = sqlalchemy.Column(
        sqlalchemy.BigInteger, sqlalchemy.ForeignKey("urls.id")
    )
    profile_image_url = sqlalchemy.orm.relationship("Url")

    likes = sqlalchemy.orm.relationship(
        "Tweet", secondary="likes", back_populates="liked_by"
    )

    hashtags = sqlalchemy.orm.relationship(
        "Hashtag", secondary="hashtag_user_associations", back_populates="users"
    )
    urls = sqlalchemy.orm.relationship(
        "Url", secondary="url_user_associations", back_populates="users"
    )

    tweets = sqlalchemy.orm.relationship(
        "Tweet", back_populates="author", foreign_keys="[Tweet.author_id]"
    )

    mentioned = sqlalchemy.orm.relationship(
        "Tweet", secondary="mentions", back_populates="mentions"
    )

    followers_count = sqlalchemy.Column(sqlalchemy.BigInteger)
    following_count = sqlalchemy.Column(sqlalchemy.BigInteger)
    listed_count = sqlalchemy.Column(sqlalchemy.BigInteger)
    tweet_count = sqlalchemy.Column(sqlalchemy.BigInteger)

    @classmethod
    def _pseudonymise_api_data(cls, data):
        for identifier in [
            "id",
            "pinned_tweet_id",
        ]:
            try:
                data[identifier] = integer_hash(data[identifier])
            except KeyError:
                pass

        for identifier in [
            "username",
            "name",
            "description",
        ]:
            data[identifier] = None

        return data
