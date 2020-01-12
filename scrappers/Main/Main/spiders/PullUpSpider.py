from Main.items import MainItem
from enum import Enum
import scrapy


class NextButtonXpath(Enum):
    RF = "//*[@id='btn_main_nextpg']"
    GETTY = "//*[@class='search-pagination__button search-pagination__button--next']"


class PullUpSpider(scrapy.Spider):
    name = "pull-up-image-spider"
    start_urls = ["https://www.123rf.com/stock-photo/pull_up.html",
                  "https://www.gettyimages.com/photos/chin-ups?"]

    def parse(self, response):
        # Getting source from all image tags
        for image in response.css("img"):
            img_src = image.xpath("@src")
            if img_src:
                imageURL = img_src.extract_first()
                yield MainItem(file_urls=[imageURL])

        base_url = ""
        next_xpath = ""
        if "123rf" in response.url:
            next_xpath = NextButtonXpath.RF
        elif "gettyimages" in response.url:
            base_url = "https://www.gettyimages.com"
            next_xpath = NextButtonXpath.GETTY

        # Go to next page and repeat
        next_button = response.xpath(next_xpath)
        print(next_button.xpath("@href").extract_first())
        yield scrapy.Request(base_url + next_button.xpath("@href").extract_first(), self.parse)
