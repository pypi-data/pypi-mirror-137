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


"""Save a batch of data as returned by GetTweetsSearchAllDownloader.batches."""


__all__ = ["ApiResponseSaver"]


import datetime

import dateparser

from .engine import Session
from .errorssaver import ErrorsSaver
from .includessaver import IncludesSaver
from .likessaver import LikesSaver
from .models import SearchTerm
from .tweetsaver import TweetSaver
from ..exceptions import MonthlyQuotaExceededError


class ApiResponseSaver(IncludesSaver, ErrorsSaver, LikesSaver, TweetSaver):
    """Save a batch of data as returned by GetTweetsSearchAllDownloader.batches."""

    def save_batch(self, batch, search_term=None, liked_tweet_id=None):
        """
        Save the data in `batch` to the database.

        Tries to figure out whether items in `batch["data"]` are
        users or tweets.
        """
        earliest_tweet_created_at = datetime.datetime.now(datetime.timezone.utc)

        with Session() as session:
            with session.begin():
                if search_term:
                    search_term = (
                        session.query(SearchTerm)
                        .filter(SearchTerm.search_term == search_term)
                        .first()
                    ) or session.add(SearchTerm(search_term=search_term))

            if "title" in batch and batch["title"] == "UsageCapExceeded":
                raise MonthlyQuotaExceededError()

            if "includes" in batch:
                self._save_includes(batch["includes"], session)

            if "errors" in batch:
                self._save_errors(batch["errors"], session)

            if "data" in batch:
                if liked_tweet_id:
                    self._save_likes(batch["data"], session, liked_tweet_id)
                else:
                    for item in batch["data"]:
                        if "author_id" in item:
                            self._save_tweet(item, session, search_term)
                            earliest_tweet_created_at = min(
                                earliest_tweet_created_at, dateparser.parse(item["created_at"])
                            )
                        elif "username" in item:
                            self._save_user(item, session)

        return earliest_tweet_created_at
