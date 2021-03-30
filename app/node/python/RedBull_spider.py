# -*- coding: utf-8 -*-
from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
import json, ast
from pprint import pprint
import sys
from time import sleep


class RedbullSpiderSpider(scrapy.Spider):
    name = 'RedBull-spider'
    allowed_domains = ['redbull.com']
    start_urls = ['https://basement.redbull.com/university-api/entrants']

    def parse(self, response):


        result = json.loads(response.text)
        List = []
        registrations  = result["registrations"]

	

       	for i in range(len(registrations)):
            if(registrations[i]["country"] == "Bosnia and Herzegovina"):
                List.append(registrations[i])
		
        sortedList = sorted(List, key=lambda k: k['voteCount'],reverse=True)
	
	#newList = eval(json.dumps(sortedList))
        print(json.dumps(sortedList))
        sys.stdout.flush()
	#with open('data.json','w') as outfile:
	    #json.dump(sortedList,outfile)
                #return sortedList

configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
runner = CrawlerRunner()

d = runner.crawl(RedbullSpiderSpider)
d.addBoth(lambda _: reactor.stop())
reactor.run() # the script will block here until the crawling is finished

sleep(1000)





