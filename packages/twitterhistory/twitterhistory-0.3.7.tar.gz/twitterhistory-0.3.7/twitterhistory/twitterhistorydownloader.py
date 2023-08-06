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


"""Download posts and user metadata from the microblogging service Twitter."""


__all__ = ["TwitterHistoryDownloader"]


try:
    import blessed
    from .fancytwitterhistorydownloader import FancyTwitterHistoryDownloader
except ImportError:
    blessed = False

from .basictwitterhistorydownloader import BasicTwitterHistoryDownloader


class TwitterHistoryDownloader:  # pylint: disable=too-few-public-methods
    """Download posts and user metadata from the microblogging service Twitter."""

    __abstract__ = True

    def __new__(cls, *args, **kwargs):
        """Create a new TweetDownloader (dep. on terminal’s capabilities)."""
        if blessed and blessed.Terminal().does_styling:
            _cls = FancyTwitterHistoryDownloader
        else:
            _cls = BasicTwitterHistoryDownloader

        instance = _cls.__new__(_cls, *args, **kwargs)
        instance.__init__(*args, **kwargs)
        return instance
