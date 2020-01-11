from Main.items import MainItem
import scrapy
from selenium import webdriver


# For this page, we get other pages by put start=page_number*100. (start=100, start=200, etc)
def generate_other_starts(page_count):
    return ["https://www.123rf.com/stock-photo/pull_up_workout.html?oriSearch=pull%20up&start={}++&sti=muxocqqycvj9o9fzvv|".format(i*100) for i in range(1, page_count)]


class PullUpSpider(scrapy.Spider):
    name = "pull-up-image-spider"
    # First page does not follow start=page_number*100 rule
    start_urls = [
        "https://www.123rf.com/stock-photo/pull_up_workout.html?oriSearch=pull%20up&sti=muxocqqycvj9o9fzvv|", *generate_other_starts(42)]

    def parse(self, response):
        # Getting source from all image tags
        for image in response.css("img"):
            img_src = image.xpath("@src")
            if img_src:
                imageURL = img_src.extract_first()
                yield MainItem(file_urls=[imageURL])
