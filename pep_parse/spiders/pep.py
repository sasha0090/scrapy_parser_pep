import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = "pep"
    allowed_domains = ["peps.python.org"]
    start_urls = ["https://peps.python.org/"]

    def parse(self, response):
        pep_urls = response.css(
            'section#numerical-index tr > td:nth-child(3) a'
        )
        yield from response.follow_all(pep_urls, callback=self.parse_pep)

    def parse_pep(self, response):
        number, name = (
            response.css("h1.page-title::text").get().strip().split(" – ")
        )
        status = response.css('dt:contains("Status") + dd > abbr::text').get()

        pep_info = {
            "number": number.split(" ")[-1],
            "name": name,
            "status": status,
        }

        yield PepParseItem(pep_info)
