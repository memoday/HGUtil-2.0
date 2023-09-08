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
        'contentSelector' : '#articleBody > div:nth-child(2)',
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
    },
    'www.dnews.co.kr' : {
        'name' : '대한경제',
        'datetimeSelector' : '#container > div > div.view_contents.innerNews > div.newsCont > div.dateFont > em',
        'datetimeFormat' : '%Y-%m-%d %H:%M:%S',
        'datetimeTrim' : 5,
        'datetimeTrimEnd' : 2,
    },
    'www.news2day.co.kr' : {
        'name' : '뉴스투데이',
        'datetimeSelector' : '#main > div.contents.main_contents > div > div > div > div > div.layout_sortable > div.date > span:nth-child(2)',
        'datetimeFormat' : '%Y.%m.%d %H:%M',
        'datetimeTrim' : 6,
    },
    'www.cstimes.com' : {
        'name' : '컨슈머타임스',
    },
    'www.lkp.news' : {
        'name' : '리버티코리아포스트',
    },
    'www.fetv.co.kr' : {
        'name' : 'FETV',
    },
    'home.ebs.co.kr' : {
        'name' : 'EBS',
        'titleTrim' : 9,
    },
    'www.gosiweek.com' : {
        'name' : '공무원수험신문',
        'datetimeSelector' : '#pritnDiv > div.news_title > div.artc_tlt > dt > ul > li.right > div > span.nn',
        'datetimeFormat' : '%Y.%m.%d %H:%M',
        'datetimeTrimEnd' : 3,
        'titleSelector' : '#pritnDiv > div.news_title > div.artc_tlt > dl > span',
    },
    'ilyo.co.kr' : {
        'name' : '일요신문',
    },
    'www.fashionbiz.co.kr' : {
        'name' : '패션비즈',
        'titleSelector' : 'head > title:nth-child(8)',
    },
    'www.handmk.com' : {
        'name' : '핸드메이커',
    },
    'medigatenews.com' : {
         'name' : '메디게이트뉴스',
         'titleTrim' : 15,
    },
    'www.irobotnews.com' : {
        'name' : '로봇신문',
        'titleTrimEnd' : 9,
    },
    'www.kyeongin.com' : {
        'name' : '경인일보',
        'datetimeSelector' : '#content > div.view2021 > div > div.view-title-box > div.view-title > div > span > span.news-date',
        'datetimeFormat' : '%Y-%m-%d %H:%M',
        'datetimeTrim' : 14,
        'datetimeTrimEnd' : 8,
    },
    'www.cdntv.co.kr' : {
        'name' : 'CDN뉴스',
        'datetimeSelector' : '#bo_v_info > strong:nth-child(4)',
        'datetimeFormat' : '%y-%m-%d %H:%M',
    },
    'www.boannews.com' : {
        'name' : '보안뉴스',
        'datetimeSelector' : '#news_util01',
        'datetimeTrim' : 15,
    },
    'www.sisajournal-e.com' : {
        'name' : '시사저널이코노미',
    },
    'kr.aving.net' : {
        'name' : '에이빙뉴스',
    },
    'www.sentv.co.kr' : {
        'name' : '서울경제TV',
        'datetimeSelector' : '#news_print_wrap > section > section.news_home_list.section_1 > div.util-area > span.date',
        'datetimeFormat' : '%Y-%m-%d %H:%M:%S',
        'datetimeTrim' : 3,
    },
    'www.youngnong.co.kr' : {
        'name' : '한국영농신문',
        'titleTrimEnd' : 10,
    },
    'www.segyebiz.com' : {
        'name' : '세계비즈',
    },
    'www.vogue.co.kr' : {
        'name' : 'Vogue',
    },
    'www.sporbiz.co.kr' : {
        'name' : '한스경제'
    },
    'www.polinews.co.kr' : {
        'name' : '폴리뉴스'
    }, 
    'www.digitaltoday.co.kr' : {
        'name' : '디지털투데이'
    },
    'www.fntimes.com' : {
        'name' : 'fntimes'
    },
    'www.jungle.co.kr' : {
        'name' : '디자인정글',
    },
    'www.aflnews.co.kr' : {
        'name' : '농수축산신문',
        'titleSelector' : '#article-view > div > header > h3',
    },
    'news.cpbc.co.kr' : {
        'name' : '가톨릭평화방송평화신문',
        # 'datetimeSelector' : '#cnbc-front-articleHeader-self > div > div > div.ah_info > span.ahi_date',
        # 'datetimeFormat' : '%Y.%m.%d.%H:%M',
        # 'datetimeTrim' : 3,
    },
    'kenews.co.kr' : {
        'name' : '한국농촌경제신문',
        'datetimeSelector' : '#container > div > div:nth-child(1) > div > div.arv_001 > div.art_top > ul.art_info > li:nth-child(2)',
        'datetimeFormat' : '2023.%m.%d %H:%M:%S',
        'datetimeTrim' : 3,
    },
    'www.raonnews.com' : {
        'name' : '라온신문',
        'datetimeSelector' : '#container > div > div.sublay.sub_article > div.sl > div > div.arv_008 > div > div > div > ul.art_info > li:nth-child(2)',
        'datetimeFormat' : '%Y.%m.%d %H:%M:%S',
        'datetimeTrim' : 3,
    },
    'www.olchiolchi.com' : {
        'name' :'올치올치',
        'titleSelector' : '#main-content > div > div > div > div > div.et_pb_column.et_pb_column_3_4.et_pb_column_0_tb_body.et_pb_specialty_column.et_pb_css_mix_blend_mode_passthrough > div.et_pb_row_inner.et_pb_row_inner_0_tb_body.post_row > div > div.et_pb_with_border.et_pb_module.et_pb_post_title.et_pb_post_title_0_tb_body.et_pb_bg_layout_light.et_pb_text_align_center > div > h1',
    },
    'www.livesnews.com' : {
        'name' : '라이브팜뉴스',
        'datetimeSelector' : '#container > div > div:nth-child(1) > div > div.arv_001 > div.art_top > ul.art_info > li:nth-child(2)',
        'datetimeFormat' : '%Y.%m.%d %H:%M:%S',
        'datetimeTrim' : 3,
    },
    'www.businesskorea.co.kr' : {
        'name' : '비지니스코리아',
    },
    'radio.ytn.co.kr' : {
        'name' : 'YTN라디오',
    },
    'autotimes.hankyung.com' : {
        'name' : '오토타임즈',
        'datetimeSelector' : '#talklink_contents > div.view-title > p > span.i_date',
        'datetimeFormat' : '%Y-%m-%d %H:%M',
        'datetimeTrim' : 3,
        'titleSelector' : '#talklink_contents > div.view-title > h2',
    },
    'jhealthmedia.joins.com' : {
        'name' : '중앙일보 헬스미디어',
        'datetimeSelector' : '#container > div > div.left_area > div.article_head > div.clearfx > div.byline > em:nth-child(2)',
        'datetimeFormat' : '%Y.%m.%d %H:%M',
        'datetimeTrim' : 3,
        'titleTrimEnd' : 13,
    },
    'www.cnbnews.com' : {
        'name' : 'CNB뉴스',
    },
    'www.esquirekorea.co.kr':{
        'name' : '에스콰이어'
    },
    'www.economytalk.kr':{
        'name':'이코노미톡뉴스'
    },
    'www.medicaltimes.com' :{
        'name' : '메디칼타임즈',
        'datetimeSelector' : '#container > section > div > div > div.viewTitle_wrap > div:nth-child(3) > div.viewInfo_wrap.clearfix > div.date_info > span',
        'datetimeFormat' : '%Y-%m-%d %H:%M:%S',
        'datetimeTrim': 6,
    },
    'www.thevaluenews.co.kr':{
        'name':'더밸류뉴스',
        'datetimeSelector' : '#contents > div.basicView > div.viewContentWrap > div.titleWrap > div.registModifyDate > ul > li',
        'datetimeFormat' : '%Y-%m-%d %H:%M:%S',
        'datetimeTrim' : 5,
    },
    'www.ceoscoredaily.com':{
        'name':'CEO스코어데일리'
    },
    'www.finomy.com':{
        'name':'현대경제신문',
    },
    'www.mhj21.com':{
        'name':'문화저널21',
        'datetimeSelector' : '#wrap > div.article_head > div.read_option_top > div.writer_time',
        'datetimeFormat' : '%Y/%m/%d [%H:%M]',
        'datetimeRange' : [-19,-1]
    },
    'kizmom.hankyung.com':{
        'name':'키즈맘',
        'datetimeSelector' : '#container > div > div.rightWrap > div.news_con.mt23 > div.con_l > div > div.view_top_wrap > div > div.data > span:nth-child(1)',
        'datetimeFormat' : '%Y-%m-%d %H:%M:%S',
        'datetimeTrim' : 3,
    },
    'www.metroseoul.co.kr' : {
        'name' : '매트로신문',
        'datetimeSelector' : 'body > div.container > div.article-title > div > span:nth-child(2)',
        'datetimeFormat' : '%Y-%m-%d %H:%M:%S',
        'datetimeTrim' : 2,
    },
    'www.fntimes.com' : {
        'name' : '한국금융신문',
    },
    'stoo.com' : {
        'name' : '스포츠투데이',
    },
    'www.newspim.com' : {
        'name' : '뉴스핌',
        'datetimeSelector' : '#send-time',
        'datetimeFormat' : '%Y년%m월%d일 %H:%M',
        'contentSelector' : '#news-contents',
    },
    'www.cts.tv' : {
        'name' : 'CTS',
    },
    'ebn.co.kr' : {
        'name' : 'EBN',
        'datetimeSelector': '#newsInfo > li:nth-child(1)',
        'datetimeFormat' : '%Y.%m.%d %H:%M',
        'datetimeRange' : [3,19],
    },
    'www.newstree.kr':{
        'name' :'뉴스트리코리아',
        'datetimeSelector' : '#main > div.viewTitle > dl > dd',
        'datetimeFormat' : '%Y-%m-%d %H:%M:%S',
        'datetimeTrim' : -19,
    },
}