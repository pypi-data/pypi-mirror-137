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


"""Save the `errors` contained in a GetTweetsSearchAllDownloader.batch."""


__all__ = ["ErrorsSaver"]


from .tweetsaver import TweetSaver
from .usersaver import UserSaver


class ErrorsSaver(TweetSaver, UserSaver):
    """Save the `errors` contained in a GetTweetsSearchAllDownloader.batch."""

    def _save_errors(self, errors, session):
        for error in errors:
            if error["resource_type"] == "tweet":
                self._save_tweet(
                    {
                        "author_id": None,
                        "conversation_id": -1,
                        "created_at": None,
                        "id": error["resource_id"],
                        "lang": "",
                        "possibly_sensitive": None,
                        "public_metrics": {
                            "like_count": -1,
                            "quote_count" : -1,
                            "reply_count": -1,
                            "retweet_count": -1
                        },
                        "text": error["detail"]
                    },
                    session
                )
            elif error["resource_type"] == "user":
                try:
                    int(error["resource_id"])
                except ValueError:
                    continue
                    # {
                    #     "parameter": "entities.mentions.username",
                    #     "resource_id": "seputaranbgr",
                    #     "value": "seputaranbgr",
                    #     "detail": "User has been suspended: [seputaranbgr].",
                    #     "title": "Forbidden",
                    #     "resource_type": "user",
                    #     "type": "https://api.twitter.com/2/problems/resource-not-found"
                    # },

                self._save_user(
                    {
                        "created_at": None,
                        "description": error["detail"],
                        "id": error["resource_id"],
                        "name": "[{title:s}: {resource_id:s}]".format(**error),
                        "profile_image_url": "",
                        "protected": None,
                        "public_metrics": {
                            "followers_count": -1,
                            "following_count": -1,
                            "tweet_count": -1,
                            "listed_count": -1
                        },
                        "username": "[{title:s}: {resource_id:s}]".format(**error),
                        "verified": None
                    },
                    session
                )
