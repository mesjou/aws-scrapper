# Project Title

A simple scrapper used for getting Amazon prices.

## Summary

  - [Installing](#installing)
  - [Getting Started](#getting-started)
  - [Acknowledgments](#acknowledgments)

## Installing

After cloning install a virtual environment with ```venv``` and name ```venv```.
Then run ```./refresh-requirements.sh```.
Environment should have all required packages installed and also precommit hook is set up.


## Getting Started

Search for your desired amazon article and copy url to csv file at ```src/tracker/tracker.csv```.
Also remember to add a code to identify the product.
Now your set up to scrape by executing ```scraper.py```.

## Acknowledgments

This scrapper is inspired by the work of Fábio Neves and his article on medium
https://towardsdatascience.com/scraping-multiple-amazon-stores-with-python-5eab811453a8
