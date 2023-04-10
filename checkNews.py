import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
from urllib.parse import urlparse
import html
import press_dict
import hashlib
import json
from PIL import Image

def get_real_url_from_shortlink(url): #단축링크 원본링크로 변경
    resp = requests.get(url,headers={'User-Agent':'Mozilla/5.0'})
    print('Original URL:'+resp.url)
    return resp.url

def getTitle(source,domain):
    pressKeys = press_dict.pressData.keys()

    if domain in pressKeys:
        domain_dict = press_dict.pressData.get(domain)
        if 'titleSelector' in domain_dict:
            try:
                title = source.select_one(domain_dict['titleSelector']).text
                if domain_dict['titleCorrectionNeeded'] == True:
                    title = source.select_one(domain_dict['titleSelector'])
                    title = eval(f"source.find({domain_dict['titleCorrectionFind']})")
                    title = str(title)
                    title = title.replace('\t','')
                    title = title.replace('\n','')
                    to_clean = re.compile('<.*?>') # <> 사이에 있는 것들
                    title = re.sub(to_clean,'',title) #html태그 모두 지우기
                else:
                    pass
            except:
                title = ''
        else:
            try:
                title = source.find('meta',property='og:title')['content']
    
                if 'titleTrim' in domain_dict:
                    title = title[domain_dict['titleTrim']:]
                if 'titleTrimEnd' in domain_dict:
                    title = title[:-domain_dict['titleTrimEnd']]
            except:
                title = ''
                print('title meta값을 찾을 수 없습니다')
    else:
        try:
            title = source.find('meta',property='og:title')['content']
        except:
            title = ''
            print('title meta값을 찾을 수 없습니다')

    return title

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
            
            try:
                if domain in press_dict.pressData.keys():
                    domain_dict = press_dict.pressData.get(domain)

                    rawDatetime = source.select_one(domain_dict['datetimeSelector']).text
                    if 'datetimeTrim' in domain_dict:
                        rawDatetime = rawDatetime[domain_dict['datetimeTrim']:]
                    if 'datetimeTrimEnd' in domain_dict:
                        rawDatetime = rawDatetime[:-domain_dict['datetimeTrimEnd']]
                    if 'datetimeRange' in domain_dict:
                        rawDatetime = rawDatetime[domain_dict['datetimeRange'][0]:domain_dict['datetimeRange'][1]]
                    datetime_obj = datetime.strptime(rawDatetime,domain_dict['datetimeFormat'])
                    publishedDate = datetime_obj.strftime('%Y.%m.%d.')
                    publishedTime = datetime_obj.strftime('%H:%M')
                else:
                    publishedDate = ''
                    publishedTime = ''
            except Exception as e:
                publishedDate = ''
                publishedTime = ''
                print('published_time meta값을 찾을 수 없습니다')
                print(e)
        
        return publishedDate,publishedTime

def getContent(source,domain):

    pressKeys = press_dict.pressData.keys()
    if domain in pressKeys:
        domain_dict = press_dict.pressData.get(domain)
        if 'contentSelector' in domain_dict:
            content = source.select_one(domain_dict['contentSelector']).text

            if domain_dict['contentCorrectionNeeded'] == True:
                content = source.select_one(domain_dict['contentSelector'])
                content = eval(f"source.find({domain_dict['contentCorrectionFind']})")
                content = str(content)
                content = content.replace('<br/>','\r\n')
                to_clean = re.compile('<.*?>') # <> 사이에 있는 것들
                content = re.sub(to_clean,'',content) #html태그 모두 지우기
            else:
                pass
            print(content)
        else:
            content = ''
    else:
        content = ''

    return content

def checkNews(url) -> tuple : #언론사별 selector

    domain = urlparse(url).netloc #도메인 이름 가져옴 ex) https://www.example.com/ex/123 -> www.example.com

    print(domain)

    url = get_real_url_from_shortlink(url)
    web = requests.get(url,headers={'User-Agent':'Mozilla/5.0'})
    if web.encoding != 'UTF-8' or web.encoding != 'utf-8':
        web.encoding=None
    source = BeautifulSoup(web.text,'html.parser')

    if "n.news.naver" in url: #네이버뉴스
        print('n.news.naver checked')
        title = source.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_title > h2").text
        press = source.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_top > a > img.media_end_head_top_logo_img.light_type")['alt']
        content = source.select_one("#newsct_article")
        publishedInfo = source.select_one("#ct > div.media_end_head.go_trans > div.media_end_head_info.nv_notrans > div.media_end_head_info_datestamp > div > span")['data-date-time']

        # find all <img> tags
        img_tags = content.find_all('img')
        # replace each <img> tag with a new string
        for image in img_tags:
            try:
                image_url = image['data-src']

                if 'gif' in image_url[-13:]:
                    pass
                elif 'jpg' in image_url[-13:]:
                    hash_object = hashlib.sha256(image_url.encode())
                    verificationCode = hash_object.hexdigest()

                    try:
                        with open('image_dict.json', 'r') as f:
                            image_json = json.load(f)
                    except:
                        with open('image_dict.json', 'w') as f:
                            # Write an empty JSON object to the file
                            json.dump({}, f)
                        with open('image_dict.json', 'r') as f:
                            image_json = json.load(f)

                    if url in image_json:
                        image_json[url][verificationCode] = image_url
                    else:
                        image_json[url] = {verificationCode: image_url}

                    with open('image_dict.json', 'w') as f: #json에 image 관련 데이터 저장
                        json.dump(image_json, f, indent=4, sort_keys=True)

                    reponse = requests.get(image_url) #인식된 image 다운로드
                    with open(f'images/{verificationCode}.jpg','wb') as f:
                        f.write(reponse.content)

                    image.replace_with(verificationCode) #html 소스에 있는<img> 태그를 verificationCode로 일시적으로 바꿈, exportHangul 과정에서 verificationCode를 사진으로 변경함

                    try: #다운 받은 이미지의 크기를 조정함
                        with Image.open(f'images/{verificationCode}.jpg') as downloadImage:
                            # Change the size while preserving the aspect ratio
                            width, height = downloadImage.size
                            if width >= 360:
                                ratio = width / 360
                                new_size = (int(width / ratio), int(height / ratio))
                                downloadImage = downloadImage.resize(new_size, resample=Image.BICUBIC)

                                # Save the updated image with original quality
                                downloadImage.save(f'images/{verificationCode}.jpg', quality=95)
                            else:
                                print(f"Image {verificationCode} is too small to resize.")
                    except Exception as e:
                        print(e)
                        print('이미지 크기 조정 과정에서 오류가 발생했습니다.')
                else:
                    pass
            except Exception as e:
                print(e)
                print('Image data-src 를 불러오는 과정에서 오류가 발생했습니다.')

        contentStr = str(content).replace('<br/>','\r\n') #<br>태그 Enter키로 변경
        contentStr = str(contentStr).replace('</table>','\r\n\r\n') #이미지 부연설명 내용과 분리
        contentStr = contentStr.replace('</img>','') #이미지 위치 확인
        contentStr = contentStr.replace('<em class="img_desc">','\r\n\r\n')
        contentStr = contentStr.replace('</em>','\r\n')
        contentStr = contentStr.replace('</strong>','\r\n\r\n')
        contentStr = contentStr.replace('<div','\r\n\r\n<div')
        contentStr = contentStr.replace('</span>','\r\n')
        contentStr = contentStr.replace('			','') #방송기사 본문에서 [앵커] 앞에 알 수 없는 공백이 있어 이를 제거함
        print(contentStr)
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
        contentStr = str(contentStr).replace('</table>','\r\n\r\n') #이미지 부연설명 내용과 분리
        contentStr = contentStr.replace('</img>','\r\n') #이미지 위치 확인
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
        contentStr = str(contentStr).replace('</table>','\r\n\r\n') #이미지 부연설명 내용과 분리
        contentStr = contentStr.replace('</img>','\r\n') #이미지 위치 확인
        to_clean = re.compile('<.*?>') # <> 사이에 있는 것들
        contentEdited = re.sub(to_clean,'',contentStr) #html태그 모두 지우기        
        
    else:
        print("호환되지 않는 링크로 meta값을 탐색합니다.")
        #제목 찾기
        title = getTitle(source,domain)

        #언론사 찾기
        press = getPress(source,domain)

        #본문 찾기
        contentEdited = getContent(source,domain)

        #발행일자 찾기
        publishedDate,publishedTime = getPublishedDatetime(source,domain)

    contentEdited = html.unescape(contentEdited) #&lt;(<) &gt;(>) 정상적으로 다시 변환시킴

    return title,press,contentEdited,publishedDate,publishedTime

if __name__ == "__main__":
    title,press,contentEdited,publishedDate,publishedTime = checkNews('https://n.news.naver.com/mnews/article/023/0003755458?sid=102')
    print(contentEdited)