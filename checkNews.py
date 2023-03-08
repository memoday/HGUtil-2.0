import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from urllib.parse import urlparse
import html

def get_real_url_from_shortlink(url): #단축링크 원본링크로 변경
    resp = requests.get(url,headers={'User-Agent':'Mozilla/5.0'})
    print('Original URL:'+resp.url)
    return resp.url

def getPress(source,domain):
        pressSetting = { #press meta값이 없을 때 수동으로 언론사 이름을 제공해줌
            'www.sisa-news.com' : '시사뉴스',
            'www.ilyosisa.co.kr' : '일요시사',
            'www.skyedaily.com' : '스카이데일리',
            'idsn.co.kr' : '매일안전신문',
            'www.siminilbo.co.kr' : '시민일보',
            'www.wsobi.com' : '여성소비자신문',
            'realty.chosun.com' : '땅집고',
            'www.the-pr.co.kr' : 'The PR Time',
            'www.vegannews.co.kr' : '비건뉴스',
            'www.wikitree.co.kr' : '위키트리',
            'www.viva100.com' :'브릿지경제',
            'www.discoverynews.kr' : '디스커버리뉴스',
            'www.joongboo.com' : '중부일보',
            'www.nspna.com' : 'NSP통신',
            'www.asiatoday.co.kr' : '아시아투데이',
            'www.kihoilbo.co.kr' : '기호일보',
            'www.thedailypost.kr' : '데일리포스트',
            'www.donga.com' : '동아일보',
            'skbroadband.com' : 'SK브로드밴드',
            'www.obs.co.kr' : 'OBS',
            'www.harpersbazaar.co.kr' : '하퍼스바자',
            'mbnmoney.mbn.co.kr' : '매일경제TV',
            'www.jeonmae.co.kr' : '전국매일신문',
            'www.queen.co.kr' : 'Queen',
            'www.foodneconomy.com' : '푸드경제신문',
            'www.ktv.go.kr' : 'KTV국민방송',
        } 

        if domain in pressSetting:
            print('도메인 주소: '+domain)
            press = pressSetting[domain]
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
            try:
                if 'www.newspim.com' in domain:
                    rawDatetime = source.select_one('#send-time').text
                    print(rawDatetime)
                    datetime_obj = datetime.strptime(rawDatetime, '%Y년%m월%d일 %H:%M')
                    publishedDate = datetime_obj.strftime('%Y.%m.%d.')
                    publishedTime = datetime_obj.strftime('%H:%M')

                else:
                    publishedDate = ''
                    publishedTime = ''
                    print('published_time meta값을 찾을 수 없습니다')
            except:
                publishedDate = ''
                publishedTime = ''
        
        return publishedDate,publishedTime

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
        content = source.select_one("#dic_area")
        publishedInfo = source.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div > span")['data-date-time']
        contentStr = str(content).replace('<br/>','\r\n') #<br>태그 Enter키로 변경
        contentStr = str(contentStr).replace('</table>','\r\n') #이미지 부연설명 내용과 분리
        contentStr = contentStr.replace('</img>','') #이미지 위치 확인
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

        try:
            content.find(class_ = 'source').decompose()
            content.find(class_ = 'byline').decompose()
            content.find(class_ = 'reporter_area').decompose()
            content.find(class_ = 'copyright').decompose()
            content.find(class_ = 'categorize').decompose()
            content.find(class_ = 'promotion').decompose()
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
        contentEdited = '' #내용은 기사마다 너무 달라 불러오지 않기로 함
        #발행일자 찾기
        publishedDate,publishedTime = getPublishedDatetime(source,domain)

    contentEdited = html.unescape(contentEdited) #&lt;(<) &gt;(>) 정상적으로 다시 변환시킴

    return title,press,contentEdited,publishedDate,publishedTime