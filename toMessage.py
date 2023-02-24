import time

today = time.strftime('%Y.%m.%d.') 
hours = int(time.strftime('%H'))

if hours <= 12:
   reportHour = "09"
else :
   reportHour = '17' 

def messageHeader():
    messageHeader = f'금일({today}) {reportHour}시까지 한강 관련 주요 보도사항입니다.\n'
    return messageHeader

def messageFooter():
    messageFooter = '-문화홍보과-'
    return messageFooter

def toMessage(paperNewsList,internetNewsList):
    messageCount = 1
    finalNews = []
    noNews = []

    if len(paperNewsList) < 1 and len(internetNewsList) < 1:
        reportNone = f'금일({today}) {reportHour}시까지 한강 관련 주요 보도사항 없습니다.\n\n-문화홍보과-'
        noNews.append(reportNone)
        return noNews

    else:
        finalNews.append(messageHeader())

    if len(paperNewsList) > 0:
        finalNews.append("[신문/방송]")
        for i in range(len(paperNewsList)):
            title = paperNewsList[i]["title"]
            press = paperNewsList[i]["press"]
            summary = paperNewsList[i]["summary"]
            shortenUrl = paperNewsList[i]["shortenUrl"]
            news = f'{messageCount}. {title}({press}_{summary})\n{shortenUrl}\n'
            finalNews.append(news)
            messageCount = messageCount+1
    
    if len(internetNewsList) > 0:
        finalNews.append("[인터넷]")
        for i in range(len(internetNewsList)):
            title = internetNewsList[i]["title"]
            press = internetNewsList[i]["press"]
            summary = internetNewsList[i]["summary"]
            shortenUrl = internetNewsList[i]["shortenUrl"]
            news = f'{messageCount}. {title}({press}_{summary})\n{shortenUrl}\n'
            finalNews.append(news)
            messageCount = messageCount+1
    
    finalNews.append(messageFooter())

    return finalNews