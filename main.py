import nltk
from reddit_crawler.crawler import Crawler

# nltk.download("vader_lexicon")

if __name__ == "__main__":
    r = Crawler(
        
    )

    print(
        r.return_posts_pandas(
            subreddit_names=["politics"],
        )
    )
