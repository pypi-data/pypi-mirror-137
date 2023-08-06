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


"""Save a user to the database."""


__all__ = ["UserSaver"]


import dateparser

from .baseitemsaver import BaseItemSaver
from .models import Hashtag, Tweet, Url, User
from ..config import Config


class UserSaver(BaseItemSaver):
    """Save a user to the database."""

    def _save_user(self, data, session):
        """Save a user to the database."""
        with Config() as config:
            if config["pseudonymise"]:
                data = User._pseudonymise_api_data(data)

        with session.begin():
            user = session.get(User, int(data["id"])) or User(id=int(data["id"]))

            if (
                    user.username is None
                    or user.name is None
                    or user.followers_count is None
                    or user.following_count is None
                    or user.tweet_count is None
                    or user.listed_count is None
            ):
                session.add(user)

                user.id = int(data["id"])
                user.username = data["username"]
                user.name = data["name"]
                user.description = data["description"]
                user.protected = data["protected"]
                user.verified = data["verified"]

                if "location" in data:
                    user.location = data["location"]

                if data["created_at"]:
                    user.created_at = dateparser.parse(data["created_at"])

                if "pinned_tweet_id" in data:
                    user.pinned_tweet = (
                        session.get(Tweet, int(data["pinned_tweet_id"]))
                        or Tweet(id=int(data["pinned_tweet_id"]))
                    )

                user.profile_image_url = (
                    session.query(Url)
                    .filter(Url.url == data["profile_image_url"])
                    .first()
                ) or Url(url=data["profile_image_url"])

                if (
                    "entities" in data
                    and "description" in data["entities"]
                    and "hashtags" in data["entities"]["description"]
                ):
                    hashtags = []
                    for hashtag in data["entities"]["description"]["hashtags"]:
                        hashtags.append(hashtag["tag"])
                    hashtags = set(hashtags)
                    for hashtag in hashtags:
                        hashtag = (
                            session.get(Hashtag, hashtag)
                            or Hashtag(hashtag=hashtag)
                        )
                        if hashtag not in user.hashtags:
                            user.hashtags.append(hashtag)

                if (
                    "entities" in data
                    and "url" in data["entities"]
                    and "urls" in data["entities"]["url"]
                ):
                    urls = []
                    for url in data["entities"]["url"]["urls"]:
                        try:
                            urls.append(url["expanded_url"])
                        except KeyError:
                            urls.append(url["url"])
                    urls = set(urls)
                    for url in urls:
                        url = (
                            (
                                session.query(Url)
                                .filter(Url.url == url)
                                .first()
                            )
                            or Url(url=url)
                        )
                        if url not in user.urls:
                            user.urls.append(url)

                if "public_metrics" in data:
                    user.followers_count = data["public_metrics"]["followers_count"]
                    user.following_count = data["public_metrics"]["following_count"]
                    user.tweet_count = data["public_metrics"]["tweet_count"]
                    user.listed_count = data["public_metrics"]["listed_count"]

                self.counts["users"] += 1

        return user
