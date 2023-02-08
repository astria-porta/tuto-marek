import scrapy


class ThinkersSpider(scrapy.Spider):
    name = "thinkers"

    def start_requests(self):
        urls = [
            'https://en.wikipedia.org/wiki/List_of_philosophers_(A%E2%80%93C)',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def cleanUP(self, response):
        elements = response.xpath("//*")
        new_response = response
        extract_file = "extracted.txt"
        keeping_file = "keeping.txt"

        extracted_list = []
        keeping_list = []

        for element in elements:
            if(len(element.xpath("//*")) > 2):
                for e in element.xpath("//*"):
                    if e.xpath("@id").extract_first() not in ["A"]:
                        # new_response = new_response.replace(body=element.get().encode('utf-8'))
                        extracted_list.append(" \n".join(element.css("*").extract()))
                    else:
                        print("SPAN ID A DETECTED")
                        keeping_list.append(" \n".join(element.css("*").extract()))

                        with open(extract_file, 'wb') as f:
                            # write the list of thinkers to the file
                            for t in extracted_list:
                                f.write(t.encode())
                        self.log(f'Saved file {extract_file}')

                        with open(keeping_file, 'wb') as f:
                            # write the list of thinkers to the file
                            for t in keeping_list:
                                f.write(t.encode())
                        self.log(f'Saved file {keeping_file}')
                        return new_response

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'

        thinkers = []
        # response = self.cleanUP(response)
        # for element in response.xpath("//*"):
        #     thinkers.append(" \n".join(element.css("*").extract()))

        # for li_tag in response.css('li'):
        #     print(li_tag)
        #     if li_tag.css("a"):
        #         try:
        #             if li_tag.css("a").attrib["title"] == li_tag.css("a::text").extract_first():
        #                 print(li_tag.css("a").attrib["title"] + " -- " + li_tag.css("a::text").extract_first())
        #                 thinkers.append(" \n".join(li_tag.css("a").extract()))
        #         except KeyError:
        #             pass

        with open(filename, 'wb') as f:
            # write the list of thinkers to the file
            for t in thinkers:
                f.write(t.encode())
        self.log(f'Saved file {filename}')