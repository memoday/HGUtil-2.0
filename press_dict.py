#name: 언론사 이름

#datetimeSelector : <str> 발행일자 Selector
#datetimeFormat : <str> 발행일자 날짜양식
#datetimeTrim : <int> 발행일자 앞 글자 제거 ex) '입력 2023-04-05 08:14' 일 경우 'trim = 3', [3:] = 2023-04-05 08:14
#datetimeTrimEnd : <int> 발행일자 뒷 글자 제거 ex) [:-<int>]
#datetimeRange : [<int>,<int>] Trim으로 발행일자 정보를 제대로 불러오지 못하는 경우 사용함

#titleSelector : <str> meta값에 불필요한 값이 섞여있는 경우가 있어 특정 기사는 titleSelector로 제목을 불러옴
#titleCorrectionNeeded : <bool> 단순 Selector로 본문 내용을 찾지 못할 때 사용함, beautifulsoup에서 find로 태그를 찾음
#titleCorrectionFind : <str> find로 찾을 태그를 입력해야함, beautifulsoup find() 안에 바로 들어가는 string임 ex) "'div', class_='content_s'"
#titleTrim : <int> 제목 앞 글자 제거
#titleTrimEnd : <int> 제목 뒷 글자 제거

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
        'name': '매일경제TV',
        'datetimeSelector' : 'body > div.container > div > div.newsview_top_area > div > div > div.left_tit > p',
        'datetimeFormat' : '%Y-%m-%d %H:%M',
        'datetimeTrim' : 5,
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
        'datetimeFormat' : '%Y년 %m월 %d일 (%a) %H:%M:%S',
        'titleSelector' : 'body > table',
        'titleCorrectionNeeded' : True,
        'titleCorrectionFind' : "'td',class_='view_t'",
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
        'datetimeTrimEnd' : 37,
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
    'www.ajunews.com': {
        'name' : '아주경제',
        'titleSelector' : '#container > div.view > article.view_header > div.inner > h1',
    },
    'www.metroseoul.co.kr' : {
        'name' : '메트로신문',
        'datetimeSelector' : 'body > div.container > div.article-title > div > span:nth-child(2)',
        'datetimeFormat' : '%Y-%m-%d %H:%M:%S',
        'datetimeTrim' : 2,
    },
    'www.mediapen.com' : {
        'name' : '미디어펜',
        'datetimeSelector' : '#wrap > div.container > div > div.article-warp > div.article-content.pt-20.text-center > div:nth-child(1) > div.article-top.pt-20 > div.date-repoter',
        'datetimeRange' : [0,18],
        'datetimeFormat' : '%Y-%m-%d %H:%M:%S',
    },
    'www.lak.co.kr' : {
        'name' : '환경과조경',
        'datetimeSelector' : '#forPrint > div.btn_tools.viewtitle > ul > li:nth-child(1)',
        'datetimeFormat' : '%Y-%m-%d %H:%M',
        'datetimeTrim' : 3,
        'titleTrimEnd' : 13,
    },
    'theviewers.co.kr' : {
        'name' : '뷰어스',
        'datetimeSelector' : '#wrapper > div.sub-container > div.sub-layout > div.cont-article > article > div > div.info-area > span.mid-space',
        'datetimeFormat' : '%Y.%m.%d %H:%M',
        'datetimeTrim' : 32,
        'titleTrimEnd' : 6,
    },
    'www.kyongbuk.co.kr' : {
        'name' : '경북일보',
    },
    'www.ifm.kr' : {
        'name' : '경인방송',
        'datetimeSelector' : '#main_content > div.article_header > div > div > span:nth-child(1)',
        'datetimeFormat' : '%Y-%m-%d %H:%M'
    },
    'www.econotelling.com' : {
        'name' : '이코노텔링',
    },
    'www.sportsw.kr' : {
        'name' : '스포츠W'
    },
    'weekly.cnbnews.com' : {
        'name' : 'CNB저널(문화경제)',
        'datetimeSelector' : '#container_v2 > div > div > div > div.section_h12_v2 > div.section_12_v2 > div.m01_arv1 > div.viewsubject > p',
        'datetimeFormat' : '%Y.%m.%d %H:%M:%S',
        'datetimeTrim' : -19,
    },
    'www.allurekorea.com' : {
        'name' : 'allure',
    },
    'tbs.seoul.kr' : {
        'name' : 'TBS',
        'titleTrimEnd' : 18,
    },
    'www.naeil.com' : {
        'name' : '내일신문',
        'datetimeSelector' : '#contentArea > div.caL2 > div > div.articleArea > div.date',
        'datetimeFormat' : '%Y-%m-%d %H:%M:%S',
        'datetimeTrimEnd' : 3,
    },
    'news.bbsi.co.kr' : {
        'name' : 'BBS NEWS',
        'datetimeSelector' : '#article-view > div > header > div > article:nth-child(1) > ul > li:nth-child(2)',
        'datetimeFormat' : '%Y.%m.%d %H:%M',
        'datetimeTrim' : 4,
        'titleSelector' : '#article-view > div > header > h3',
    },
    'www.e2news.com' : {
        'name' : '이투뉴스',
    },
    'www.todayenergy.kr' : {
        'name' : '투데이에너지',
        'datetimeSelector' : '#user-container > div.float-center.max-width-1280 > header > section > div > ul > li:nth-child(2)',
        'datetimeFormat' : '%Y.%m.%d %H:%M',
        'datetimeTrim' : 4,
    },
    'www.tournews21.com' : {
        'name' : '투어코리아',
    },
    'www.sportsq.co.kr' : {
        'name' : '스포츠Q',
    }
}