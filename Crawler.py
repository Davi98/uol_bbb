from datetime import datetime
from log import log
from Browser import Browser
import re


class Crawler:

    def __init__(self,browser):
        self.browser = browser
    
    def get_dom(self):
       self.browser.goto()
       element = self.browser.driver.find_element_by_xpath("//*")
       return element

    def crawl(self):
        dom = self.get_dom()
        data = self.parse(dom)
        return data

    def parse(self,dom):
        data= {}
        names = []
        percentages = []
       
        participants = dom.find_elements_by_xpath("//span[@class='answer-title']")
        participants_number = dom.find_elements_by_xpath("//span[@class='perc-value ng-binding']")
        total_votes = dom.find_element_by_xpath("//span[@class='total-votes  ng-binding']").get_attribute("innerText")
        for i in range(len(participants)):
            names.append(participants[i].get_attribute("innerText"))
            percentages.append(participants_number[i].get_attribute("innerText"))
       
        data = {
            "names": names,
            "percentages": percentages,
            "total_votes": total_votes,
            "create_date" : datetime.utcnow()         
        }       


        return data