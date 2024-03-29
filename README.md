# HGUtil-2.0 업무자동화 (기사 크롤링, 한컴 매크로)

<br>
<br>

> [다운로드 바로가기](https://github.com/memoday/HGUtil-2.0/releases)

<br>
<br>

<h1> 1. 사용 안내</h1>

- 다운로드 중 'HGUtil.exe은(는) 위험할 수 있으므로 다운로드하지 않습니다.' 표시될 시 '더보기 -> 계속'
- Windows의 PC 보호 창이 뜨면 '추가 정보 -> 실행'
- 일부 백신 프로그램(V3, 알약 등)에서 실행을 차단 할 수 있습니다. (백신 사용중지 혹은 진단 예외 등록 바람)
<br>

<h1> 2. 대표 기능 소개</h1>

<h2> 2-1. 기사 등록 및 테이블 </h2>

```def addNews(self)```

인터넷 기사 주소를 입력하면 크롤링한 데이터를 테이블에 입력합니다.
<br>
> **업태**와 **주요내용**(요약)은 크롤링 대상이 아닙니다. 직접 수정하셔야 합니다.
<br>

**주소**는 네이버 API를 활용해 me2.do 단축링크를 제공합니다. 자세한 내용은 아래 3번을 참고해주세요.
<br>

테이블 상단 클릭을 통해 정렬 기능을 사용할 수 있습니다.
<br>
등록된 기사를 삭제 해야하는 경우, 삭제할 행의 셀을 한 번 클릭하여 **삭제**버튼을 통해 삭제를 할 수 있습니다.
<br>

버전 v1.0.0 기준, 아래 도메인과 완벽 호환합니다.

- 네이버 뉴스 (n.news.naver.com)
- 네이버 스포츠뉴스 (sports.news.naver.com)
- 네이버 연예뉴스 (entertain.naver.com)

네이버 외 주소는 meta데이터를 크롤링합니다. meta가 존재하지 않는 경우 공백으로 채워지게 됩니다.


발행일자 meta 데이터가 존재하지 않는 경우 **<YYYY-MM-DD"T"HH:MM>** 양식으로 모두 채워주셔야합니다. ex) 2023-03-16T17:23

<br>

![HGUtil_기사등록](https://user-images.githubusercontent.com/74040890/220837501-e6e20a6a-8a27-43dc-9d1d-a85a5140427c.gif)


<h2> 2-2. 한글로 내보내기 </h2>

```hwpMacro.py```

테이블에 입력된 기사를 지정된 양식의 한글 파일로 내보냅니다.
<br>
테이블을 한글로 그대로 옮기는 것이기에  **주요내용**을 비롯한 모든 공백 칸을 채워주시길 바랍니다.
<br>



<br>

![HGUtil_한글](https://user-images.githubusercontent.com/74040890/220838770-96f79a83-343e-4311-bb47-3a75d3175f4e.gif)


<h2> 2-3. 메시지로 내보내기 </h2>

```toMessage.py```

테이블에서 선택한 기사를 지정된 메시지 양식으로 출력합니다.
<br>
출력되는 기사의 순서는 변경이 가능하며, 출력된 메시지를 임의로 수정할 수도 있습니다.
<br>
선택된 기사가 없다면 미리 설정해둔 메시지가 출력하게 됩니다.

<br>

![HGUtil_메시지](https://user-images.githubusercontent.com/74040890/220840102-7cf2134a-c964-43a0-8f71-625b6a7f9420.gif)


<h2> 2-4. 작업 내용 저장/불러오기 </h2>

작업한 테이블 정보를 table.ini 파일로 저장할 수 있습니다. ini파일은 프로그램 경로에 생성됩니다.
<br>
**불러오기**로 경로에 있는 table.ini에서 데이터를 불러와  테이블을 복구합니다.
<br>

테이블 정렬은 다시 설정해야합니다.
<br>

<h1>3. 네이버 API </h1>

```naverShorten.py```
<br><br>
아래는 네이버 API키가 들어가는 코드입니다. ```secret.py``` 따로 생성해서 적용해주세요.

```
def getId():
    client_id = YOUR_CLIENT_ID
    return client_id

def getSecret():
    client_secret = YOUR_CLIENT_SECRET
    return client_secret
```

네이버 개발자 센터에서 개인 API Key를 발급받을 수 있습니다.
<br>
발급받은 API Key는 하루 최대 25,000개의 단축링크를 생성할 수 있습니다.
<br>

<h1>4. 오류 해결법 </h1>
<h2> 4-1. 한글 내보내기 실패 win32.com.gen_py has no attribute 'CLSIDToClassMap' </h2>

- hwpMacro.py에 있는 win32.com.client 라이브러리의 오류입니다.
- User > Appdata > Local > Temp 경로에 gen_py라는 폴더를 삭제해주면 됩니다.

<br>

![image](https://user-images.githubusercontent.com/74040890/225817878-f21786ae-6636-4619-ab98-abfc407c8aed.png)

<h1>5. 기타 </h1>
<h2> 5-1. 보안 팝업 (보안 승인 모듈 추가하기) </h2>

- 파일 수정, 그림 삽입 등 과정에서 팝업 뜨는걸 방지해주는 모듈입니다.
- 보안 승인 모듈은 한컴디벨로퍼에서 다운이 가능합니다.
- 상세 적용방법은 아래 링크에서 확인해주시길 바랍니다.

https://developer.hancom.com/hwpctrl-hwpautomation/

<br>

![보안모듈](https://user-images.githubusercontent.com/74040890/231094919-245a85b2-1f2b-4990-92fd-1cc34fa0a7c5.png)

<br>

![image](https://user-images.githubusercontent.com/74040890/232679312-fa32efe2-d346-4100-b14f-31891bb2710e.png)

<br>
C드라이브에 보안모듈 이름을 "FilePathCheckerModule.dll"로 저장해둔 상태로 레지스트리를 위와 같이 추가했습니다.

