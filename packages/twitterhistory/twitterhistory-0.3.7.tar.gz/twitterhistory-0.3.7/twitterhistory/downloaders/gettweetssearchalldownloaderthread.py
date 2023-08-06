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


"""Worker threads wrapping an GetTweetsSearchAllDownloader."""


__all__ = ["GetTweetsSearchAllDownloaderThread"]


import datetime

from ..exceptions import (
    MonthlyQuotaExceededError,
    TemporaryApiResponseError,
)
from .basedownloaderthread import BaseDownloaderThread
from .gettweetssearchalldownloader import GetTweetsSearchAllDownloader

from ..timespan import TimeSpan


class GetTweetsSearchAllDownloaderThread(BaseDownloaderThread):
    """Wraps a TweetDownloader to run in a separate thread."""

    def __init__(self, api_key_managers, todo_deque, done_queue):
        """
        Initialize a GetTweetsSearchAllDownloaderThread.

        Args:
            api_key_managers: instance of an ApiKeyManager
            todo_deque: collections.deque that serves (search_term, TimeSpan)
                        tuples that need to be downloaded
            done_queue: queue.Queue into which to put (search_term, TimeSpan)
                        tuples that have been downloaded

        """
        super().__init__(api_key_managers=api_key_managers)

        self._todo_deque = todo_deque
        self._done_queue = done_queue

    def run(self):
        """Get TimeSpans off todo_deque and download tweets."""
        while not self.shutdown.is_set():
            try:
                search_term, timespan = self._todo_deque.pop()
                self._search_term = search_term
            except IndexError:
                break

            tweet_downloader = GetTweetsSearchAllDownloader(
                search_term, timespan, self._api_key_managers
            )

            earliest_tweet = timespan.end  # haven’t covered anything yet
            try:
                for batch in tweet_downloader.batches:
                    earliest_tweet = min(
                        earliest_tweet,
                        self.api_response_saver.save_batch(
                            batch,
                            search_term=search_term
                        )
                    )

                    if self.shutdown.is_set():
                        timespan.start = earliest_tweet
                        break

            except TemporaryApiResponseError as exception:
                # (includes RateLimitExceededError)
                # report what we managed to download ...
                self._done_queue.put(
                    (search_term, TimeSpan(earliest_tweet, timespan.end))
                )

                # and remember what we haven’t been able to download
                timespan.end = earliest_tweet
                self._todo_deque.append((search_term, timespan))

                # then wait until we’re allowed again, or told to shutdown
                wait_seconds = (
                    exception.reset_time - datetime.datetime.now(datetime.timezone.utc)
                ).total_seconds()

                if self.shutdown.wait(timeout=wait_seconds):
                    break

            except MonthlyQuotaExceededError as exception:
                # TODO: report error properly,
                # for now, re-raise exception to escalate to parent thread
                raise exception from None

            # … report to parent thread how much we worked
            self._done_queue.put((search_term, timespan))
