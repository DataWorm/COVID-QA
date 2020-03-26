# run 'scrapy runspider BMEL_scraper.py' to scrape data

from datetime import date

import scrapy
from scrapy.crawler import CrawlerProcess


class CovidScraper(scrapy.Spider):
    name = 'bmel_spyder'
    start_urls = ['https://www.bmel.de/DE/Ministerium/_Texte/corona-virus-faq-fragen-antworten.html']

    def transformContent(self, contentNode):
        responseParts = []
        for responsePart in contentNode.xpath('.//text()').getall():
            strippedPart = responsePart.strip()
            if len(strippedPart) > 0:
                responseParts.append(strippedPart)
        return ' '.join(responseParts)
		
    def parse(self, response):
        columns = {
            "question": [],
            "answer": [],
            "answer_html": [],
            "link": [],
            "name": [],
            "source": [],
            "category": [],
            "country": [],
            "region": [],
            "city": [],
            "lang": [],
            "last_update": [],
        }

        categoryName = ""
        question = ""
        print(response.xpath('//body').get())
        print('\n\n')
        for elementPath in response.xpath('//div[@id="content"]/div[@id="main"]/child::node()'):
            tagName = elementPath.xpath('name()').get()
            print(tagName)
            print("Content: "+" ".join(elementPath.xpath('.//text()').getall()))
            if tagName == "h2":
                categoryName = elementPath.xpath('text()').get()
                print("Category: "+categoryName)
            if len(categoryName) == 0:
                continue
            if tagName == "h3":
                question = elementPath.xpath('text()').get()
                print("Question: "+question)
            '''
            for path in catPath.xpath('./following-sibling::*/'):
                response = self.transformContent(responsePath)
                columns['category'].append(categoryName)
                columns['question'].append(question)
                columns['answer'].append(response)
                columns['answer_html'].append(responsePath.get())
            '''

        today = date.today()

        columns["link"] = ["https://www.bmel.de/DE/Ministerium/_Texte/corona-virus-faq-fragen-antworten.html"] * len(columns["question"])
        columns["name"] = ["Coronavirus - Fragen und Antworten"] * len(columns["question"])
        columns["source"] = ["Bundesministerium für Ernährung und Landwirtschaft (BMEL)"] * len(columns["question"])
        columns["country"] = ["DE"] * len(columns["question"])
        columns["region"] = [""] * len(columns["question"])
        columns["city"] = [""] * len(columns["question"])
        columns["lang"] = ["de"] * len(columns["question"])
        columns["last_update"] = [today.strftime("%Y/%m/%d")] * len(columns["question"])

        return columns


if __name__ == "__main__":
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    process.crawl(CovidScraper)
    process.start()
