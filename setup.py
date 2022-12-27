from setuptools import setup

from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="reddit_multimodal_crawler",
    version="1.2.0",
    description="A scraper which will scrape out multimedia data from reddit.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Aneesh Aparajit G",
    url="https://github.com/aneesh-aparajit/reddit-crawler",
    packages=["reddit_multimodal_crawler"],
    install_requires=["praw", "pandas", "numpy", "requests", "bcrypt", "nltk"],
    keywords=["web-scraping", "webscraper", "reddit", "multimodal", "datascience"],
    author_email="aneeshaparajit.g2002@gmail.com",
)
