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

"""A Twitter Place ORM data model."""


__all__ = ["Place"]


import dataclasses

import geoalchemy2
import sqlalchemy
import sqlalchemy.orm

from .base import Base


# https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/place


@dataclasses.dataclass
class PlaceType(Base):
    """A place type ORM data model."""

    id = sqlalchemy.Column(sqlalchemy.BigInteger, primary_key=True)
    place_type = sqlalchemy.Column(sqlalchemy.Text, unique=True)
    places = sqlalchemy.orm.relationship("Place")


@dataclasses.dataclass
class Country(Base):
    """A country ORM data model."""

    __tablename__ = "countries"  # override "countrys"

    name = sqlalchemy.Column(sqlalchemy.Text, index=True)
    code = sqlalchemy.Column(sqlalchemy.Text, primary_key=True)
    places = sqlalchemy.orm.relationship("Place")


@dataclasses.dataclass
class Place(Base):
    """A Twitter Place ORM data model."""

    id = sqlalchemy.Column(sqlalchemy.Text, primary_key=True)

    contained_within = sqlalchemy.orm.relationship(
        "Place", back_populates="contains", remote_side=[id]
    )
    contains = sqlalchemy.orm.relationship("Place", back_populates="contained_within")
    container_id = sqlalchemy.Column(
        sqlalchemy.Text,
        sqlalchemy.ForeignKey("places.id"),
        index=True
    )

    country_code = sqlalchemy.Column(
        sqlalchemy.Text,
        sqlalchemy.ForeignKey("countries.code"),
        index=True
    )
    country = sqlalchemy.orm.relationship("Country", back_populates="places")

    geom = sqlalchemy.Column(geoalchemy2.Geometry(srid=4326))

    name = sqlalchemy.Column(sqlalchemy.Text, index=True)
    full_name = sqlalchemy.Column(sqlalchemy.Text)

    place_type_id = sqlalchemy.Column(
        sqlalchemy.BigInteger,
        sqlalchemy.ForeignKey("place_types.id"),
        index=True
    )
    place_type = sqlalchemy.orm.relationship("PlaceType", back_populates="places")

    tweets = sqlalchemy.orm.relationship("Tweet")
