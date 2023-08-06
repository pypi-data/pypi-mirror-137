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


"""Save a place to the database."""


__all__ = ["PlaceSaver"]


import shapely.geometry

from .baseitemsaver import BaseItemSaver
from .models import Country, Place, PlaceType


class PlaceSaver(BaseItemSaver):
    """Save a place to the database."""

    def _save_place(self, data, session):
        """Save a place to the database."""
        with session.begin():
            place = session.get(Place, data["id"]) or Place(id=data["id"])

            if place.name is None:
                session.add(place)

                place.name = data["name"],
                place.full_name = data["full_name"]

                place.place_type = (
                    session.query(PlaceType)
                    .filter(PlaceType.place_type == data["place_type"])
                    .first()
                ) or PlaceType(place_type=data["place_type"])

                if "contained_within" in data:
                    for containing_place in data["contained_within"]:
                        containing_place = (
                            session.get(Place, containing_place)
                            or Place(id=containing_place)
                        )
                        place.contained_within.append(containing_place)

                if "country" in data and "country_code" in data:
                    place.country = (
                        session.get(Country, data["country_code"])
                        or Country(
                            code=data["country_code"],
                            name=data["country"]
                        )
                    )

                if "geometry" in data["geo"]:
                    place.geom = "SRID=4326;" + shapely.geometry.shape(data["geo"]["geometry"]).wkt
                elif "bbox" in data["geo"]:
                    place.geom = "SRID=4326;" + shapely.geometry.box(*data["geo"]["bbox"]).wkt

        return place
