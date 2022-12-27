from setuptools import setup

setup(
    name="reddit_crawler",
    version="1.0.0",
    description="A scraper which will scrape out multimedia data from reddit.",
    long_description="""This package will help you scrape data from reddit for any of your data science or data analytics project. This is a wrapper on the PRAW package customized for easy data extraction.""",
    author="Aneesh Aparajit G",
    packages=["reddit_multimodal"],
    install_requires=["praw", "pandas", "numpy", "requests"],
    keywords=["web-scraping", "webscraper", "reddit", "multimodal", "datascience"],
    author_email="aneeshaparajit.g2002@gmail.com",
)
