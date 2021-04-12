import os
from Browser import Browser
from Crawler import Crawler
from Mongo import Mongo

browser = Browser()
crawler = Crawler(browser)

mongo_uri = os.environ['MONGO_URI']
mongo = Mongo(mongo_uri)
data = crawler.crawl()
mongo.save(data)
