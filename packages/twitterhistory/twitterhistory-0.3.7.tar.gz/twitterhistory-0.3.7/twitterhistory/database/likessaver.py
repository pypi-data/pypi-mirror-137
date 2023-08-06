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


"""Save the `likes` contained in a `LikesDownloader.batch`."""


__all__ = ["LikesSaver"]


from .usersaver import UserSaver
from .models import Tweet, User


class LikesSaver(UserSaver):
    """Save the `likes` contained in a `LikesDownloader.batch`."""

    def _save_likes(self, likes, session, tweet_id):
        for user in likes:
            self._save_user(user, session)

        with session.begin():
            tweet = session.get(Tweet, tweet_id)
            session.add(tweet)

            for user in likes:
                user = session.get(User, int(user["id"]))
                tweet.liked_by.append(user)
                self.counts["likes"] += 1
