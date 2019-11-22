# -*- coding: utf-8 -*-
import scrapy


class Imdb250Spider(scrapy.Spider):
    name = 'imdb250'
    allowed_domains = ['www.imdb.com']
    start_urls = ['https://www.imdb.com/chart/top/?ref_=nv_mv_250']

    def parse(self, response):
        #yillar=response.css('.secondaryInfo::text').getall()
        #puanlar=response.css('strong::text').getall()
        # for yil, ad, puan in zip(yillar, adlar, puanlar):
        #     yield {'adi': ad, 'yil':yil, 'puan': puan}
        urls = response.css('.titleColumn a::attr(href)').getall()
        for url in urls:
            yield response.follow(url, callback=self.parsemovie)

    def parsemovie(self, response):
        genre = response.css('#titleStoryLine :nth-child(10) a::text').get()
        time = response.css('#titleDetails time::text').get()
        #budget = response.css('#titleDetails :nth-child(12)::text').get()
        storyline = response.css('.summary_text::text').get()
        title = response.css('h1::text').get()
        yield {
            'title': title,
            'genre': genre,
            'duration': time,
            #'budget': budget,
            'storyline': storyline
        }

