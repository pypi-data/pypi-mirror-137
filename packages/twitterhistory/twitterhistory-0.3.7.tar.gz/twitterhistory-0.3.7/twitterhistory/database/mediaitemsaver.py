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


"""Save a media_item to the database."""


__all__ = ["MediaItemSaver"]


from .baseitemsaver import BaseItemSaver
from .models import MediaItem, MediaType


class MediaItemSaver(BaseItemSaver):
    """Save a media_item to the database."""

    def _save_media_item(self, data, session):
        """Save a media_item to the database."""
        with session.begin():
            media_item = session.get(MediaItem, data["media_key"])

            if media_item is None:
                media_item = MediaItem(media_key=data["media_key"])

                if "url" in data:
                    media_item.url = data["url"]

                media_item.media_type = (
                    session.query(MediaType)
                    .filter(MediaType.media_type == data["type"])
                    .first()
                ) or MediaType(media_type=data["type"])

                session.add(media_item)

        return media_item
