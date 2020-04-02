
from __future__ import print_function
import json
import re
import logging

import scrapy
from scrapy.http.request import Request
# from spider_project.items import SpiderProjectItem

from six.moves.urllib import parse

class Linkedin_Site_Spider(scrapy.Spider):
    name = "linkedin_spider"
    currentDepth = 1
    accountName = 'microsoft'

    def start_requests(self):
        """
        Start scraping with first request
        """
        newUrl = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=" + self.accountName + "&start=0"
        yield Request(
            url = newUrl,
            callback=self.parse_list_page
        )

    def parse_list_page(self, response):
        """
        Link parsing example (25 records/page)
        https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=salesforce
        https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=salesforce&start=25
        """
        next_link = response.url
        next_link = next_link[:next_link.find(self.accountName)] + self.accountName + '&start=' + str(25 * self.currentDepth)
        yield Request(
            url= next_link,
            callback=self.parse_list_page
        )
        self.extract_product(response)
        self.currentDepth += 1
            

    def extract_product(self, response):
        jobDivs = response.css('div.result-card__contents')
        for index, job in enumerate(jobDivs):
            title = job.css('h3.job-result-card__title::text').get()
            company = job.css('a.job-result-card__subtitle-link::text').get()
            timeSincePost =  job.css('time::text').get()
            newPost = dict(
                        title=title,
                        company=company, 
                        timeSincePost=timeSincePost
                        )
            #un-capitalize company name results
            if self.accountName==company.lower():
                #push into database
                print(newPost)
                    
        
