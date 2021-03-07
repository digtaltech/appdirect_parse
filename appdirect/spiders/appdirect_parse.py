from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
import codecs
from time import sleep
from selenium import webdriver
from appdirect.items import Urls
import csv


class someSpider(CrawlSpider):
    name = 'app'
    allowed_domains = ['help.appdirect.com']
    start_urls = ['https://help.appdirect.com/']
    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = Urls()
        
        if re.search(r'\Default\b', response.url):
            driver = webdriver.Chrome("C:\chromedriver\chromedriver.exe")
            driver.get(response.url)
            sleep(2)
            button = driver.find_element_by_xpath(
                '//button[@class="button needs-pie next-topic-button"]')

            status = True
            url_parse = "0"

            while status:
                try:
                    filename = driver.current_url.split("/")[-1] + '.html'
                    with open(r'dump_dynamic.csv', 'a', newline='') as csvfile:
                        fieldnames = ['url', 'title', 'path']
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writerow(
                            {'url': driver.current_url, 'title': "Dynamic", 'path': f'html2/{filename}'})

                    file_object = codecs.open(
                        f'dynamic_page/{filename}', "w", "utf-8")
                    html = driver.page_source
                    file_object.write(f'<base href="{driver.current_url}">')
                    file_object.write(html)

                    button.click()
                    sleep(2)
                    if (url_parse == driver.current_url):
                        status = False
                        driver.close()
                except:
                    driver.close()
        else:
            filename = response.url.split("/")[-1] + '.html'
            item['url'] = response.url
            item['title'] = response.xpath('//title/text()').get()
            item['path'] = f"static_page/{filename}"
            with open(f'static_page/{filename}', 'wb') as f:
                f.write(f'<base href="{response.url}">'.encode())
                f.write(response.body)
            return item
