import checkNews as cn
import hwpMacro

urlList = ['https://entertain.naver.com/read?oid=109&aid=0004443514','https://n.news.naver.com/mnews/article/241/0003149995?sid=103']
urlList2 = ['https://n.news.naver.com/mnews/article/018/0005417218?sid=100','https://n.news.naver.com/mnews/article/366/0000874286?sid=102','https://n.news.naver.com/mnews/article/050/0000062990?sid=101']
paperNewsList = []
internetNewsList = []

for i in range(len(urlList)):
    title, press, content, publishedDate, publishedTime = cn.checkNews(urlList[i])

    paperNews = {
        'title' : title,
        'press' : press,
        'publishedDate' : publishedDate,
        'publishedTime' : publishedTime,
        'shortenUrl' : 'shortenUrl',
        'content': content,
        'summary' : 'summary',
        }
    paperNewsList.append(paperNews)

for i in range(len(urlList2)):
    title, press, content, publishedDate, publishedTime = cn.checkNews(urlList2[i])

    internetNews = {
        'title' : title,
        'press' : press,
        'publishedDate' : publishedDate,
        'publishedTime' : publishedTime,
        'shortenUrl' : 'shortenUrl',
        'content': content,
        'summary' : 'summary',
        }
    internetNewsList.append(internetNews)

hwpMacro.main(paperNewsList,internetNewsList)
    