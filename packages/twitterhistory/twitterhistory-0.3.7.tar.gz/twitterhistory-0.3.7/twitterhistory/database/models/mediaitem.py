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

"""A Twitter MediaItem ORM data model."""


__all__ = ["MediaItem"]


import dataclasses

import sqlalchemy
import sqlalchemy.orm

from .base import Base


# https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/media


@dataclasses.dataclass
class MediaType(Base):
    """A media type ORM data model."""

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    media_type = sqlalchemy.Column(sqlalchemy.Text, unique=True)
    media_items = sqlalchemy.orm.relationship("MediaItem")


@dataclasses.dataclass
class MediaItem(Base):
    """A Twitter MediaItem ORM data model."""

    media_key = sqlalchemy.Column(sqlalchemy.Text, primary_key=True)
    url = sqlalchemy.Column(sqlalchemy.Text)
    media_type_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("media_types.id"),
        index=True
    )
    media_type = sqlalchemy.orm.relationship("MediaType", back_populates="media_items")

    tweets = sqlalchemy.orm.relationship(
        "Tweet", secondary="media_item_tweet_associations", back_populates="media"
    )


class MediaItemTweetAssociation(Base):
    """A many-to-many relation table between media items and tweets."""

    media_item_media_key = sqlalchemy.Column(
        sqlalchemy.Text,
        sqlalchemy.ForeignKey("media_items.media_key"),
        primary_key=True,
    )
    tweet_id = sqlalchemy.Column(
        sqlalchemy.BigInteger,
        sqlalchemy.ForeignKey("tweets.id"),
        primary_key=True
    )
