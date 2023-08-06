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

"""ORM models for Twitter entities."""


__all__ = [
    "Conversation",
    "Country",
    "Hashtag",
    "Language",
    "MediaItem",
    "MediaType",
    "Place",
    "PlaceType",
    "SearchTerm",
    "Tweet",
    "TweetReference",
    "TweetReferenceType",
    "Url",
    "User",
]


import sqlalchemy

from .conversation import Conversation
from .hashtag import Hashtag
from .language import Language
from .mediaitem import MediaItem, MediaType
from .place import Country, Place, PlaceType
from ..databaseschemaupdater import DatabaseSchemaUpdater
from .searchterm import SearchTerm
from .tweet import Tweet, TweetReference, TweetReferenceType
from .url import Url
from .user import User

from ..engine import engine
from .base import Base


if sqlalchemy.inspect(engine).has_table(Tweet.__table__):  # DATA_EXISTS
    DatabaseSchemaUpdater().update_to_latest()
else:
    Base.metadata.create_all(engine)
    DatabaseSchemaUpdater().set_schema_version(DatabaseSchemaUpdater.LATEST)
