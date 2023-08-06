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
Download (all) tweets.

Overloaded to provide fancy console output
"""


__all__ = ["FancyTwitterHistoryDownloader"]


import threading

import blessed

from .basictwitterhistorydownloader import BasicTwitterHistoryDownloader
from . import __version__ as version


class FancyTwitterHistoryDownloader(BasicTwitterHistoryDownloader):
    """
    Download (all) tweets.

    With fancy console output.
    """

    WELCOME = (
        "{t.bold}{t.blue} ### twitterhistory "
        + "{t.normal}{t.blue}"
        + version
        + "{t.bold} ###"
        + "{t.normal}"
    )

    STATUS = (
        "{t.normal} Downloaded metadata for "
        + "{t.bold}{t.magenta}{tweets: 9d} 💬 tweets "
        + "{t.normal}{t.magenta}{tweet_rate: 11.1f}/s\n"
        + "{t.normal}                         "
        + "{t.bold}{t.magenta}{users: 9d} 👦 users "
        + "{t.normal}{t.magenta}{user_rate: 11.1f}/s\n"
        + "{t.normal}                         "
        + "{t.bold}{t.magenta}{likes: 9d} 👍 likes "
        + "{t.normal}{t.magenta}{like_rate: 11.1f}/s\n"
        + "{t.normal} using                   "
        + "{t.bold}{t.green}{workers: 9d} 💪 workers\n"
        + "{t.normal}{t.bold} TODO:                {todo: 12d} 🚧 time slots"
        + "{t.normal}"
    )
    STATUS_LINES = len(STATUS.splitlines())

    SHUTDOWN_ANNOUNCEMENT = "{t.bold}Cleaning up. 🛑 {t.normal}"

    SUMMARY = (
        "{t.normal}Downloaded  {t.bold}{t.magenta}{tweets: 9d} 💬 tweets\n"
        + "{t.normal}            {t.bold}{t.magenta}{users: 9d} 👦 users\n"
        + "{t.normal}            {t.bold}{t.magenta}{likes: 9d} 👍 likes\n"
        + "{t.normal}"
    )

    def __init__(self):
        """Initialise TweetDownloader."""
        super().__init__()

        self.terminal = blessed.Terminal()

        print(self.WELCOME.format(t=self.terminal))

        # scroll down terminal, in case we’re at the bottom
        print(self.STATUS_LINES * "\n", end="")

        self.pos_y, _ = self.terminal.get_location(timeout=5)
        self._tweet_count = 0

    def report_progress(self):
        """Report current progress."""
        statistics = self.statistics

        with self.terminal.location(0, (self.pos_y - self.STATUS_LINES)):
            print(
                self.STATUS.format(
                    t=self.terminal,
                    tweets=statistics.tweets,
                    users=statistics.users,
                    likes=statistics.likes,
                    tweet_rate=statistics.tweets_rate,
                    user_rate=statistics.users_rate,
                    like_rate=statistics.likes_rate,
                    workers=(threading.active_count() - self.NUM_MANAGERS),
                    todo=len(self._todo_deque),
                )
            )

    def announce_shutdown(self):
        """Tell the user that we initiated shutdown."""
        # clear the status output
        for i in range(self.STATUS_LINES):
            with self.terminal.location(0, (self.pos_y - (i + 1))):
                print(self.terminal.clear_eol)

        with self.terminal.location(0, (self.pos_y - self.STATUS_LINES)):
            print(self.SHUTDOWN_ANNOUNCEMENT.format(t=self.terminal))

    def summarise_overall_progress(self):
        """
        Summarise what we have done.

        (Called right before exit)
        """
        statistics = self.statistics
        with self.terminal.location(0, (self.pos_y - self.STATUS_LINES)):
            print(
                self.SUMMARY.format(
                    t=self.terminal,
                    tweets=statistics.tweets,
                    users=statistics.users,
                    likes=statistics.likes,
                    tweet_rate=statistics.tweets_rate,
                    user_rate=statistics.users_rate,
                    like_rate=statistics.likes_rate
                )
            )
