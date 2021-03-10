import os.path as path
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) \
    Version/14.0.3 Safari/605.1.15",
    "Accept-Language": "en-US, en;q=0.5",
}


def search_product_list(tracker_path, result_path):
    """
    Load tracker file and execute scrape function for all rows and save to output file.

    Parameters
    ----------
    tracker_path: path to csv file that stores all products to scrape
    result_path: path to results csv to store scrapping results to

    Returns
    -------
    None
    """
    if path.exists(result_path):
        search_hist = pd.read_csv(result_path, sep=";")
    else:
        columns = ["date", "code", "url", "title", "price", "stock", "review_score", "review_count"]
        search_hist = pd.DataFrame(columns=columns)
    prod_tracker = pd.read_csv(tracker_path, sep=";")

    for row in prod_tracker.itertuples():
        search_hist = search_hist.append(scrape_infos(row.url, row.code, row.Index), sort=False)

    search_hist.to_csv(result_path, index=False, sep=";")


def scrape_infos(url, code, i):
    """
    Scrape informations from amazon website using soup

    Parameters
    ----------
    url : the url of the amazon website that should be scraped
    code : product code

    Returns
    -------
    pandas data frame with this columns:
        "date"
        "code"
        "url"
        "title"
        "price"
        "stock"
        "review_score"
        "review_count"
    """

    page = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(page.content, features="lxml")

    return pd.DataFrame(
        {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "code": code,
            "url": url,
            "title": scrape_name(soup),
            "price": scrape_price(soup),
            "stock": scrape_stock(soup),
            "review_score": scrape_review_score(soup),
            "review_count": scrape_review_count(soup),
        },
        index=[i],
    )


def scrape_name(soup_object):
    try:
        name = soup_object.find(id="productTitle").get_text().strip()
    except:  # noqa E722
        name = ""
    return name


def scrape_price(soup_object):
    try:
        price = float(soup_object.find(id="priceblock_ourprice").get_text().replace("€", "").replace(",", ""))
    except:  # noqa E722
        price = ""
    return price


def scrape_stock(soup_object):
    try:
        soup_object.select("#availability .a-color-state")[0].get_text().strip()
        stock = "Out of Stock"
    except:  # noqa E722
        try:
            soup_object.select("#availability .a-color-price")[0].get_text().strip()
            stock = "Out of Stock"
        except:  # noqa E722
            stock = "Available"
    return stock


def scrape_review_score(soup_object):
    try:
        review_score = float(
            soup_object.select('i[class*="a-icon a-icon-star a-star-"]')[0].get_text().split(" ")[0].replace(",", ".")
        )
    except:  # noqa E722
        try:
            review_score = float(
                soup_object.select('i[class*="a-icon a-icon-star a-star-"]')[1]
                .get_text()
                .split(" ")[0]
                .replace(",", ".")
            )
        except:  # noqa E722
            review_score = ""
    return review_score


def scrape_review_count(soup_object):
    try:
        review_count = int(soup_object.select("#acrCustomerReviewText")[0].get_text().split(" ")[0].replace(".", ""))
    except:  # noqa E722
        try:
            review_count = int(
                soup_object.select("#acrCustomerReviewText")[0].get_text().split(" ")[0].replace(".", "")
            )
        except:  # noqa E722
            review_count = ""
    return review_count


if __name__ == "__main__":
    search_product_list("trackers/tracker.csv", "search_history/search_results.csv")
