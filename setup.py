from setuptools import setup

from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="reddit_multimodal",
    version="2.0.0",
    description="A scraper which will scrape out multimedia data from reddit.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Aneesh Aparajit G",
    packages=["reddit_multimodal"],
    install_requires=["praw", "pandas", "numpy", "requests"],
    keywords=["web-scraping", "webscraper", "reddit", "multimodal", "datascience"],
    author_email="aneeshaparajit.g2002@gmail.com",
)
