# package imports
import uvicorn
from typing import Optional
from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.responses import FileResponse
from pydantic import BaseModel
import csv

# local imports
import scraper.scraper as scr

#added by vdeenda
from models import UserCreate,Item,SessionLocal,engine,WatchList,ItemValue
from datetime import datetime,timedelta
from sqlalchemy import select,distinct
from celery import Celery
import scraper.formattr as form
from scraper.scraper import httpsGet,findConfig,scrapeProduct
import requests

# response type define
class jsonScraps(BaseModel):
    timestamp: str
    title: str
    price: str
    website: str
    link: Optional[str] = None


# response type for variety count api
class analysisVarietyCountJson(BaseModel):
    website: str
    count: int


# response type for top cosy value per item over the website
class analysisTopCostJson(BaseModel):
    website: str
    lowest_price: float
    lowest_price_link: str
    highest_price: float
    highest_price_link: str


app = FastAPI()
celeryapp = Celery('main', broker='redis://localhost:6379/0')
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    '''Get documentation of API

    Parameters
    ----------
    None

    Returns
    ----------
    documentation redirect
    '''
    response = RedirectResponse(url='/redoc')
    return response


@app.get("/{site}/{item_name}", response_model=List[jsonScraps])
async def search_items_API(
    site: str,
    item_name: str,
    relevant: Optional[str] = None,
    order_by_col: Optional[str] = None,
    reverse: Optional[bool] = False,
    listLengthInd: Optional[int] = 10,
    export: Optional[bool] = False
):
    '''Wrapper API to fetch AMAZON, WALMART and TARGET query results

    Parameters
    ----------
    item_name: string of item to be searched

    Returns
    ----------
    itemListJson: JSON List
        list of search results as JSON List
    '''
    # logging in file
    file = open("logger.txt", "a")
    file.write(site +' query:' + str(item_name)+'\n')

    # building argument
    args = {
        'search': item_name,
        'sort': 'pr' if order_by_col == 'price' else 'pr',  # placeholder TDB
        'des': reverse,  # placeholder TBD
        'num': listLengthInd,
        'relevant': relevant
    }

    scrapers = []

    if site == 'az' or site == 'all':
        scrapers.append('amazon')
    if site == 'wm' or site == 'all':
        scrapers.append('walmart')
    if site == 'tg' or site == 'all':
        scrapers.append('target')
    if site == 'cc' or site == 'all':
        scrapers.append('costco')
    if site == 'bb' or site == 'all':
        scrapers.append('bestbuy')
    if site == 'eb' or site == 'all':
        scrapers.append('ebay')

    # calling scraper.scrape to fetch results
    itemList = scr.scrape(args=args, scrapers=scrapers)

    if not export and len(itemList) > 0:
        file.close()
        return itemList
    elif len(itemList) > 0:
        # returning CSV
        with open('slash.csv', 'w', encoding='utf8', newline='') as f:
            dict_writer = csv.DictWriter(f, itemList[0].keys())
            dict_writer.writeheader()
            dict_writer.writerows(itemList)
        return FileResponse('slash.csv', media_type='application/octet-stream', filename='slash_'+item_name+'.csv')
    else:
        # No results
        return None


@app.get("/analysis/varietyCount/all/{item_name}", response_model=List[analysisVarietyCountJson])
async def items_variety_count_analysis_API(
    item_name: str,
    order_by_col: Optional[str] = None,
    reverse: Optional[bool] = False
):
    ''' Wrapper API to fetch the count of number of varieties for a particular item found  in 
    AMAZON, WALMART, TARGET, COSTCO, BESTBUY, EBAY query results
    Parameters
    ----------
    item_name: string of item to be searched

    Returns
    ----------
    itemListJson: JSON List
        list of count of varieties of the item across all websites as JSON List
    '''

    # building argument
    args = {
        'search': item_name,
        'sort': 'pr' if order_by_col == 'price' else 'pr',  # placeholder TDB
        'des': reverse,  # placeholder TBD
    }

    itemList = getItemInfoByItemName(args)

    variety_count_dict = getVarietyCountByWebsite(itemList)

    variety_count_list = []
    for key, value in variety_count_dict.items():
        temp = {
            "website": key,
            "count": value
        }
        variety_count_list.append(temp)

    return variety_count_list


@app.get("/analysis/topCost/all/{item_name}", response_model=List[analysisTopCostJson])
async def items_top_cost_analysis_API(
    item_name: str,
    order_by_col: Optional[str] = None,
    reverse: Optional[bool] = False
):
    ''' Wrapper API to fetch the top lowest and highest price of item found in 
    AMAZON, WALMART, TARGET, COSTCO, BESTBUY, EBAY query results
    Parameters
    ----------
    item_name: string of item to be searched

    Returns
    ----------
    itemListJson: JSON List
        list of lowest and highest price of the item across all websites as JSON List
    '''

    # building argument
    args = {
        'search': item_name,
        'sort': 'pr' if order_by_col == 'price' else 'pr',  # placeholder TDB
        'des': reverse,  # placeholder TBD
    }

    itemList = getItemInfoByItemName(args)

    lowest_price_dict, lowest_price_link_dict,  highest_price_dict, highest_price_link_dict = getLowestHighestPriceByWebsite(itemList)

    price__list = []
    for key, value in lowest_price_dict.items():
        website = key
        lowest_price = value
        lowest_price_link = lowest_price_link_dict[key]
        highest_price = highest_price_dict[key]
        highest_price_link = highest_price_link_dict[key]
        temp = {
            "website": website,
            "lowest_price": lowest_price,
            "lowest_price_link": lowest_price_link,
            "highest_price": highest_price,
            "highest_price_link": highest_price_link
        }
        price__list.append(temp)

    return price__list


def getItemInfoByItemName(args):

    scrapers = []
    scrapers.append('amazon')
    scrapers.append('walmart')
    scrapers.append('target')
    scrapers.append('costco')
    scrapers.append('bestbuy')
    scrapers.append('ebay')

    # calling scraper.scrape to fetch results
    itemList = scr.scrape(args=args, scrapers=scrapers)
    return itemList


def getVarietyCountByWebsite(itemList):
    variety_count_dict = {
        'amazon': 0, 'walmart': 0, 'target': 0, 'costco': 0, 'bestbuy': 0, 'ebay': 0
    }

    # iterate and parse the itemlist to create a dict of website vs count
    for item in itemList:
        website = item['website']
        variety_count_dict[website] += 1

    return variety_count_dict


def getLowestHighestPriceByWebsite(itemList):
    lowest_price_dict = {
        'amazon': float('inf'), 'walmart': float('inf'), 'target': float('inf'), 'costco': float('inf'), 'bestbuy': float('inf'), 'ebay': float('inf')
    }

    lowest_price_link_dict = {
        'amazon': "", 'walmart': "", 'target': "", 'costco': "", 'bestbuy': "", 'ebay': ""
    }

    highest_price_dict = {
        'amazon': 0, 'walmart': 0, 'target': 0, 'costco': 0, 'bestbuy': 0, 'ebay': 0
    }

    highest_price_link_dict = {
        'amazon': "", 'walmart': "", 'target': "", 'costco': "", 'bestbuy': "", 'ebay': ""
    }

    for item in itemList:

        if(item['price'] == ''):
            continue
        website = item['website']
        price = getFloatPrice(item['price'])


        if(price < lowest_price_dict[website]):
            lowest_price_dict[website] = price
            lowest_price_link_dict[website] = item['link']
        
        if(price > highest_price_dict[website]):
            highest_price_dict[website] = price
            highest_price_link_dict[website] = item['link']

    return lowest_price_dict, lowest_price_link_dict, highest_price_dict, highest_price_link_dict


def getFloatPrice(price):
    temp = ""
    float_price = 0
    
    for ch in price:
        if (ch >= '0' and ch <= '9') or (ch == '.'):
            temp += ch
    if temp:
        float_price = float(temp)
    return float_price

#Pydantic models for User Registration
class UserRegister(BaseModel):
    username: str
    password: str
    email: str
    confpassword: str

class UserCreatePy(BaseModel):
    username: str
    password: str
    email: str

#api end point for creating user in db
@app.post("/users/",response_model= UserCreatePy) 
async def create_user(user:UserRegister):
    db_user = UserCreate(username=user.username,password=user.password,email=user.email)
    db = SessionLocal()
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()
    return db_user
    
class WatchListPy(BaseModel):
    user_id:int
    price:float
    date:str
    link:str
    site:str


@app.post("/watchlist/")
async def add_item(watchlistitem:WatchListPy):
    date_format = "%d/%m/%Y %H:%M:%S"
    my_date = datetime.strptime(watchlistitem.date, date_format)
    item = Item(link=watchlistitem.link,site = watchlistitem.site,price=watchlistitem.price,date=my_date)
    #If the item is present in Item Master DB don't add
    results = checkItem(item)
    if(len(results)==0):
        db = SessionLocal()
        db.add(item)
        db.commit()
        db.refresh(item)
        db.close()
        addToWatchList(watchlistitem,item.item_id,my_date)
    else:
        addToWatchList(watchlistitem,results[0][0],my_date)
    return "added"

def checkItem(item:Item):
    db = SessionLocal()
    stmt = select(distinct(Item.item_id)).where(Item.link == item.link)
    results = db.execute(stmt).fetchall()
    db.close()
    return results

def addToWatchList(watchlist,item_id_master,my_date):
    db = SessionLocal() 
    item_watchlist = WatchList(user_id=watchlist.user_id,item_id=item_id_master,price=watchlist.price,date=my_date)
    db.add(item_watchlist)
    db.commit()
    db.refresh(item_watchlist)
    db.close()
    return    

def addToItemValue(item_id,price,scrape_time):
    db = SessionLocal()
    stmt = select(ItemValue.price).where(ItemValue.item_id == item_id)
    price_db = stmt.execute(stmt).fetchall()
    scraped_item = ItemValue(item_id = item_id,price = float(price[1:]),date = scrape_time)
    db.add(scraped_item)
    db.commit()
    db.refresh(scraped_item)
    db.close()
    #If the price scraped is less that what we already have, send email
    if price_db < price:
          #send email notif here
          #also you should update the new min value in watchlist table for this item_id
        print('inside email block')
    
    return

#Scheduler task
urlList = set()
@celeryapp.task
def check_database_record():
    #find the item_id associated for watchlist table\
    db = SessionLocal()
    stmt = select(distinct(WatchList.item_id))
    item_id_lists = db.execute(stmt).fetchall()   #list of item ids for which we have to scrape
    for item_id in item_id_lists:
        stmt2 = select(Item.link,Item.site).where(Item.item_id == item_id[0])
        res = db.execute(stmt2).fetchall()
        urlList.add((res[0][0],res[0][1],item_id[0]))
    db.close()
    #scrape these links present in urlList
    for url in urlList:
        price = scrapeProduct(url[0],url[1])
        item_id = url[2]
        current_time = datetime.now()
        addToItemValue(item_id,price,current_time)  #adding scraped item to database
    return

celeryapp.conf.beat_schedule = {
    'check-database-record': {
        'task': 'main.check_database_record',
        'schedule': timedelta(seconds=50),
    },
}
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
