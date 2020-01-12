from Main.items import MainItem
import scrapy
from selenium import webdriver


class PullUpSpider(scrapy.Spider):
    name = "pull-up-image-spider"
    # First page does not follow start=page_number*100 rule
    start_urls = [
        "https://www.123rf.com/stock-photo/pull_up_workout.html?oriSearch=pull+up+workout|"]

    def parse(self, response):
        # Getting source from all image tags
        for image in response.css("img"):
            img_src = image.xpath("@src")
            if img_src:
                imageURL = img_src.extract_first()
                yield MainItem(file_urls=[imageURL])

        next_button = response.xpath("//*[@id='btn_main_nextpg']")
        yield scrapy.Request(next_button.xpath("@href").extract_first(), self.parse)
