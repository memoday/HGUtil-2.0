import os
import sys
import urllib.request
import json
import requests
import secret


def get_real_url_from_shortlink(url): #단축링크 원본링크로 변경
    resp = requests.get(url,headers={'User-Agent':'Mozilla/5.0'})
    print('Original URL:'+resp.url)
    return resp.url

def naverShorten(longUrl): 

    longUrl = get_real_url_from_shortlink(longUrl)

    encText = urllib.parse.quote(longUrl)
    data = "url=" + encText
    url = "https://openapi.naver.com/v1/util/shorturl"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",secret.getId())
    request.add_header("X-Naver-Client-Secret",secret.getSecret())
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
        response_body = response.read()
        response_body.decode('utf-8')
        result = json.loads(response_body)
        shortenUrl = result["result"]["url"]
        print(shortenUrl)
        return shortenUrl
    else:
        print("Error Code:" + rescode)

if __name__ == "__main__":
    print(naverShorten('https://odium.kr'))