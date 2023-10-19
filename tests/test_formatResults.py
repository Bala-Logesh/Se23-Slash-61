"""
Copyright (C) 2021 SE Slash - All Rights Reserved
You may use, distribute and modify this code under the
terms of the MIT license.
You should have received a copy of the MIT license with
this file. If not, please write to: secheaper@gmail.com

"""

import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import src.scraper.formattr as formatter
from bs4 import BeautifulSoup

def test_sortList():
    """
    Checks the sortList function
    """
    arr = [{"price":"$10"}, {"price":"$20"}, {"price":"$0"}]
    ansArr = [{"price":"$0"}, {"price":"$10"}, {"price":"$20"}]
    revAnsArr = [{"price":"$20"}, {"price":"$10"}, {"price":"$0"}]
    assert formatter.sortList(arr, "pr", False) == ansArr
    assert formatter.sortList(arr, "pr", True) == revAnsArr

def test_formatResults():
    """
    Checks the formatResults function
    """
    timestamp='timestamp'
    titles = [BeautifulSoup('<div class="someclass">title  </div>', "html.parser")]
    prices = [BeautifulSoup('<div class="someclass">$0.99  </div>', "html.parser")]
    links = [{"href":"/bestbuy"}]
    image="<img alt='HP - 17.3 HD+ Laptop - AMD Ryzen 3 7320U - 8GB Memory - 256GB SSD - Natural Silver - Front_Zoom' class=product-image src=https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6554/6554443_sd.jpg;maxHeight=200;maxWidth=300 srcset=https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6554/6554443_sd.jpg;maxHeight=400;maxWidth=600 2x/>"

    product = formatter.formatResult("bestbuy", titles, prices, links,image)
    ans = {"timestamp":"timestamp","title":"title", "price":"$0.99", "website":"bestbuy","links":"www.bestbuy.com/bestbuy","image":"https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6554/6554443_sd.jpg;maxHeight=200;maxWidth=300"}

    assert product["title"] == ans["title"] and product["price"] == ans["price"]  and product["website"] == ans["website"] and product["link"]==ans["links"] and product["image"] ==ans["image"]