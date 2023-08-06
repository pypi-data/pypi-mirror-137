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


"""Save a tweet to the database."""


__all__ = ["TweetSaver"]


import dateparser
import shapely.geometry

from .baseitemsaver import BaseItemSaver
from .models import (
    Conversation,
    Hashtag,
    Language,
    MediaItem,
    Place,
    Tweet,
    TweetReference,
    TweetReferenceType,
    Url,
    User
)
from ..config import Config


class TweetSaver(BaseItemSaver):
    """Save a tweet to the database."""

    def _save_tweet(self, data, session, search_term=None):
        """Save a tweet to the database."""
        with Config() as config:
            if config["pseudonymise"]:
                data = Tweet._pseudonymise_api_data(data)

        with session.begin():
            tweet = session.get(Tweet, int(data["id"])) or Tweet(id=int(data["id"]))

            if (
                    tweet.text is None
                    or tweet.like_count is None
                    or tweet.quote_count is None
                    or tweet.reply_count is None
                    or tweet.retweet_count is None
            ):
                # some important properties missing:
                # probably we did not save this tweet (properly) yet

                session.add(tweet)
                tweet.possibly_sensitive = data["possibly_sensitive"]
                tweet.text = data["text"]

                if data["created_at"]:
                    tweet.created_at = dateparser.parse(data["created_at"])

                if data["author_id"]:  # error responses (deleted tweets) don’t detail users
                    tweet.author = (
                        session.get(User, data["author_id"])
                        or User(id=data["author_id"])
                    )

                if (
                    "geo" in data
                    and "coordinates" in data["geo"]
                    and "coordinates" in data["geo"]["coordinates"]
                ):
                    tweet.geom = "SRID=4326;" + shapely.geometry.Point(
                        *data["geo"]["coordinates"]["coordinates"]
                    ).wkt

                if "geo" in data and "place_id" in data["geo"]:
                    tweet.place = (
                        session.get(Place, data["geo"]["place_id"])
                        or Place(id=data["geo"]["place_id"])
                    )

                if "in_reply_to_user_id" in data:
                    if data["in_reply_to_user_id"] == data["author_id"]:
                        tweet.in_reply_to = tweet.author
                    else:
                        tweet.in_reply_to = (
                            session.get(User, data["in_reply_to_user_id"])
                            or User(id=data["in_reply_to_user_id"])
                        )

                if "conversation_id" in data:
                    tweet.conversation = (
                        session.get(Conversation, data["conversation_id"])
                        or Conversation(id=data["conversation_id"])
                    )

                tweet.language = (
                    session.get(Language, data["lang"])
                    or Language(language=data["lang"])
                )

                if "attachments" in data and "media_keys" in data["attachments"]:
                    tweet.media = []
                    for media_key in data["attachments"]["media_keys"]:
                        media_item = (
                            session.get(MediaItem, media_key)
                            or MediaItem(media_key=media_key)
                        )
                        if media_item not in tweet.media:
                            tweet.media.append(media_item)

                if "entities" in data and "hashtags" in data["entities"]:
                    tweet.hashtags = []
                    for hashtag in data["entities"]["hashtags"]:
                        hashtag = (
                            session.get(Hashtag, hashtag["tag"])
                            or Hashtag(hashtag=hashtag["tag"])
                        )
                        if hashtag not in tweet.hashtags:
                            tweet.hashtags.append(hashtag)

                if "entities" in data and "urls" in data["entities"]:
                    tweet.urls = []
                    for url in data["entities"]["urls"]:
                        url = (
                            session.query(Url)
                            .filter(Url.url == url["url"])
                            .first()
                        ) or Url(url=url["url"])
                        if url not in tweet.urls:
                            tweet.urls.append(url)

                if "entities" in data and "mentions" in data["entities"]:
                    tweet.mentions = []
                    for mention in data["entities"]["mentions"]:
                        # if everything went in order, then we should already
                        # have saved the user (mention is by username)
                        mentioned_user = (
                            session.query(User)
                            .filter(User.username == mention["username"])
                            .first()
                        )
                        if (
                                mentioned_user is not None  # TODO!
                                and mentioned_user not in tweet.mentions
                        ):
                            tweet.mentions.append(mentioned_user)

                if "referenced_tweets" in data:
                    for referenced_tweet in data["referenced_tweets"]:
                        tweet_reference = TweetReference()
                        reference_type = (
                            session.query(TweetReferenceType)
                            .filter(TweetReferenceType.reference_type == referenced_tweet["type"])
                            .first()
                        ) or (
                            TweetReferenceType(
                                reference_type=referenced_tweet["type"]
                            )
                        )
                        referenced_tweet = (
                            session.get(Tweet, int(referenced_tweet["id"]))
                            or Tweet(id=int(referenced_tweet["id"]))
                        )

                        tweet_reference = session.get(
                            TweetReference,
                            {
                                "referencing_tweet_id": tweet.id,
                                "referenced_tweet_id": referenced_tweet.id,
                                "reference_type_id": reference_type.id
                            }
                        )
                        if not tweet_reference:
                            tweet_reference = TweetReference(
                                referenced_tweet=referenced_tweet,
                                reference_type=reference_type
                            )
                            tweet.referenced_tweets.append(tweet_reference)

                        session.add(tweet_reference.referenced_tweet)
                        session.flush()
                        # not sure why we have to flush here, but session.get()
                        # does not return any pending objects -> might lead to
                        # duplicate tweets in the same commit (==merge conflict)

                if "public_metrics" in data:
                    tweet.like_count = data["public_metrics"]["like_count"]
                    tweet.quote_count = data["public_metrics"]["quote_count"]
                    tweet.reply_count = data["public_metrics"]["reply_count"]
                    tweet.retweet_count = data["public_metrics"]["retweet_count"]

                if search_term is not None:
                    tweet.search_terms = [search_term]

                self.counts["tweets"] += 1

        return tweet
