from vansky_scraper.spiders import params

results = []
results.append({'title': 'mac for sale',
                'href': 'www.gofuckyouself.glob'})
results.append({'title': 'mac pro cheap af',
                'href': 'www.gofuckyouself.org'})
results.append({'title': '出惠普 M28w镭射打印机',
                'href': 'www.vansky.com/info/adfree/1664364.html'})

def send_mail(subject, msg):

    import smtplib
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login(params.USERNAME, params.PASSWORD)
    message = f'Subject: {subject}\n\n{msg}'
    server.sendmail('victorsun1685@gmail.com', 'victorsun1685@gmail.com', message.encode('utf-8'))
    server.quit()
    print('Email successfully sent')

#
# if len(results) > 0:
#     message = ''
#     for result in results:
#         message += str(result['title']) + '\n'
#         message += result['href'] + '\n'
#     subject = f'You have {len(results)} new search result'
#     if len(results) > 1:
#         subject += 's'
#     send_mail(subject, message)

def check_posting(title):
    if '回收' in title:
        return False
    words = ['amacon', 'macneill', 'maclaren', 'mackenzie']
    title = ''.join(char.lower() for char in title if char.isascii)
    for word in words:
        if word.lower() in title:
            return False
    return True

check_posting('出售-列治文TEMPO by Amacon一年新两房两卫高层公寓')
check_posting('24小时可上门，高价回收苹果电脑Macbook Pro，Air，iPhone，iMac，iPad，好坏都收')
check_posting('出租2间雅房! Richmond列治文高尚社区 MacNeill中学步行5分钟 独立卫浴 也可1厅1卧')
check_posting('2016年MacBook Air 13” i5-1.6ghz 8g 256ssd $650 一口价')