import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
from os import link
import unittest

from requests.models import Response
from src.main import getFloatPrice, getItemInfoByItemName, getLowestHighestPriceByWebsite, getVarietyCountByWebsite


class TestMain(unittest.TestCase):

    def test_getFloatPrice(self):
        """
        Assert float price conversion
        """

        assert getFloatPrice("price of the quantity is $200.384") == 200.384
        assert getFloatPrice("$10.0$") == 10.0
        assert getFloatPrice("") == 0
    
    def test_getItemInfoByItemName(self):
        # building argument
        item_name = "chair"
        order_by_col = ""
        reverse = False

        args = {
            'search': item_name,
            'sort': 'pr' if order_by_col == 'price' else 'pr',
            'des': reverse,
            'num': 1
        }

        response = ['walmart', 'costco', 'bestbuy', 'ebay']
        # response = ['amazon', 'walmart', 'target', 'costco', 'bestbuy', 'ebay']

        itemList = getItemInfoByItemName(args)
        for item in itemList:
            assert item['website'] in response

    def test_getVarietyCountByWebsite(self):
        itemList = [
            {'timestamp': '29/11/2021 11:46:26', 'title': 'HOMEFUN Ergonomic Office Chair, High Bac...', 'price': '$97.98', 'link': 'www.amazon.com/HOMEFUN-Ergonomic-Adjustable-Armrests-Support/dp/B084WWQB5B/ref=sr_1_1?keywords=chair&qid=1638204385&sr=8-1', 'website': 'amazon'}, 
            {'timestamp': '29/11/2021 11:46:28', 'title': 'Big Joe Milano Bean Bag Chair, Multiple ...', 'price': 'From $48.13', 'link': 'www.walmart.comhttps://wrd.walmart.com/track?pltfm=desktop&tax=4044_103150_97116_91853&rdf=1&plmt=sp-search-middle~desktop~&eventST=click&spQs=apqgqDEG00Gk_QH7Y98s-tvzD2GJBtYRHuyrCs-NV8UWvHysqbYcLsclYVXrTItsxT99dj59OB3kUD_JhC3RyHy-pCq4J6WjLiQcT_qrqQA&pos=1&pgId=chair&bt=1&adUid=ZavTQ7x_M1eGlAtdVKJy6__X2-ZoZz6XZJJn&storeId=1372&mloc=sp-search-middle&pt=search&rd=https%3A%2F%2Fwww.walmart.com%2Fip%2FBig-Joe-Milano-Bean-Bag-Chair-Blue%2F51744431%3Fathbdg%3DL1800', 'website': 'walmart'}, 
            {'timestamp': '29/11/2021 11:46:29', 'title': 'Steel Folding Chair Black - PDG', 'price': '$11.99', 'website': 'target', 'link': 'https://www.target.com/p/steel-folding-chair-black-pdg/-/A-14777780'}, 
            {'timestamp': '29/11/2021 11:46:30', 'title': 'Respawn Gaming Chair', 'price': '$229.99', 'link': 'https://www.costco.com/respawn-gaming-chair.product.100388800.html', 'website': 'costco'}, 
            {'timestamp': '29/11/2021 11:46:35', 'title': 'Razer - Iskur Gaming Chair with Built-in...', 'price': '$349.99', 'link': 'www.bestbuy.com/site/razer-iskur-gaming-chair-with-built-in-lumbar-support-black/6476898.p?skuId=6476898', 'website': 'bestbuy'}, 
            {'timestamp': '29/11/2021 11:46:36', 'title': 'Steelcase Leap V2 Chair,  -Open Box- Ful...', 'price': '$329.11', 'website': 'ebay', 'link': 'https://www.ebay.com/itm/Steelcase-Leap-V2-Chair-Open-Box-Fully-Loaded-Black-Fabric-/121882349228'}
            ]
        answer = {'amazon': 1, 'walmart': 1, 'target': 1, 'costco': 1, 'bestbuy': 1, 'ebay': 1}

        response = getVarietyCountByWebsite(itemList)
        assert response['amazon'] == answer['amazon'] and response['walmart'] == answer['walmart'] and response['target'] == answer['target'] and response['costco'] == answer['costco'] and response['bestbuy'] == answer['bestbuy'] and response['ebay'] == answer['ebay']

    def test_getLowestHighestPriceByWebsite(self):
        itemList = [
            {'timestamp': '29/11/2021 11:46:26', 'title': 'HOMEFUN Ergonomic Office Chair, High Bac...', 'price': '$97.98', 'link': 'www.amazon.com/HOMEFUN-Ergonomic-Adjustable-Armrests-Support/dp/B084WWQB5B/ref=sr_1_1?keywords=chair&qid=1638204385&sr=8-1', 'website': 'amazon'}, 
            {'timestamp': '29/11/2021 11:46:28', 'title': 'Big Joe Milano Bean Bag Chair, Multiple ...', 'price': 'From $48.13', 'link': 'www.walmart.comhttps://wrd.walmart.com/track?pltfm=desktop&tax=4044_103150_97116_91853&rdf=1&plmt=sp-search-middle~desktop~&eventST=click&spQs=apqgqDEG00Gk_QH7Y98s-tvzD2GJBtYRHuyrCs-NV8UWvHysqbYcLsclYVXrTItsxT99dj59OB3kUD_JhC3RyHy-pCq4J6WjLiQcT_qrqQA&pos=1&pgId=chair&bt=1&adUid=ZavTQ7x_M1eGlAtdVKJy6__X2-ZoZz6XZJJn&storeId=1372&mloc=sp-search-middle&pt=search&rd=https%3A%2F%2Fwww.walmart.com%2Fip%2FBig-Joe-Milano-Bean-Bag-Chair-Blue%2F51744431%3Fathbdg%3DL1800', 'website': 'walmart'}, 
            {'timestamp': '29/11/2021 11:46:29', 'title': 'Steel Folding Chair Black - PDG', 'price': '$11.99', 'website': 'target', 'link': 'https://www.target.com/p/steel-folding-chair-black-pdg/-/A-14777780'}, 
            {'timestamp': '29/11/2021 11:46:30', 'title': 'Respawn Gaming Chair', 'price': '$229.99', 'link': 'https://www.costco.com/respawn-gaming-chair.product.100388800.html', 'website': 'costco'}, 
            {'timestamp': '29/11/2021 11:46:35', 'title': 'Razer - Iskur Gaming Chair with Built-in...', 'price': '$349.99', 'link': 'www.bestbuy.com/site/razer-iskur-gaming-chair-with-built-in-lumbar-support-black/6476898.p?skuId=6476898', 'website': 'bestbuy'}, 
            {'timestamp': '29/11/2021 11:46:36', 'title': 'Steelcase Leap V2 Chair,  -Open Box- Ful...', 'price': '$329.11', 'website': 'ebay', 'link': 'https://www.ebay.com/itm/Steelcase-Leap-V2-Chair-Open-Box-Fully-Loaded-Black-Fabric-/121882349228'}
            ]
        
        lowest_price_ans = {
            'amazon': 0,
            'walmart': 48.13,
            'target': 0,
            'costco': 229.99,
            'bestbuy': 349.99,
            'ebay': 329.11
        }

        lowest_price_link_ans = {
            'amazon': "www.amazon.com/HOMEFUN-Ergonomic-Adjustable-Armrests-Support/dp/B084WWQB5B/ref=sr_1_1?keywords=chair&qid=1638204385&sr=8-1",
            'walmart': "www.walmart.comhttps://wrd.walmart.com/track?pltfm=desktop&tax=4044_103150_97116_91853&rdf=1&plmt=sp-search-middle~desktop~&eventST=click&spQs=apqgqDEG00Gk_QH7Y98s-tvzD2GJBtYRHuyrCs-NV8UWvHysqbYcLsclYVXrTItsxT99dj59OB3kUD_JhC3RyHy-pCq4J6WjLiQcT_qrqQA&pos=1&pgId=chair&bt=1&adUid=ZavTQ7x_M1eGlAtdVKJy6__X2-ZoZz6XZJJn&storeId=1372&mloc=sp-search-middle&pt=search&rd=https%3A%2F%2Fwww.walmart.com%2Fip%2FBig-Joe-Milano-Bean-Bag-Chair-Blue%2F51744431%3Fathbdg%3DL1800",
            'target': "https://www.target.com/p/steel-folding-chair-black-pdg/-/A-14777780",
            'costco': "https://www.costco.com/respawn-gaming-chair.product.100388800.html",
            'bestbuy': "www.bestbuy.com/site/razer-iskur-gaming-chair-with-built-in-lumbar-support-black/6476898.p?skuId=6476898",
            'ebay': "https://www.ebay.com/itm/Steelcase-Leap-V2-Chair-Open-Box-Fully-Loaded-Black-Fabric-/121882349228"
            }

        highest_price_ans = {
            'amazon': 97.98,
            'walmart': 48.13,
            'target': 11.99,
            'costco': 229.99,
            'bestbuy': 349.99,
            'ebay': 329.11}

        highest_price_link_ans = {
            'amazon': "www.amazon.com/HOMEFUN-Ergonomic-Adjustable-Armrests-Support/dp/B084WWQB5B/ref=sr_1_1?keywords=chair&qid=1638204385&sr=8-1",
            'walmart': "www.walmart.comhttps://wrd.walmart.com/track?pltfm=desktop&tax=4044_103150_97116_91853&rdf=1&plmt=sp-search-middle~desktop~&eventST=click&spQs=apqgqDEG00Gk_QH7Y98s-tvzD2GJBtYRHuyrCs-NV8UWvHysqbYcLsclYVXrTItsxT99dj59OB3kUD_JhC3RyHy-pCq4J6WjLiQcT_qrqQA&pos=1&pgId=chair&bt=1&adUid=ZavTQ7x_M1eGlAtdVKJy6__X2-ZoZz6XZJJn&storeId=1372&mloc=sp-search-middle&pt=search&rd=https%3A%2F%2Fwww.walmart.com%2Fip%2FBig-Joe-Milano-Bean-Bag-Chair-Blue%2F51744431%3Fathbdg%3DL1800",
            'target': "https://www.target.com/p/steel-folding-chair-black-pdg/-/A-14777780",
            'costco': "https://www.costco.com/respawn-gaming-chair.product.100388800.html",
            'bestbuy': "www.bestbuy.com/site/razer-iskur-gaming-chair-with-built-in-lumbar-support-black/6476898.p?skuId=6476898",
            'ebay': "https://www.ebay.com/itm/Steelcase-Leap-V2-Chair-Open-Box-Fully-Loaded-Black-Fabric-/121882349228"}

        lowest_price_dict, lowest_price_link_dict,  highest_price_dict, highest_price_link_dict = getLowestHighestPriceByWebsite(itemList)

        assert lowest_price_dict == lowest_price_ans and lowest_price_link_dict == lowest_price_link_ans and highest_price_dict == highest_price_ans and highest_price_link_dict == highest_price_link_ans
