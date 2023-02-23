# HGUtil-2.0 업무자동화

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

인터넷 기사 주소를 입력하면 크롤링을 해 테이블에 맞게 데이터가 입력됩니다. 
<br>
> **업태**와 **주요내용**(요약)은 사용자가 임의로 수정해줘야 합니다.
<br>

**주소**는 네이버 API를 활용해 me2.do 단축링크를 제공합니다. 자세한 내용은 아래 3번을 참고해주세요.
<br>

테이블 상단 메뉴 클릭을 통해 정렬 기능을 사용할 수 있습니다.
<br>
등록된 기사 중 삭제가 필요한 경우, 삭제할 행의 셀을 클릭하여 **삭제**버튼을 통해 삭제를 할 수 있습니다.
<br>

버전 v1.0.0 기준, 아래 도메인과 완벽 호환합니다.

- 네이버 뉴스 (n.news.naver.com)
- 네이버 스포츠뉴스 (sports.news.naver.com)
- 네이버 연예뉴스 (entertain.naver.com)

네이버 외 기사주소를 입력하면 등록된 meta데이터를 불러옵니다. meta가 존재하지 않는 경우 공백으로 채워지게 됩니다.

<br>

![HGUtil_기사등록](https://user-images.githubusercontent.com/74040890/220837501-e6e20a6a-8a27-43dc-9d1d-a85a5140427c.gif)


<h2> 2-2. 한글로 내보내기 </h2>

```hwpMacro.py```

테이블에 입력된 기사를 지정된 양식의 한글 파일로 내보냅니다.
<br>
테이블에 있는 데이터를 그대로 한글로 옮기는 것이기에  **주요내용**을 비롯한 모든 공백 칸을 채워주시길 바랍니다.
<br>



<br>

![HGUtil_한글](https://user-images.githubusercontent.com/74040890/220838770-96f79a83-343e-4311-bb47-3a75d3175f4e.gif)


<h2> 2-3. 메시지로 내보내기 </h2>

```toMessage.py```

테이블에서 선택된 기사를 지정된 메시지 양식으로 출력합니다.
<br>
출력되는 기사의 순서도 변경이 가능하며, 출력된 메시지를 임의로 수정할 수도 있습니다.
<br>
기사가 선택되지 않으면 준비된 메시지를 대신 출력합니다.

<br>

![HGUtil_메시지](https://user-images.githubusercontent.com/74040890/220840102-7cf2134a-c964-43a0-8f71-625b6a7f9420.gif)


<h2> 2-4. 작업 내용 저장/불러오기 </h2>

작업한 테이블 정보를 table.ini 파일로 저장할 수 있습니다. ini파일은 프로그램 경로에 생성됩니다.
<br>
**불러오기**로 경로에 있는 table.ini에서 데이터를 불러와  테이블을 복구합니다.
<br>
테이블 정렬은 직접 다시 설정해야합니다.
<br>

<h1>3. 네이버 API </h1>

```naverShorten.py```
```secret.py```에 적용된 코드

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



