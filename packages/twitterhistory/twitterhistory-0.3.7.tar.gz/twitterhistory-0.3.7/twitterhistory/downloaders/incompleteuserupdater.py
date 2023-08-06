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
Re-download users for which we have incomplete data.

Uses the User lookup endpoint:
https://developer.twitter.com/en/docs/twitter-api/users/lookup/api-reference/get-users
"""


__all__ = ["IncompleteUserUpdater"]


from .incompletedataupdater import IncompleteDataUpdater


class IncompleteUserUpdater(IncompleteDataUpdater):
    """
    Re-download users for which we have incomplete data.

    Uses the User lookup endpoint:
    https://developer.twitter.com/en/docs/twitter-api/users/lookup/api-reference/get-users
    """

    API_ENDPOINT_URL = "https://api.twitter.com/2/users"

    def compile_query(self):
        """Compile the query dict for downloading a batch of data."""
        query = {
            "ids": ",".join(self._ids),
            "expansions": ",".join(
                [
                    "pinned_tweet_id"
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
            )
        }
        return query
