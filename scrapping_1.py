from lxml import html
import csv,os,json
import requests
import re
from exceptions import ValueError
from time import sleep

def test(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    proxies = {'http' : 'http://10.10.0.0:0000',
          'https': 'http://120.10.0.0:0000'}
    page = requests.get(url,proxies=proxies, headers=headers)
    doc = html.fromstring(page.content)
    print(doc)

def AmzonParser(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    proxies = {'https' : 'https://142.163.212.82'}
    page = requests.get(url,proxies=proxies, headers=headers)
    while True:
        sleep(3)
        try:
            doc = html.fromstring(page.content)
            XPATH_SALE_PRICE = '//span[contains(@id,"ourprice") or contains(@id,"saleprice")]/text()'
            XPATH_SHIPPING = '//self::span[contains(text(),"Shipping")]//text()'
            XPATH_ORIGINAL_PRICE = '//td[contains(text(),"List Price") or contains(text(),"M.R.P") or contains(text(),"Price")]/following-sibling::td/text()'
            XPATH_AVAILABILITY = '//div[@id="availability"]//text()'

            RAW_SALE_PRICE = doc.xpath(XPATH_SALE_PRICE)
            RAW_SHIPPING = doc.xpath(XPATH_SHIPPING)
            RAw_AVAILABILITY = doc.xpath(XPATH_AVAILABILITY)
            SALE_PRICE = ' '.join(''.join(RAW_SALE_PRICE).split()).strip() if RAW_SALE_PRICE else None
            SHIPPING = ''.join(RAW_SHIPPING).strip()
            SHIPPING_DETAIL = re.findall('(FREE Shipping)', SHIPPING)
            SHIPPING_PRICE = re.findall('(\$[0-9]+\.[0-9])\w+',SHIPPING)
            AVAILABILITY = ''.join(RAw_AVAILABILITY).strip() if RAw_AVAILABILITY else None

            if len(SHIPPING_DETAIL) == 0:
                SHIPPING_DETAIL = 0
            else:
                SHIPPING_DETAIL = 1
            if len(SHIPPING_PRICE) == 0:
                SHIPPING_PRICE = None
            else:
                SHIPPING_PRICE = SHIPPING_PRICE[0]
                SHIPPING_PRICE = float(SHIPPING_PRICE[1:])
                SALE_PRICE = float(SALE_PRICE[1:]) + SHIPPING_PRICE

            if page.status_code!=200:
                raise ValueError('captha')
            data = {
                    'SALE_PRICE':SALE_PRICE,
                    'SHIPPING_PRICE':SHIPPING_PRICE,
                    'SHIPPING_DETAIL':SHIPPING_DETAIL,
                    'AVAILABILITY':AVAILABILITY,
                    }

            return data
        except Exception as e:
            print e

def ReadAsin():
    # AsinList = csv.DictReader(open(os.path.join(os.path.dirname(__file__),"Asinfeed.csv")))
    AsinList = ['B0046UR4F4',
    'B00JGTVU5A',
    'B00GJYCIVK',
    'B00EPGK7CQ']
    extracted_data = []
    for i in AsinList:
        url = "http://www.amazon.com/dp/"+i
        print "Processing: "+url
        extracted_data.append(AmzonParser(url))
        sleep(1)
    print(extracted_data)

def SingleURL():
    url =  "https://www.amazon.com/Panasonic-Headphones-RP-TCM120-K-Ergonomic-Comfort-Fit/dp/B003EM8008/ref=sr_1_7?ie=UTF8&qid=1542160631&sr=8-7&keywords=headphone&dpID=41gcvddg7KL&preST=_SX300_QL70_&dpSrc=srch"
    content = AmzonParser(url)
    print(content)

if __name__ == "__main__":
    SingleURL()
