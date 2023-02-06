import scrapy


class ThinkersSpider(scrapy.Spider):
    name = "thinkers"

    def start_requests(self):
        urls = [
            'https://en.wikipedia.org/wiki/List_of_philosophers_(A%E2%80%93C)',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'

        thinkers = []
        for li_tag in response.css('li'):
            if li_tag.css("a"):
                try:
                    if li_tag.css("a").attrib["title"] == li_tag.css("a::text").extract_first():
                        print(li_tag.css("a").attrib["title"] + " -- " + li_tag.css("a::text").extract_first())
                        thinkers.append(" \n".join(li_tag.css("a").extract()))
                except KeyError:
                    pass

        with open(filename, 'wb') as f:
            # write the list of thinkers to the file
            for t in thinkers:
                f.write(t.encode())
        self.log(f'Saved file {filename}')