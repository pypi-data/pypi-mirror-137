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


"""Worker threads wrapping an IncompleteDataUpdater."""


__all__ = ["IncompleteDataUpdaterThread"]


import datetime
import queue

from ..exceptions import (
    InvalidNextTokenError,
    MonthlyQuotaExceededError,
    TemporaryApiResponseError,
)
from .basedownloaderthread import BaseDownloaderThread


class IncompleteDataUpdaterThread(BaseDownloaderThread):
    """Wraps an IncompleteDataUpdater to run in a separate thread."""

    # After this many attempts to find empty records we’ll let it be
    MAX_SUCCESSIVE_UNSUCCESSFUL_ATTEMPTS = 10

    # How long to wait (in seconds) in between attempts
    WAIT_SECONDS_IN_BETWEEN_ATTEMPTS = 2 * 60

    def __init__(self, api_key_managers, in_queue):
        """
        Initialize a IncompleteDataUpdaterThread.

        Args:
            api_key_managers: instance of an ApiKeyManager
            in_queue: queue.Queue
        """
        super().__init__(api_key_managers=api_key_managers)
        self._in_queue = in_queue

    def run(self):
        """Download data for incomplete records."""
        successive_unsuccessful_attempts = 0
        while (
                successive_unsuccessful_attempts < self.MAX_SUCCESSIVE_UNSUCCESSFUL_ATTEMPTS
                and not self.shutdown.is_set()
        ):
            data_downloader = self._Downloader(
                self._in_queue,
                self._api_key_managers,
                self.shutdown
            )

            try:
                for batch in data_downloader.batches:
                    try:
                        liked_tweet_id = data_downloader.liked_tweet_id
                    except AttributeError:
                        liked_tweet_id = None

                    self.api_response_saver.save_batch(
                        batch,
                        liked_tweet_id=liked_tweet_id
                    )

                    if self.shutdown.is_set():
                        break

                successive_unsuccessful_attempts = 0

            except InvalidNextTokenError:
                # we got a next_token, but there was no additional data
                continue

            except TemporaryApiResponseError as exception:
                # wait until we’re allowed again
                wait_seconds = (
                    exception.reset_time - datetime.datetime.now(datetime.timezone.utc)
                ).total_seconds()

                if self.shutdown.wait(timeout=wait_seconds):
                    break

            except MonthlyQuotaExceededError as exception:
                # TODO: report error properly,
                # for now, re-raise exception to escalate to parent thread
                raise exception from None

            except queue.Empty:
                # wait a bit and try again, unless self.shutdown is set
                successive_unsuccessful_attempts += 1
                if self.shutdown.wait(timeout=self.WAIT_SECONDS_IN_BETWEEN_ATTEMPTS):
                    break
