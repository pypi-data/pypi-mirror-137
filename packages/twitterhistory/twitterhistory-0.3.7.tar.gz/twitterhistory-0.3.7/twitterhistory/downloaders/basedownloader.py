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


"""Parent class for all downloaders."""


__all__ = [
    "BaseDownloader"
]


import json

import requests
import requests.exceptions

from ..exceptions import (
    ApiResponseError,
    InvalidNextTokenError,
    NoAcademicTwitterAccount,
    MonthlyQuotaExceededError,
    RateLimitExceededError,
    TemporaryApiResponseError
)


class BaseDownloader:  # pylint: disable=too-few-public-methods
    """Parent class for all downloaders."""

    _api_key_managers = {}  # ‘pseudo-singleton’

    def __init__(self, api_key_managers={}):
        """Initialize the base class for downloaders."""
        if not self._api_key_managers:
            self._api_key_managers = api_key_managers

    def compile_query(self):
        """Compile the query dict for downloading a batch of data."""
        raise NotImplementedError(
            "BaseDownloader does not provide a compile_query, "
            + " implement it in child classes."
        )

    @property
    def api_endpoint_url(self):
        """Return the API_ENDPOINT_URL with possible extra path parameters `.format()`ed."""
        # override this in more specific cases in the child class
        return self.API_ENDPOINT_URL

    @property
    def batches(self):
        """Iterate over downloaded batches of data."""
        query = self.compile_query()
        next_token = None

        while True:
            if next_token is not None:
                query["next_token"] = next_token

            with self._api_key_managers[self.API_ENDPOINT_URL].get_api_key() as api_key:
                headers = {"Authorization": "Bearer {:s}".format(api_key)}

                try:
                    response = requests.get(
                        self.api_endpoint_url, headers=headers, params=query
                    )
                except requests.exceptions.RequestException:
                    raise TemporaryApiResponseError(time_until_reset=120)

                try:
                    # some strings in Twitter API responses can apparently
                    # contain NUL characters that cause hickups in PostgreSQL
                    results = json.loads(
                        response.text
                        .replace("\\u0000", "\\u2400")
                    )
                except json.decoder.JSONDecodeError as exception:
                    raise ApiResponseError(response.text) from exception

                if not response.ok:
                    try:
                        if results["error"]["code"] == 88:
                            raise RateLimitExceededError(
                                response.headers["x-rate-limit-reset"]
                            )
                    except KeyError:
                        pass

                    try:
                        if (
                                results["status"] == 429
                                or results["status"] == 503
                        ):
                            # results["title"]: "Too Many Requests"
                            # results["title"]: "Service Unavailable"
                            # wait 2 min
                            raise TemporaryApiResponseError(
                                time_until_reset=120
                            )
                    except KeyError:
                        pass

                    try:
                        if results["title"] == "UsageCapExceeded":
                            raise MonthlyQuotaExceededError()
                    except KeyError:
                        pass

                    try:
                        if results["reason"] == "client-not-enrolled":
                            raise NoAcademicTwitterAccount(results["detail"])
                    except KeyError:
                        pass

                    try:
                        for error in results["errors"]:
                            if "next_token" in error["parameters"]:
                                # some endpoints (e.g., liking_users) wrongly
                                # return a next_token
                                raise InvalidNextTokenError
                    except KeyError:
                        pass

                    # other, not anticipated error:
                    raise ApiResponseError((results, response.headers))

            yield results

            try:
                next_token = results["meta"]["next_token"]
            except KeyError:
                break
