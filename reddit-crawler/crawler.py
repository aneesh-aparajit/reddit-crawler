from __future__ import annotations
import praw
import pandas as pd
import json
import numpy as np
from datetime import datetime
from typing import List
from tqdm import tqdm
import bcrypt


class Crawler(object):
    def __init__(self, client_id: str, client_secret: str, user_agent: str) -> None:
        """Initializes the object of Crawler, which will eventually scrape the data from Reddit.

        Args:
            * client_id (str) : client_id is an id given by Reddit API.
            * client_secret (str) : client_secret is the secret key given by Reddit API when registering the project.
            * user_agent (str) : this is kind of a discription of the project
                - This is usually written as
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.reddit = praw.Reddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            user_agent=self.user_agent,
        )

    @classmethod
    def get_posts(
        self, subreddit_name: str, sort_by: str = "top", limit: int | None = None
    ):
        """This method of Crawler, retrieves the posts of a particular subreddit ordered by the sort_by parameter.

        Args:
            * subreddit_name (str) : The subreddit you want to crawl through.
            * sort_by (str) : The preference of tags to find.
            * limit (int) : The maximum number of posts you want.
        """
        if sort_by not in ["hot", "new", "rising", "top"]:
            raise NotImplementedError(
                'This wrapper is only implemented for ["hot", "new", "rising", "top"].'
            )
        interface = self.reddit.subreddit(subreddit_name)
        iterator = getattr(interface, sort_by)
        posts = iterator(limit=limit)
        return posts

    def return_posts_pandas(
        self,
        subreddit_names: List[str],
        sort_by: str = "top",
        limit: int | None = None,
        save: bool = True,
    ) -> pd.DataFrame:

        data = {
            "titles": [],
            "authors": [],
            "upvote_ratios": [],
            "upvotes": [],
            "created": [],
            "nsfw": [],
            "multimedia_url": [],
            "multimedia_type": [],
            "extracted_time": [],
            "body": [],
        }

        for subreddit_name in tqdm(subreddit_names):
            posts = self.get_posts(
                subreddit_name=subreddit_name, sort_by=sort_by, limit=limit
            )
            for p in posts:
                data["extracted_time"].append(datetime.now())
                data["titles"].append(p.title)
                data["authors"].append(
                    bcrypt.hashpw(p.author.encode("utf8"), bcrypt.gensalt())
                )
                data["upvote_ratios"].append(p.upvote_ratio)
                data["upvotes"].append(p.score)
                data["nsfw"].append(p.over_18)
                data["urls"].append(p.url)

                if p.is_video:
                    data["multimedia_type"].append("video")
                    data["multimedia_url"].append(
                        p.media["reddit_video"]["fallback_url"]
                    )

                else:
                    url = p.url
                    if url.split(".")[-1] in ["png", "jpg", "jpeg"]:
                        data["multimedia_url"].append(url)
                        data["multimedia_type"].append("image")

                    else:
                        data["multimedia_url"].append(np.na)
                        data["multimedia_type"].append("text")

                data["body"].append(p.selftext)
