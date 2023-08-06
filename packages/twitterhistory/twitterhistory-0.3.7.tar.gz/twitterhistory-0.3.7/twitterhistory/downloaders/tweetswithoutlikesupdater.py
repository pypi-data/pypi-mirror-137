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


"""
Downloads `likes` relationships for tweets.

Uses the Likes lookup endpoint:
https://developer.twitter.com/en/docs/twitter-api/tweets/likes/api-reference/get-tweets-id-liking_users#tab1
"""


__all__ = ["TweetsWithoutLikesUpdater"]


import queue

from .incompletedataupdater import IncompleteDataUpdater


class TweetsWithoutLikesUpdater(IncompleteDataUpdater):
    """Downloads `likes` relationships for tweets."""

    API_ENDPOINT_URL = "https://api.twitter.com/2/tweets/{id:d}/liking_users"

    def __init__(self, *args, **kwargs):
        """Initialise a TweetsWithoutLikesUpdater."""
        super().__init__(*args, **kwargs)
        self.liked_tweet_id = None

    @property
    def api_endpoint_url(self):
        """Return the API endpoint URL with path parameters replaced."""
        self.liked_tweet_id = None
        for _ in range(100):  # try to get an item off the queue at most 100 times
            try:
                self.liked_tweet_id = self._in_queue.get(timeout=10)
            except queue.Empty as exception:
                if self.shutdown.is_set():
                    raise exception
                continue

        if not self.liked_tweet_id:
            raise queue.Empty

        return self.API_ENDPOINT_URL.format(id=self.liked_tweet_id)

    def compile_query(self):
        """Compile the query dict for downloading a batch of data."""
        query = {
            "expansions": ",".join(
                [
                    "pinned_tweet_id"
                ]
            ),
            # "media.fields": ",".join(
            #     [
            #         #  "duration_ms",
            #         #  "height",
            #         #  "media_key",
            #         #  "preview_image_url",
            #         "type",
            #         "url",
            #         #  "width",
            #         # "public_metrics",
            #         #  "non_public_metrics",
            #         #  "organic_metrics",
            #         #  "promoted_metrics"
            #     ]
            # ),
            # "place.fields": ",".join(
            #     [
            #         #  "contained_within",
            #         "country",
            #         "country_code",
            #         "full_name",
            #         "geo",
            #         "id",
            #         "name",
            #         "place_type",
            #     ]
            # ),
            "tweet.fields": ",".join(
                [
                    "attachments",
                    "author_id",
                    # "context_annotations",
                    "conversation_id",
                    "created_at",
                    "entities",
                    "geo",
                    "id",
                    "in_reply_to_user_id",
                    "lang",
                    # "non_public_metrics",
                    "public_metrics",
                    # "organic_metrics",
                    # "promoted_metrics",
                    "possibly_sensitive",
                    "referenced_tweets",
                    "reply_settings",
                    "source",
                    "text",
                    "withheld",
                ]
            ),
            "user.fields": ",".join(
                [
                    "created_at",
                    "description",
                    "entities",
                    "location",
                    "name",
                    "pinned_tweet_id",
                    "profile_image_url",
                    "protected",
                    "public_metrics",
                    "url",
                    "username",
                    "verified",
                    "withheld",
                ]
            )
        }
        return query
