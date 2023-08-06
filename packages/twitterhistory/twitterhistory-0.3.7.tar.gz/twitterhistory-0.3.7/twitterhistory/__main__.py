#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#   Copyright (C) 2019 Christoph Fink, University of Helsinki
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


import argparse


def main():
    """Download posts and user metadata from the microblogging service Twitter."""
    argparser = argparse.ArgumentParser(prog="python -m twitterhistory")
    argparser.add_argument(
        "-c",
        "--config",
        help="""Use this config file (instead of the default location, see README)""",
        default=None
    )
    args = argparser.parse_args()

    # because Config is a pseudo-singleton, we have to import it only here (once
    # we know a possible different configuration file path)
    # We also need to explicitely create a Config() because importing
    # TwitterHistoryDownloader would implicitely create one without arguments
    from .config import Config
    _ = Config(config_files=args.config)

    from .twitterhistorydownloader import TwitterHistoryDownloader
    TwitterHistoryDownloader().download()


if __name__ == "__main__":
    main()
