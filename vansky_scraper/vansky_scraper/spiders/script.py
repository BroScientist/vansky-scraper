# -*- coding: utf-8 -*-
import scrapy
from vansky_scraper.spiders import params


class ScriptSpider(scrapy.Spider):
    name = 'script'
    allowed_domains = ['vansky.com']
    start_urls = ['https://www.vansky.com/info/index.html?page=1&location=&year=&title=mac']
    # start_urls = ['https://www.vansky.com/info/SMYX.html']
    results = []

    def send_mail(self, subject, msg):
        try:
            import smtplib
            server = smtplib.SMTP('smtp.gmail.com', 587)
            self.logger.info('connection success')
            server.ehlo()
            server.starttls()
            server.login(params.USERNAME, params.PASSWORD)
            self.logger.info('login success')
            message = f'Subject: {subject}\n\n{msg}'
            message = 'Subject: ' + subject + '\n\n' + msg
            server.sendmail('victorsun1685@gmail.com', 'victorsun1685@gmail.com', message.encode('utf-8'))
            server.quit()
            self.logger.info('Email successfully sent')
        except:
            self.logger.info('Email failed to send')

    def check_posting(self, title, post_time):
        if '回收' in title:
            return False
        if '分钟' in post_time:
            words = ['amacon', 'macneill', 'maclaren', 'mackenzie']
            title = ''.join(char.lower() for char in title if char.isascii)
            for word in words:
                if word.lower() in title:
                    return False
            return True

    def parse(self, response):
        ads = response.xpath('//*[@itemprop="itemListElement"]')

        for ad in ads[1:10]:
            try:
                # watch out for the first ad, which is not what we want & fucked up
                # we are only checking the first 10 ads here because there is no way in hell they post more than 10 macs in one hour
                title = ad.xpath('.//a[@class="adsTitleFont"]/text()').extract_first().strip()
                url = ad.xpath('.//a[@class="adsTitleFont"]/@href').extract_first()
                full_url = 'www.vansky.com/info/' + url
                post_time = ad.xpath('.//div[@class="adsContentFont"]/text()').extract_first().strip()

                if self.check_posting(title, post_time):
                    self.results.append({'title': title,
                                         'href': full_url})

                    yield {
                        'title': title,
                        'full_url': full_url,
                        'post_time': post_time
                    }
            except:
                pass

        self.logger.info('results bruh')
        self.logger.info(len(self.results))
        self.logger.info(self.results)

        if len(self.results) > 0:
            message = ''
            for result in self.results:
                message += result['title'] + '\n'
                message += result['href'] + '\n\n'
            subject = f'You have {len(self.results)} new search result'
            if len(self.results) > 1:
                subject += 's'
            self.send_mail(subject, message)




