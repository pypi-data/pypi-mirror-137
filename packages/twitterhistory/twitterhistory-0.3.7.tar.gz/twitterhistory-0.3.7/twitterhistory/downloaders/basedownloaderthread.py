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


"""Base class for worker threads downloading data."""


__all__ = ["BaseDownloaderThread"]


from .baseworkerthread import BaseWorkerThread
from ..database.apiresponsesaver import ApiResponseSaver


class BaseDownloaderThread(BaseWorkerThread):
    """Base class for worker threads downloading data."""

    def __init__(self, api_key_managers):
        """
        Intialize a BaseDownloaderThread.

        Args:
            api_key_managers: instance of an ApiKeyManager
        """
        super().__init__()
        self._api_key_managers = api_key_managers
        self.api_response_saver = ApiResponseSaver(self.shutdown)

    @property
    def counts(self):
        """Count how many tweets we saved to the database."""
        return self.api_response_saver.counts
