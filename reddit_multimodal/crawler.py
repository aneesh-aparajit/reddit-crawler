from __future__ import annotations
import praw
import pandas as pd
import numpy as np
from datetime import datetime
from typing import List
import bcrypt
import os
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from pprint import pprint


class Crawler(object):
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        user_agent: str,
        base_dir: str = "./data/",
    ) -> None:
        """Initializes the object of Crawler, which will eventually scrape the data from Reddit.

        Args:
            * client_id (str) : client_id is an id given by Reddit API.
            * client_secret (str) : client_secret is the secret key given by Reddit API when registering the project.
            * user_agent (str) : this is kind of a discription of the project
                - This is usually written as `<APP_NAME> <VERSION> /u/<USERNAME>`.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.reddit = praw.Reddit(
            client_id=self.client_id,
            client_secret=self.client_secret,
            user_agent=self.user_agent,
        )
        self.base_dir = base_dir
        self.sia = SIA()

    def _get_posts(
        self, subreddit_name: str, sort_by: str = "top", limit: int | None = None
    ):
        """This method of Crawler, retrieves the posts of a particular subreddit ordered by the sort_by parameter.

        Args:
            * subreddit_name (str) : The subreddit you want to crawl through.
            * sort_by (str) : The preference of tags to find.
            * limit (int) : The maximum number of posts you want.

        Return:
            * Returns a `praw.models.listing.generator.ListingGenerator` object.
                - The data can be accessed by using a simple for loop.
        """
        if sort_by not in ["hot", "new", "rising", "top"]:
            raise NotImplementedError(
                'This wrapper is only implemented for ["hot", "new", "rising", "top"].'
            )
        interface = self.reddit.subreddit(subreddit_name)
        iterator = getattr(interface, sort_by)
        posts = iterator(limit=limit)
        return posts

    def get_posts(
        self,
        subreddit_names: List[str],
        sort_by: str = "top",
        limit: int | None = None,
        save: bool = True,
        save_format: str = "csv",
    ) -> pd.DataFrame:

        """This method will help us extract the posts from a list of subreddits. This method saves the dataframe in different formats based on the request.

        Note: The name of the user will be encoded.

        Args:
            - subreddit_names (List[str]): This parameter expects a list which contains the names of the subreddit you want to scrape through.
            - sort_by (str): This parameter is a query to get the relevant posts.
            - limit (int | None): This is to control the number of parameters you want. None by default.
            - save (bool): This to say if you want to save the dataset or not. True by default.
            - save_format (str): This is to specify the format in which youn want to save the data. "csv" by default. The characters are expected to be lower case.

        Returns:
            Although this method will save the data in which ever format, it will return to you a `pd.DataFrame` object.
        """

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
            "subreddit": [],
            "title_polarity_neg": [],
            "title_polarity_pos": [],
            "title_compound": [],
            "body_polarity_neg": [],
            "body_polarity_pos": [],
            "body_compound": [],
            "urls": [],
        }

        for subreddit_name in subreddit_names:
            posts = self._get_posts(
                subreddit_name=subreddit_name, sort_by=sort_by, limit=limit
            )
            for p in posts:

                data["extracted_time"].append(datetime.now())
                data["subreddit"].append(f"r/{subreddit_name}")
                data["titles"].append(p.title)

                if p.author is not None:
                    data["authors"].append(
                        bcrypt.hashpw(p.author.name.encode("utf8"), bcrypt.gensalt())
                    )
                else:
                    data["authors"].append(np.nan)

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
                        data["multimedia_url"].append(np.nan)
                        data["multimedia_type"].append("text")

                data["body"].append(p.selftext)

                title_polarity = self.sia.polarity_scores(p.title)
                body_polarity = self.sia.polarity_scores(p.selftext)

                data["title_polarity_neg"].append(title_polarity["neg"])
                data["title_polarity_pos"].append(title_polarity["pos"])
                data["title_compound"].append(title_polarity["compound"])

                data["body_polarity_neg"].append(body_polarity["neg"])
                data["body_polarity_pos"].append(body_polarity["pos"])
                data["body_compound"].append(body_polarity["compound"])

                data["created"].append(p.created_utc)

        print({k: len(v) for k, v in data.items()})

        df = pd.DataFrame(data)

        if os.path.exists("./data"):
            pass
        else:
            os.mkdir("./data")
            print(f"./data/ did not exist. So, created file.")

        if save:
            if save_format == "csv":
                df.to_csv(os.path.join(self.base_dir, "posts.csv"))
            elif save_format == "tsv":
                df.to_csv(os.path.join(self.base_dir, "posts.tsv"), sep="\t")
            elif save_format == "parquet":
                df.to_csv(os.path.join(self.base_dir, "posts.parquet"))
            elif save_format == "json":
                df.to_csv(os.path.join(self.base_dir, "posts.json"))
            elif save_format == "sql":
                df.to_csv(os.path.join(self.base_dir, "posts.sql"))
            elif save_format == "pickle":
                df.to_csv(os.path.join(self.base_dir, "posts.pkl"))
            else:
                raise NotImplementedError(
                    """The format, you want the code is not implemented. But, you can extend the Crawler.get_posts() method by maneuvering the return object accordingly.
                    
                    Also, you may want to try entering the format in lower case!
                    """
                )

        return df

    def get_comments(
        self,
        subreddit_names: List[str],
        sort_by: str = "top",
        limit: int | None = None,
        save: bool = True,
        save_format: str = "csv",
    ) -> pd.DataFrame:

        """This method will return the comments for each post.

        Note: The name of the user will be encoded.

        Args:
            - subreddit_names (List[str]): This parameter expects a list which contains the names of the subreddit you want to scrape through.
            - sort_by (str): This parameter is a query to get the relevant posts.
            - limit (int | None): This is to control the number of parameters you want. None by default.
            - save (bool): This to say if you want to save the dataset or not. True by default.
            - save_format (str): This is to specify the format in which youn want to save the data. "csv" by default. The characters are expected to be lower case.

        Returns:
            Although this method will save the data in which ever format, it will return to you a `pd.DataFrame` object.
        """

        data = {
            "post_title": [],
            "post_user": [],
            "comment": [],
            "comment_user": [],
            "post_created": [],
            "subreddit": [],
            "comment_created": [],
        }

        for subreddit_name in subreddit_names:
            posts = self._get_posts(
                subreddit_name=subreddit_name, sort_by=sort_by, limit=limit
            )

            for p in posts:
                lim = 0
                for c in p.comments:
                    try:
                        (
                            title,
                            post_user,
                            comment,
                            comment_user,
                            post_created,
                            comment_created,
                            subreddit,
                        ) = [None] * 7

                        title = p.title
                        post_user = p.author.name if p.author is not None else np.nan
                        comment = c.body
                        comment_user = c.author.name if c.author is not None else np.nan
                        subreddit = subreddit_name
                        post_created = p.created_utc
                        comment_created = c.created_utc

                        data["post_title"].append(title)
                        data["post_user"].append(post_user)
                        data["post_created"].append(post_created)
                        data["comment"].append(comment)
                        data["comment_user"].append(comment_user)
                        data["comment_created"].append(comment_created)
                        data["subreddit"].append(subreddit)

                        lim += 1

                    except:
                        break

                    if lim == limit:
                        break

        df = pd.DataFrame(data)

        if os.path.exists("./data"):
            pass
        else:
            os.mkdir("./data")
            print(f"./data/ did not exist. So, created file.")

        if save:
            if save_format == "csv":
                df.to_csv(os.path.join(self.base_dir, "comments.csv"))
            elif save_format == "tsv":
                df.to_csv(os.path.join(self.base_dir, "comments.tsv"), sep="\t")
            elif save_format == "parquet":
                df.to_csv(os.path.join(self.base_dir, "comments.parquet"))
            elif save_format == "json":
                df.to_csv(os.path.join(self.base_dir, "comments.json"))
            elif save_format == "sql":
                df.to_csv(os.path.join(self.base_dir, "comments.sql"))
            elif save_format == "pickle":
                df.to_csv(os.path.join(self.base_dir, "comments.pkl"))
            else:
                raise NotImplementedError(
                    """The format, you want the code is not implemented. But, you can extend the Crawler.get_posts() method by maneuvering the return object accordingly.
                    
                    Also, you may want to try entering the format in lower case!
                    """
                )

        return df
