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


"""Base class for workers that search for incomplete records (of tweets and users, e.g.)."""


__all__ = ["IncompleteDataFinderThread"]


import queue

from .baseworkerthread import BaseWorkerThread
from ..database.engine import Session


QUEUE_SIZE = 100000  # limit memory usage (this is guesstimate, might need adjustment)


class IncompleteDataFinderThread(BaseWorkerThread):
    """Find incomplete records (base class)."""

    MAX_QUEUE_SIZE = 100000
    # limit memory usage
    # (this is guesstimate and might need adjustment)

    BATCH_SIZE = 1000

    def __init__(self):
        """Initialize an IncompleteDataUpdater."""
        super().__init__()
        self.incomplete_records = queue.Queue(self.MAX_QUEUE_SIZE)

    def run(self):
        """Feed the queue with the IDs of incomplete records."""
        while not self.shutdown.is_set():
            with Session() as session:
                if (
                    session.execute(
                        session.query(
                            self._sqlquery.exists()
                        )
                    )
                    .scalars()
                    .first()
                ):
                    # if there are any incomplete records
                    for record_id in (
                            session.execute(
                                self._sqlquery
                                .execution_options(stream_results=True)  # server-side cursor
                            )
                            .yield_per(self.BATCH_SIZE)
                            .scalars()
                    ):
                        while not self.shutdown.is_set():
                            try:
                                self.incomplete_records.put(record_id, timeout=1)
                                break
                            except queue.Full:
                                continue
                        else:
                            break  # break out of for loop

                else:
                    # there are NO INCOMPLETE RECORDS
                    # wait a bit and try again, unless self.shutdown is set
                    if self.shutdown.wait(timeout=(2 * 60)):
                        break
