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


"""Save the `includes` contained in a GetTweetsSearchAllDownloader.batch."""


__all__ = ["IncludesSaver"]


from .mediaitemsaver import MediaItemSaver
from .placesaver import PlaceSaver
from .tweetsaver import TweetSaver
from .usersaver import UserSaver


class IncludesSaver(MediaItemSaver, PlaceSaver, TweetSaver, UserSaver):
    """Save the `includes` contained in a GetTweetsSearchAllDownloader.batch."""

    def _save_includes(self, includes, session):
        if "media" in includes:
            for media_item in includes["media"]:
                if self.shutdown.is_set():
                    break
                self._save_media_item(media_item, session)
        if "places" in includes:
            for place in includes["places"]:
                if self.shutdown.is_set():
                    break
                self._save_place(place, session)
        if "tweets" in includes:
            for tweet in includes["tweets"]:
                if self.shutdown.is_set():
                    break
                self._save_tweet(tweet, session)
        if "users" in includes:
            for user in includes["users"]:
                if self.shutdown.is_set():
                    break
                self._save_user(user, session)

        # note to self:
        #   to avoid redundant code here,
        #   should we have an iterator method that yields
        #   the next thing and checks in between?
