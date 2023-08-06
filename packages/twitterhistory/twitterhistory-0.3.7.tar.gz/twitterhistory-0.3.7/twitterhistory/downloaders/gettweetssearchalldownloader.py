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
Download all tweets relating to a search query.

Uses the full-archive search endpoint available to Twitter accounts
with access to the Academic Research API track.

https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-all
"""


__all__ = ["GetTweetsSearchAllDownloader"]


from .basedownloader import BaseDownloader


class GetTweetsSearchAllDownloader(BaseDownloader):
    """
    Download all tweets relating to a search query.

    Uses the full-archive search endpoint available to Twitter accounts
    with access to the Academic Research API track.

    https://developer.twitter.com/en/docs/twitter-api/tweets/search/api-reference/get-tweets-search-all
    """

    API_ENDPOINT_URL = "https://api.twitter.com/2/tweets/search/all"

    def __init__(self, search_term, timespan, api_key_managers):
        """Initialize a GetTweetsSearchAllDownloader."""
        super().__init__(api_key_managers)
        self._search_term = search_term
        self._timespan = timespan

    def compile_query(self):
        """Compile the query dict for downloading a batch of data."""
        query = {
            "query": self._search_term,
            "expansions": ",".join(
                [
                    #  "attachments.poll_ids",
                    "attachments.media_keys",
                    "author_id",
                    "entities.mentions.username",
                    "geo.place_id",
                    "in_reply_to_user_id",
                    "referenced_tweets.id",
                    "referenced_tweets.id.author_id",
                ]
            ),
            "media.fields": ",".join(
                [
                    #  "duration_ms",
                    #  "height",
                    #  "media_key",
                    #  "preview_image_url",
                    "type",
                    "url",
                    #  "width",
                    # "public_metrics",
                    #  "non_public_metrics",
                    #  "organic_metrics",
                    #  "promoted_metrics"
                ]
            ),
            "place.fields": ",".join(
                [
                    #  "contained_within",
                    "country",
                    "country_code",
                    "full_name",
                    "geo",
                    "id",
                    "name",
                    "place_type",
                ]
            ),
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
            ),
            "start_time": self._timespan.start.isoformat(),
            "end_time": self._timespan.end.isoformat(),
            "max_results": 500,
        }
        return query
