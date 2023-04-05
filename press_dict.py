#name: 언론사 이름

#datetimeSelector : <str> 발행일자 Selector
#datetimeFormat : <str> 발행일자 날짜양식
#datetimeTrim : <int> 발행일자 앞 글자 제거
#datetimeTrim ex) '입력 2023-04-05 08:14' 일 경우 'trim = 3', [3:] = 2023-04-05 08:14
#datetimeTrimEnd : <int> 발행일자 뒷 글자 제거

#titleSelector : <str> meta값에 불필요한 값이 섞여있는 경우가 있어 특정 기사는 titleSelector로 제목을 불러옴

#contentSelector : <str> 기사 본문 Selector, 230405 본문 태그가 단순하게 되어있는 기사만 등록함
#contentCorrectionNeeded : <bool> 단순 Selector로 본문 내용을 찾지 못할 때 사용함, beautifulsoup에서 find로 태그를 찾음
#contentCorrectionFind : <str> find로 찾을 태그를 입력해야함, beautifulsoup find() 안에 바로 들어가는 string임 ex) "'div', class_='content_s'"

pressData = {
    'www.sisa-news.com': {
        'name': '시사뉴스',
        'datetimeSelector': '#container > div.column.col73.mb00 > div:nth-child(1) > div > div.arv_005_01 > div.fix_art_top > div > div > ul.art_info > li:nth-child(2)',
        'datetimeFormat': '%Y.%m.%d %H:%M:%S',
        'datetimeTrim': 3,
    },
    'www.ilyosisa.co.kr': {
        'name': '일요시사'
    },
    'www.skyedaily.com': {
        'name': '스카이데일리',
        'datetimeSelector' : '#n_view2 > div > div.articlearea > div.articletitle > div:nth-child(6) > font',
        'datetimeFormat' : '%Y-%m-%d %H:%M:%S',
        'datetimeTrim' : 3,
        'titleSelector' : '#n_view2 > div > div.articlearea > div.articletitle > div.bigtitle',
    },
    'skyedaily.com': {
        'name': '스카이데일리',
        'datetimeSelector' : '#n_view2 > div > div.articlearea > div.articletitle > div:nth-child(6) > font',
        'datetimeFormat' : '%Y-%m-%d %H:%M:%S',
        'datetimeTrim' : 3,
        'titleSelector' : '#n_view2 > div > div.articlearea > div.articletitle > div.bigtitle',
    },
    'idsn.co.kr': {
        'name': '매일안전신문'
    },
    'www.siminilbo.co.kr': {
        'name': '시민일보'
    },
    'www.wsobi.com': {
        'name': '여성소비자신문'
    },
    'realty.chosun.com': {
        'name': '땅집고'
    },
    'www.the-pr.co.kr': {
        'name': 'The PR Time'
    },
    'www.vegannews.co.kr': {
        'name': '비건뉴스'
    },
    'www.wikitree.co.kr': {
        'name': '위키트리'
    },
    'www.viva100.com': {
        'name': '브릿지경제'
    },
    'www.discoverynews.kr': {
        'name': '디스커버리뉴스'
    },
    'www.joongboo.com': {
        'name': '중부일보'
    },
    'www.nspna.com': {
        'name': 'NSP통신'
    },
    'www.asiatoday.co.kr': {
        'name': '아시아투데이'
    },
    'www.kihoilbo.co.kr': {
        'name': '기호일보'
    },
    'www.thedailypost.kr': {
        'name': '데일리포스트'
    },
    'www.donga.com': {
        'name': '동아일보'
    },
    'ch1.skbroadband.com': {
        'name': 'SK브로드밴드',
        'datetimeSelector': 'body > div.wrapper > div.container > div.contentBox > div > div.wrap_content_view > div.content_metadata > dl > dd > div > span',
        'datetimeFormat': '%Y-%m-%d %H:%M:%S',
        'contentSelector' : 'body > div.wrapper > div.container > div.contentBox > div > div.wrap_content_view',
        'contentCorrectionNeeded' : True,
        'contentCorrectionFind' : "'div', class_='content_s'",
    },
    'www.obsnews.co.kr': {
        'name': 'OBS'
    },
    'www.harpersbazaar.co.kr': {
        'name': '하퍼스바자'
    },
    'mbnmoney.mbn.co.kr': {
        'name': '매일경제TV'
    },
    'www.jeonmae.co.kr': {
        'name': '전국매일신문'
    },
    'www.queen.co.kr': {
        'name': 'Queen'
    },
    'www.foodneconomy.com': {
        'name': '푸드경제신문'
    },
    'www.ktv.go.kr': {
        'name': 'KTV국민방송'
    },
    'www.areyou.co.kr': {
        'name': '아유경제'
    },
    'www.newsmaker.or.kr': {
        'name': '뉴스메이커',
        'datetimeSelector' : 'body > table > tbody > tr > td > table:nth-child(6) > tbody > tr > td:nth-child(1) > table:nth-child(2) > tbody > tr > td > table > tbody > tr:nth-child(6) > td > table > tbody > tr > td:nth-child(2) > span > font',
        'datetimeFormat' : '%Y년 %m월 %d일 (월) %H:%M:%S',
        'titleSelector' : 'body > table > tbody > tr > td > table:nth-child(6) > tbody > tr > td:nth-child(1) > table:nth-child(2) > tbody > tr > td > table > tbody > tr:nth-child(3) > td',
    },
    'thepublic.kr': {
        'name': '더퍼블릭'
    },
    'www.ekn.kr': {
        'name': '에너지경제'
    },
    'www.goodkyung.com': {
        'name': '굿모닝경제'
    },
    'www.newstomato.com': {
        'name': '뉴스토마토',
        'datetimeSelector' : '#main-top > div.rn_container.mt90px.mb30px > div.rn_sti_case > div.rn_sdate',
        'datetimeFormat': '%Y-%m-%d %H:%M:%S',
        'datetimeTrim' : 6,
        'datetimeTrimEnd' : 19,
    },
    'www.sisaon.co.kr': {
        'name': '시사오늘'
    },
    'hobbyen-news.com': {
        'name': '하비엔뉴스'
    },
    'www.job-post.co.kr': {
        'name': '잡포스트'
    },
    'www.elle.co.kr': {
        'name': '엘르'
    },
    'www.redian.org': {
        'name': '레디앙'
    },
    'www.ajunews.com':{
        'name' : '아주경제',
        'titleSelector' : '#container > div.view > article.view_header > div.inner > h1',
    }
}

