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

"""A Tweet ORM data model."""


__all__ = ["Tweet"]


import dataclasses

import geoalchemy2
import sqlalchemy
import sqlalchemy.orm

from .base import Base

from ...integer_hash import integer_hash


# https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet


@dataclasses.dataclass
class TweetReferenceType(Base):
    """A media type ORM data model."""

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    reference_type = sqlalchemy.Column(sqlalchemy.Text, unique=True)


@dataclasses.dataclass
class TweetReference(Base):  # ‘Association Object’ in sqlalchemy terminology
    """An ORM model to represent the relationship between two tweets."""

    referenced_tweet_id = sqlalchemy.Column(
        sqlalchemy.BigInteger,
        sqlalchemy.ForeignKey("tweets.id"),
        primary_key=True
    )
    referenced_tweet = sqlalchemy.orm.relationship(
        "Tweet",
        foreign_keys=[referenced_tweet_id],
        back_populates="referencing_tweets"
    )

    referencing_tweet_id = sqlalchemy.Column(
        sqlalchemy.BigInteger,
        sqlalchemy.ForeignKey("tweets.id"),
        primary_key=True
    )
    referencing_tweet = sqlalchemy.orm.relationship(
        "Tweet",
        foreign_keys=[referencing_tweet_id],
        back_populates="referenced_tweets"
    )

    reference_type_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("tweet_reference_types.id"),
        primary_key=True
    )
    reference_type = sqlalchemy.orm.relationship("TweetReferenceType")


@dataclasses.dataclass
class Tweet(Base):
    """A Tweet ORM data model."""

    id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime(timezone=True), index=True)
    possibly_sensitive = sqlalchemy.Column(sqlalchemy.Boolean)
    text = sqlalchemy.Column(sqlalchemy.Text)

    geom = sqlalchemy.Column(geoalchemy2.Geometry("POINT", 4326))

    author_id = sqlalchemy.Column(
        sqlalchemy.BigInteger,
        sqlalchemy.ForeignKey("users.id"),
        index=True
    )
    author = sqlalchemy.orm.relationship(
        "User", back_populates="tweets", foreign_keys=[author_id]
    )

    in_reply_to_user_id = sqlalchemy.Column(
        sqlalchemy.BigInteger, sqlalchemy.ForeignKey("users.id")
    )
    in_reply_to = sqlalchemy.orm.relationship(
        "User", foreign_keys=[in_reply_to_user_id]
    )

    conversation_id = sqlalchemy.Column(
        sqlalchemy.BigInteger,
        sqlalchemy.ForeignKey("conversations.id"),
        index=True
    )
    conversation = sqlalchemy.orm.relationship("Conversation", back_populates="tweets")

    language_language = sqlalchemy.Column(
        sqlalchemy.Text,
        sqlalchemy.ForeignKey("languages.language"),
        index=True
    )
    language = sqlalchemy.orm.relationship("Language", back_populates="tweets")

    like_count = sqlalchemy.Column(sqlalchemy.BigInteger)

    liked_by = sqlalchemy.orm.relationship(
        "User", secondary="likes", back_populates="likes"
    )

    place_id = sqlalchemy.Column(
        sqlalchemy.Text,
        sqlalchemy.ForeignKey("places.id"),
        index=True
    )
    place = sqlalchemy.orm.relationship("Place", back_populates="tweets")

    quote_count = sqlalchemy.Column(sqlalchemy.BigInteger)

    referenced_tweets = sqlalchemy.orm.relationship(
        "TweetReference",
        primaryjoin="(Tweet.id==TweetReference.referencing_tweet_id)",
        back_populates="referencing_tweet",
    )
    referencing_tweets = sqlalchemy.orm.relationship(
        "TweetReference",
        primaryjoin="(Tweet.id==TweetReference.referenced_tweet_id)",
        back_populates="referenced_tweet",
    )

    reply_count = sqlalchemy.Column(sqlalchemy.BigInteger)

    retweet_count = sqlalchemy.Column(sqlalchemy.BigInteger)

    hashtags = sqlalchemy.orm.relationship(
        "Hashtag", secondary="hashtag_tweet_associations", back_populates="tweets"
    )
    media = sqlalchemy.orm.relationship(
        "MediaItem", secondary="media_item_tweet_associations", back_populates="tweets"
    )
    mentions = sqlalchemy.orm.relationship(
        "User", secondary="mentions", back_populates="mentioned"
    )
    urls = sqlalchemy.orm.relationship(
        "Url", secondary="url_tweet_associations", back_populates="tweets"
    )

    search_terms = sqlalchemy.orm.relationship(
        "SearchTerm",
        secondary="search_term_tweet_associations",
        back_populates="tweets"
    )

    @classmethod
    def _pseudonymise_api_data(cls, data):
        for identifier in [
            "id",
            "author_id",
            "in_reply_to_user_id",
            "conservation_id",
        ]:
            try:
                data[identifier] = integer_hash(data[identifier])
            except KeyError:
                pass

        if "referenced_tweets" in data:
            for i in range(len(data["referenced_tweets"])):
                data["referenced_tweets"][i]["id"] = integer_hash(
                    data["referenced_tweets"][i]["id"]
                )

        for identifier in []:
            data[identifier] = None

        return data
