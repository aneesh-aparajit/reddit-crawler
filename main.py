import nltk
from reddit_multimodal_crawler.crawler import Crawler
import argparse

nltk.download("vader_lexicon")

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--subreddit_file_path",
        "A path to the file which contains the subreddits to scrape from.",
        type=str,
    )
    parser.add_argument(
        "--limit", "The limit to number of articles to scrape.", type=int
    )
    parser.add_argument("--client_id", "The Client ID provided by Reddit.", type=str)
    parser.add_argument(
        "--client_secret", "The Secret ID provided by the Reddit.", type=str
    )
    parser.add_argument(
        "--user_agent",
        "The User Agent in the form of <APP_NAME> <VERSION> by /u/<REDDIT_USERNAME>",
        type=str,
    )
    parser.add_argument(
        "--posts", "A boolean variable to parse through the posts or not.", type=bool
    )
    parser.add_argument(
        "--comments",
        "A boolean variable to parse through the comments of the top posts of subreddit",
        type=bool,
    )

    args = parser.parse_args()

    client_id = args["client_id"]
    client_secret = args["client_secret"]
    user_agent = args["user_agent"]
    file_path = args["subreddit_file_path"]
    limit = args["limit"]

    r = Crawler(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

    subreddit_list = open(file_path, "r").readlines().split()

    print(subreddit_list)

    if args["posts"]:
        r.get_posts(subreddit_names=subreddit_list, sort_by="top", limit=limit)

    if args["comments"]:
        r.get_comments(subreddit_names=subreddit_list, sort_by="top", limit=limit)
