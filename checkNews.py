import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from urllib.parse import urlparse
import html
import press_dict

def get_real_url_from_shortlink(url): #단축링크 원본링크로 변경
    resp = requests.get(url,headers={'User-Agent':'Mozilla/5.0'})
    print('Original URL:'+resp.url)
    return resp.url

def getPress(source,domain):
        
        pressKeys = press_dict.pressData.keys()

        if domain in pressKeys:
            domain_dict = press_dict.pressData.get(domain)
            print('도메인 주소: '+domain)
            press = domain_dict['name']
        else:
            try:
                press = source.find('meta',property='og:site_name')['content']
            except:
                press = ''
                print('site_name meta값을 찾을 수 없습니다.')
        return press

def getPublishedDatetime(source,domain) -> tuple:
        try:
            metaDate = source.find('meta',property='article:published_time')['content']
            rawDate = metaDate[0:10]
            rawDate = datetime.strptime(rawDate,'%Y-%m-%d')
            finalDate = str(datetime.strftime(rawDate,'%Y.%m.%d.'))

            finalTime = metaDate[11:16]

            publishedDate = finalDate
            publishedTime = finalTime

        except:

            datetime_formats = {
                'www.newspim.com': {
                    'datetimeSelector': '#send-time',
                    'format': '%Y년%m월%d일 %H:%M'
                },
                'ch1.skbroadband.com': {
                    'datetimeSelector': 'body > div.wrapper > div.container > div.contentBox > div > div.wrap_content_view > div.content_metadata > dl > dd > div > span',
                    'format': '%Y-%m-%d %H:%M:%S'
                },
                'www.sisa-news.com': {
                    'datetimeSelector': '#container > div.column.col73.mb00 > div:nth-child(1) > div > div.arv_005_01 > div.fix_art_top > div > div > ul.art_info > li:nth-child(2)',
                    'datetimeFormat': '%Y.%m.%d %H:%M:%S',
                    'datetimeTrim': 3
                }
            }

            try:
                if domain in datetime_formats.keys():
                    domain_dict = datetime_formats.get(domain)

                    rawDatetime = source.select_one(domain_dict['datetimeSelector']).text
                    if 'datetimeTrim' in domain_dict:
                        rawDatetime = rawDatetime[domain_dict['datetimeTrim']:]
                    datetime_obj = datetime.strptime(rawDatetime,domain_dict['datetimeFormat'])
                    publishedDate = datetime_obj.strftime('%Y.%m.%d.')
                    publishedTime = datetime_obj.strftime('%H:%M')
            except:
                publishedDate = ''
                publishedTime = ''
                print('published_time meta값을 찾을 수 없습니다')
        
        return publishedDate,publishedTime

def getContent(source,domain):

    if 'ch1.skbroadband.com' in domain:
        content = source.find('meta',property='og:description')['content']
    else:
        content = ''

    return content

def checkNews(url) -> tuple : #언론사별 selector

    domain = urlparse(url).netloc #도메인 이름 가져옴 ex) https://www.example.com/ex/123 -> www.example.com

    url = get_real_url_from_shortlink(url)
    web = requests.get(url,headers={'User-Agent':'Mozilla/5.0'})
    if web.encoding != 'UTF-8':
        web.encoding=None
    source = BeautifulSoup(web.text,'html.parser')

    if "n.news.naver" in url: #네이버뉴스
        print('n.news.naver checked')
        title = source.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_title > h2").text
        press = source.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_top > a > img.media_end_head_top_logo_img.light_type")['alt']
        content = source.select_one("#newsct_article")
        publishedInfo = source.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div > span")['data-date-time']
        contentStr = str(content).replace('<br/>','\r\n') #<br>태그 Enter키로 변경
        contentStr = str(contentStr).replace('</table>','\r\n\r\n') #이미지 부연설명 내용과 분리
        contentStr = contentStr.replace('</img>','') #이미지 위치 확인
        contentStr = contentStr.replace('<em class="img_desc">','\r\n\r\n')
        contentStr = contentStr.replace('</em>','\r\n')
        contentStr = contentStr.replace('</strong>','\r\n\r\n')
        contentStr = contentStr.replace('			','') #방송기사 본문에서 [앵커] 앞에 알 수 없는 공백이 있어 이를 제거함
        to_clean = re.compile('<.*?>') # <> 사이에 있는 것들
        contentEdited = re.sub(to_clean,'',contentStr) #html태그 모두 지우기

        rawDate = publishedInfo[0:10]
        rawDate = datetime.strptime(rawDate,'%Y-%m-%d')
        finalDate = str(datetime.strftime(rawDate,'%Y.%m.%d.'))

        time = publishedInfo[11:16]
        # finalTime = datetime.strptime(time,'%H:%M')
        finalTime = time

        publishedDate = finalDate
        publishedTime = finalTime

    elif "sports.news.naver" in url: #네이버 스포츠뉴스
        print('sports.news.naver checked')
        title = source.select_one("#content > div > div.content > div > div.news_headline > h4").text
        press = source.select_one("#pressLogo > a > img")['alt']
        content = source.select_one("#newsEndContents")

        classes_to_remove = ['source', 'byline', 'reporter_area', 'copyright', 'categorize', 'promotion']

        for class_name in classes_to_remove:
            try:
                content.find(class_ = class_name).decompose()
            except:
                pass

        date = source.select_one("#content > div > div.content > div > div.news_headline > div > span:nth-child(1)").text
        date = date.replace('기사입력 ','')
        publishedDate = date[0:11]
        rawPublishedTime = date[12:20]
        rawPublishedTime = rawPublishedTime.replace('오전','AM')
        rawPublishedTime = rawPublishedTime.replace('오후','PM')
        publishedTime = datetime.strptime(rawPublishedTime, '%p %I:%M') # %I가 12시간 형식, %H가 24시간 형식
        publishedTime = datetime.strftime(publishedTime, '%H:%M')
        
        contentStr = str(content).replace('<br/>','\r\n') #<br>태그 Enter키로 변경
        contentStr = str(contentStr).replace('</table>','\r\n') #이미지 부연설명 내용과 분리
        contentStr = contentStr.replace('</img>','') #이미지 위치 확인
        to_clean = re.compile('<.*?>') # <> 사이에 있는 것들
        contentEdited = re.sub(to_clean,'',contentStr) #html태그 모두 지우기
    
    elif "entertain.naver.com" in url:
        print('entertain.naver checked')
        title = source.find('meta',property='og:title')['content']
        press = source.select_one("#content > div.end_ct > div > div.press_logo > a > img")['alt']
        content = source.select_one("#articeBody")
        date = source.select_one('#content > div.end_ct > div > div.article_info > span > em').text

        publishedDate = date[0:11]
        rawPublishedTime = date[12:]
        rawPublishedTime = rawPublishedTime.replace('오전','AM')
        rawPublishedTime = rawPublishedTime.replace('오후','PM')
        publishedTime = datetime.strptime(rawPublishedTime, '%p %I:%M') # %I가 12시간 형식, %H가 24시간 형식
        publishedTime = datetime.strftime(publishedTime, '%H:%M')

        contentStr = str(content).replace('<br/>','\r\n') #<br>태그 Enter키로 변경
        contentStr = str(contentStr).replace('</table>','\r\n') #이미지 부연설명 내용과 분리
        contentStr = contentStr.replace('</img>','') #이미지 위치 확인
        to_clean = re.compile('<.*?>') # <> 사이에 있는 것들
        contentEdited = re.sub(to_clean,'',contentStr) #html태그 모두 지우기        
        
    else:
        print("호환되지 않는 링크로 meta값을 탐색합니다.")
        #제목 찾기
        try:
            title = source.find('meta',property='og:title')['content']
        except:
            title = ''
            print('title meta값을 찾을 수 없습니다')

        #언론사 찾기
        press = getPress(source,domain)

        #본문 찾기
        contentEdited = getContent(source,domain)

        #발행일자 찾기
        publishedDate,publishedTime = getPublishedDatetime(source,domain)

    contentEdited = html.unescape(contentEdited) #&lt;(<) &gt;(>) 정상적으로 다시 변환시킴

    return title,press,contentEdited,publishedDate,publishedTime

if __name__ == "__main__":
    title,press,contentEdited,publishedDate,publishedTime = checkNews('https://n.news.naver.com/mnews/article/052/0001858853?sid=102')