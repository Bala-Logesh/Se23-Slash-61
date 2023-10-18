# package imports
from datetime import datetime
import requests
from ebaysdk.finding import Connection
import http.client
import json

# local imports
from scraper.formattr import formatTitle
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# configs

WALMART = {
    "site": "walmart",
    "url": "https://www.walmart.com/search?q=",
    "item_component": "div",
    "item_indicator": {"data-item-id": True},
    "title_indicator": "div span.lh-title",
    "price_indicator": "div.lh-copy",
    "link_indicator": "a",
    "image_indicator": "div.relative img",
}

AMAZON = {
    "site": "amazon",
    "url": "https://www.amazon.com/s?k=",
    "item_component": "div",
    "item_indicator": {"data-component-type": "s-search-result"},
    "title_indicator": "h2 a span",
    "price_indicator": "span.a-price span",
    "link_indicator": "h2 a.a-link-normal",
    # "image_indicator":
}

COSTCO = {
    "site": "costco",
    "url": "https://www.costco.com/CatalogSearch?dept=All&keyword=",
    "item_component": "div",
    "item_indicator": {"class": "product-tile-set"},
    "title_indicator": "span a",
    "price_indicator": "div.price",
    "link_indicator": "span.description a",
    "image_indicator": "img.img-responsive",
}

BESTBUY = {
    "site": "bestbuy",
    "url": "https://www.bestbuy.com/site/searchpage.jsp?st=",
    "item_component": "li",
    "item_indicator": {"class": "sku-item"},
    "title_indicator": "h4",
    "price_indicator": ".pricing-price span",
    "link_indicator": "a.image-link",
    "image_indicator": ".product-image",
}


# .priceView-customer-price span
# -----Working new code implementation for target--------#
def scrape_target(query):
    """Scrape Target's api for data

    Parameters
    ----------
    query: str
        Item to look for in the api

    Returns
    ----------
    items: list
        List of items from the dict
    """

    conn = http.client.HTTPSConnection("redsky.target.com")
    api_url = "/redsky_aggregations/v1/web/plp_search_v2?"
    page = "/s/" + query + "&"
    keyword = query + "&"
    params = {
        "key": "9f36aeafbe60771e321a7cc95a78140772ab3e96&",
        "channel": "WEB&",
        "count": "24&",
        "default_purchasability_filter": "true&",
        "include_sponsored": "true&",
        "keyword": keyword,
        "new_search": "true&",
        "offset": "0&",
        "page": page,
        "platform": "desktop&",
        "pricing_store_id": "1824&",
        "scheduled_delivery_store_id": "1892&",
        "store_ids": "1824,1104,3255,2111,961&",
        "useragent": "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/117.0.0.0+Safari/537.36&",
        "visitor_id": "018B29CF57E90201817F6A983C9DD517&",
        "zip": "27610",
    }
    for i in params:
        api_url = api_url + (i + "=" + params[i])
    conn.request("GET", api_url)
    res = conn.getresponse()
    data = res.read()
    decoded_data = data.decode("utf-8")
    dict_data = json.loads(decoded_data)
    items = []
    for p in dict_data["data"]["search"]["products"]:
        item = {
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "title": formatTitle(p["item"]["product_description"]["title"]),
            "price": str(p["price"]["formatted_current_price"]),
            "website": "target",
            "link": p["item"]["enrichment"]["buy_url"],
            "image": p["item"]["enrichment"]["images"]["primary_image_url"],
        }
        items.append(item)
    return items


def scrape_ebay(query):
    """Scrape Target's api for data

    Parameters
    ----------
    query: str
        Item to look for in the api

    Returns
    ----------
    items: list
        List of items from the dict
    """

    EBAY_APP = "BradleyE-slash-PRD-2ddd2999f-2ae39cfa"

    try:
        api = Connection(appid=EBAY_APP, config_file=None, siteid="EBAY-US")
        response = api.execute("findItemsByKeywords", {"keywords": query})
    except ConnectionError as e:
        print(e)
        return []

    data = response.dict()

    items = []
    for p in data["searchResult"]["item"]:
        item = {
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "title": formatTitle(p["title"]),
            "price": "$" + p["sellingStatus"]["currentPrice"]["value"],
            "website": "ebay",
            "link": p["viewItemURL"],
            "image": p["galleryURL"],
        }
        items.append(item)

    return items


CONFIGS = [WALMART, AMAZON, COSTCO, BESTBUY]
