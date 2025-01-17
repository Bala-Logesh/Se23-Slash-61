# package imports
from bs4 import BeautifulSoup
import requests

# local imports
import scraper.formattr as form
from scraper.configs import AMAZON, WALMART, COSTCO, BESTBUY, scrape_ebay, scrape_target


def httpsGet(URL):
    """makes HTTP called to the requested URL with custom headers

    Parameters
    ----------
    URL: str
        URL we are sending request to

    Returns
    ----------
    soup: str
        HTML of page we requested
    """
    headers = {
        "User-Agent": "Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/117.0.0.0+Safari/537.36",    
        'Accept-Encoding': 'gzip, deflate',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'no-cache'
    }
    s = requests.Session()
    page = s.get(URL, headers=headers)
    if page.status_code == 200:
        soup1 = BeautifulSoup(page.content, 'html.parser')
        return BeautifulSoup(soup1.prettify(), 'html.parser')
    else:
        # TODO add logger
        return None
    
def congifMappingFunction(url):
    second_part = url.split(".")[1]

    # firstcharacter after'.'
    w = second_part[0]
    # if w == "a":
    #     return AMAZON
    if w == "w":
        return WALMART
    elif w == "c":
        return COSTCO
    elif w == "b":
        return BESTBUY
    elif w == "t":
        # https://www.target.com/s?searchTerm=mobile+phone&tref=typeahead%7Cterm%7Cmobile+phone%7C%7C%7Chistory
        start_index = url.find("=")
        end_index = url.find("&")
        substring = url[start_index + 1 : end_index]
        return scrape_target(substring)
    elif w == "e":
        # https://www.ebay.com/sch/i.html?_nkw=keyboard
        s_index = url.find("=")
        sub = url[s_index:]
        return scrape_ebay(sub)



def search(query, config):
    """Scrape the given config for a specific item

    Parameters
    ----------
    query: str
        Query of item we are looking for
    config: dict
        Configuration for site we are scraping

    Returns
    ----------
    products: list
        List of items returned from website
    """
    if config['site'] == 'costco':
        query = form.formatSearchQueryForCostco(query)
    else:
        query = form.formatSearchQuery(query)
    URL = config['url'] + query

    # fetch url
    page = httpsGet(URL)
    if not page:
        return []

    # begin parsing page content
    results = page.find_all(config['item_component'], config['item_indicator'])
    products = []
    for res in results:
        title = res.select(config["title_indicator"])
        if title == []:
            continue
        price = res.select(config["price_indicator"])
        if price == []:
            continue
        link = res.select(config["link_indicator"])
        image = res.select(config["image_indicator"])
        tags_as_strings = [str(tag) for tag in image]
        #print(tags_as_strings)
        image = "".join(tags_as_strings)
        # url_start=image.find("src=")
        # url_end=image.find(" srcset=")
        # img=image[url_start+4:url_end]
        #print(img)
        product = form.formatResult(config["site"], title, price, link, tags_as_strings)
        products.append(product)
    return products


def scrape(args, scrapers):
    """Conduct scraping of sites based on scrapers

    Parameters
    ----------
    args: dict
        Dictionary of arguments used for scraping

        search : str [query to search on]
        sort : str [sort by column name ; pr - price]
        des : boolean [True for reverse, False for asc]
        num : number of rows in the output
    scrapers: list
        List of scrapers to use

    Returns
    ----------
    overall: list
        List of items returned from scrapers
    """

    query = args['search']

    overall = []
    for scraper in scrapers:
        if scraper == 'walmart':
            local = search(query, WALMART)
        elif scraper == 'amazon':
            local = search(query, AMAZON)
        elif scraper == 'target':
            local = scrape_target(query)
        elif scraper == 'ebay':
            local = scrape_ebay(query)
        elif scraper == 'costco':
            local = search(query, COSTCO)
        elif scraper == 'bestbuy':
            local = search(query, BESTBUY)
        else:
            continue
        # TBD : move number of items fetched to global level ?
        for sort_by in args['sort']:
            local = form.sortList(local, sort_by, args['des'])[:args.get('num', len(local))]
        overall.extend(local)

    for sort_by in args['sort']:
        overall = form.sortList(overall, sort_by, args['des'])

    return overall

def findConfig(site):
    if site == 'amazon':
        return AMAZON
    elif site == 'walmart':
        return BESTBUY
    elif site == 'costco':
        return COSTCO
    elif site == 'target':
        return scrape_target
    elif site == 'bestbuy':
        return BESTBUY
    return scrape_ebay

def scrapeProduct(url,site):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',  # noqa: E501
        'Accept-Encoding': 'gzip, deflate',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'no-cache'
    }
    s = requests.Session()
    page = s.get(url, headers=headers)
    if page.status_code == 200:
        if site == 'walmart':    #logic added only for walmart, etend for other websites too
            soup = BeautifulSoup(page.content, "html.parser")
            res = soup.find("span",{"itemprop":"price"})
            price = res.text.strip()
            return price
    else:
        # TODO add logger
        print('Failure')
    return