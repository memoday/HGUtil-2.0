import checkNews as cn
import hwpMacro
import naverShorten

TurlList = ['https://entertain.naver.com/read?oid=109&aid=0004443514','https://n.news.naver.com/mnews/article/241/0003149995?sid=103']
TurlList2 = ['https://n.news.naver.com/mnews/article/018/0005417218?sid=100','https://n.news.naver.com/mnews/article/366/0000874286?sid=102','https://n.news.naver.com/mnews/article/050/0000062990?sid=101']
newsList = []

def crawl(urlList):

    for i in range(len(urlList)):
        title, press, content, publishedDate, publishedTime = cn.checkNews(urlList[i])
        shortenUrl = naverShorten.naverShorten(urlList[i])

        news = {
            'title' : title,
            'press' : press,
            'publishedDate' : publishedDate,
            'publishedTime' : publishedTime,
            'shortenUrl' : shortenUrl,
            'content': content,
            'summary' : 'summary',
            }
        newsList.append(news)

    return newsList
    # hwpMacro.main(paperNewsList,internetNewsList)
    