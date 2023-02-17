import os
import sys
import urllib.request
import json


client_id = "9Ro4_Qfw2DyTiCMaMQbt" # 개발자센터에서 발급받은 Client ID 값
client_secret = "lTxJi70grI" # 개발자센터에서 발급받은 Client Secret 값

def naverShorten(longUrl): 

    encText = urllib.parse.quote(longUrl)
    data = "url=" + encText
    url = "https://openapi.naver.com/v1/util/shorturl"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
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