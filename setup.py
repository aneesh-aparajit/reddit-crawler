from setuptools import setup

setup(
    name="reddit-crawler",
    version="0.0.1",
    description="A scraper which will scrape out multimedia data from reddit.",
    long_description="""""",
    author="Aneesh Aparajit G",
    packages=["reddit-crawler"],
    install_requires=["praw", "pandas", "numpy", "requests"],
)
