import os
import sys
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import src.scraper.formattr as formatter
from bs4 import BeautifulSoup

def test_ImgURL():
    titles = [BeautifulSoup('<div class="someclass">title  </div>', "html.parser")]
    prices = [BeautifulSoup('<div class="someclass">$0.99  </div>', "html.parser")]
    links = [{"href":"/walmart"}]
    images=""

    product = formatter.formatResult("bestbuy", titles, prices, links,images)
    ans = {"title":"title", "price":"$0.99", "website":"bestbuy","links":"www.example.com/walmart"}
    assert formatter.formatimageURL("<img alt='HP - 17.3 HD+ Laptop - AMD Ryzen 3 7320U - 8GB Memory - 256GB SSD - Natural Silver - Front_Zoom' class=product-image src=https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6554/6554443_sd.jpg;maxHeight=200;maxWidth=300 srcset=https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6554/6554443_sd.jpg;maxHeight=400;maxWidth=600 2x/>","bestbuy")=="https://pisces.bbystatic.com/image2/BestBuy_US/images/products/6554/6554443_sd.jpg"
    assert formatter.formatimageURL("<img alt=Pentel RSVP Ballpoint Pen, (0.7 mm) Fine Line, Black, 2 Pack class=absolute top-0 left-0 data-testid= productTileImage height="" id=is-0-productImage-9 loading=lazy src=https://i5.walmartimages.com/asr/c7b16fbb-7664-408b-ad27-e8c4d2747866.fc186df01b94a93553360faa7c7dfff2.jpeg?odnHeight=784&amp;odnWidth=580&amp;odnBg=FFFFFF srcset=https://i5.walmartimages.com/asr/c7b16fbb-7664-408b-ad27-e8c4d2747866.fc186df01b94a93553360faa7c7dfff2.jpeg?odnHeight=392&amp;odnWidth=290&amp;odnBg=FFFFFF 1x, https://i5.walmartimages.com/asr/c7b16fbb-7664-408b-ad27-e8c4d2747866.fc186df01b94a93553360faa7c7dfff2.jpeg?odnHeight=784&amp;odnWidth=580&amp;odnBg=FFFFFF 2x width=""/><img alt=Walmart Plus class=flex height=20 loading=lazy src=//i5.walmartimages.com/dfw/63fd9f59-ac39/29c6759d-7f14-49fa-bd3a-b870eb4fb8fb/v1/wplus-icon-blue.svg width=20","walmart")=="https://i5.walmartimages.com/asr/c7b16fbb-7664-408b-ad27-e8c4d2747866.fc186df01b94a93553360faa7c7dfff2.jpeg"
    assert formatter.formatimageURL("<img alt=MacBook Pro (14-inch) - Apple M1 Pro Chip with 8-Core CPU and 14-Core GPU, 512GB SSD (2021) automation-id=productImageLink_23 class=img-responsive src=https://images.costco-static.com/ImageDelivery/imageService?profileId=12026540&amp;imageId=100713178-847__1&amp;recipeName=350 width=350  height=350 onerror=this.onerror='';this.src='/wcsstore/CostcoGLOBALSAS/images/unavailable_350.png' width=350/>","costco")=="=https://images.costco-static.com/ImageDelivery/imageService?profileId=12026540&amp;imageId=100713178-847__1&amp;recipeName=350"
    
