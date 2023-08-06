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


"""Exceptions raised by twitterhistory."""


__all__ = [
    "ApiResponseError",
    "InvalidNextTokenError",
    "NoAcademicTwitterAccount",
    "MonthlyQuotaExceededError",
    "RateLimitExceededError",
    "TemporaryApiResponseError",
]


import datetime


class ApiResponseError(BaseException):
    """Raised when API returns bogus data."""


class InvalidNextTokenError(ApiResponseError):
    """
    Raised when API does not accept a next_token.

    This is to work around issue #13: some API endpoints
    return a next_token, even though there are no additional
    records to fetch on additional pages.
    """


class NoAcademicTwitterAccount(ApiResponseError):
    """Raised when API key not enrolled in academic API programme."""


class MonthlyQuotaExceededError(ApiResponseError):
    """Raised when API blocks because montly quota is used up."""


class TemporaryApiResponseError(ApiResponseError):
    """Raised when API has an error and waiting a bit should help."""

    def __init__(self, *args, time_until_reset=-1, **kwargs):
        """Initialise a TemporaryApiResponseError."""
        super().__init__(*args, **kwargs)
        self.reset_time = (
            datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(seconds=time_until_reset)
        )

    def __str__(self):
        """Show meaningful information about the remaining duration."""
        return "{:s}(reset_time={:%Y-%m-%d %H:%M:%S})".format(
            self.__class__.__name__, self.reset_time
        )

    def __repr__(self):
        """Show meaningful information about the remaining duration."""
        return str(self)


class RateLimitExceededError(TemporaryApiResponseError):
    """Raised when API blocks because rate limit is reached."""
