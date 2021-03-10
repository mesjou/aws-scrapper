from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup

# http://www.networkinghowtos.com/howto/common-user-agent-list/
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) \
    Version/14.0.3 Safari/605.1.15",
    "Accept-Language": "en-US, en;q=0.5",
}


def search_product_list():
    """
    This function lods a csv file named TRACKER_PRODUCTS.csv, with headers: [url, code, buy_below]
    It looks for the file under in ./trackers

    It also requires a file called SEARCH_HISTORY.xslx under the folder ./search_history to start saving the results.
    An empty file can be used on the first time using the script.

    Both the old and the new results are then saved in a new file named SEARCH_HISTORY_{datetime}.xlsx
    This is the file the script will use to get the history next time it runs.

    Parameters
    ----------
    interval_count : TYPE, optional
        DESCRIPTION. The default is 1. The number of iterations you want the script to run a search on the full list.
    interval_hours : TYPE, optional
        DESCRIPTION. The default is 6.

    Returns
    -------
    New .xlsx file with previous search history and results from current search

    """
    prod_tracker = pd.read_csv("trackers/tracker.csv", sep=";")
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    search_hist = pd.read_csv("search_history/search_results.csv")

    for row in prod_tracker.itertuples():
        page = requests.get(row.url, headers=HEADERS)
        soup = BeautifulSoup(page.content, features="lxml")

        # find product name
        try:
            title = soup.find(id="productTitle").get_text().strip()
        except:  # noqa E722
            title = ""

        # find product price
        try:
            price = float(soup.find(id="priceblock_ourprice").get_text().replace("€", "").replace(",", ""))
        except:  # noqa E722
            price = ""

        # find review
        try:
            review_score = float(
                soup.select('i[class*="a-icon a-icon-star a-star-"]')[0].get_text().split(" ")[0].replace(",", ".")
            )
            review_count = int(soup.select("#acrCustomerReviewText")[0].get_text().split(" ")[0].replace(".", ""))
        except:  # noqa E722
            try:
                review_score = float(
                    soup.select('i[class*="a-icon a-icon-star a-star-"]')[1].get_text().split(" ")[0].replace(",", ".")
                )
                review_count = int(soup.select("#acrCustomerReviewText")[0].get_text().split(" ")[0].replace(".", ""))
            except:  # noqa E722
                review_score = ""
                review_count = ""

        # check availability
        try:
            soup.select("#availability .a-color-state")[0].get_text().strip()
            stock = "Out of Stock"
        except:  # noqa E722
            try:
                soup.select("#availability .a-color-price")[0].get_text().strip()
                stock = "Out of Stock"
            except:  # noqa E722
                stock = "Available"

        log = pd.DataFrame(
            {
                "date": now,
                "code": row.code,
                "url": row.url,
                "title": title,
                "price": price,
                "stock": stock,
                "review_score": review_score,
                "review_count": review_count,
            },
            index=[row.Index],
        )
        print(log)
        search_hist = search_hist.append(log, sort=False)

    search_hist.to_csv("search_history/search_results.csv".format(now), index=False)


if __name__ == "__main__":
    search_product_list()
