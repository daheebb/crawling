# %%
import requests
import bs4
import time
import pandas as pd
import re

url = "https://www.smu.ac.kr/kor/life/notice.do?mode=list&srCampus=smu&articleLimit=10&article.offset=0"
html = requests.get(url).text
soup = bs4.BeautifulSoup(html, "html.parser")

data = []
css_selector = ".board-thumb-content-wrap"

for tag in soup.select(css_selector):
    # 카테고리 추출
    category = tag.select_one("span.cate").get_text(strip=True) if tag.select_one("span.cate") else "미분류"
    
    # 제목 추출
    title = tag.select_one("td:nth-child(3) a").get_text(strip=True)
    
    # 날짜 추출 및 클리닝
    # "작성일 2026-01-21" 형태에서 숫자와 하이픈만 남김
    raw_date = tag.select_one("li.board-thumb-content-date").get_text(strip=True)
    clean_date = re.sub(r'[^0-9\-]', '', raw_date) 
    
    # 링크 추출
    link_tag = tag.select_one("a")
    link = "https://www.smu.ac.kr" + link_tag["href"] if link_tag else ""

    data.append((category, title, clean_date, link))
    time.sleep(0.1)

# 데이터프레임 생성
df = pd.DataFrame(data=data, columns=["분류", "제목", "날짜", "url"])

# 형식을 '%Y-%m-%d'로 지정
df['날짜'] = pd.to_datetime(df['날짜'], format='%Y-%m-%d', errors='coerce')

# 전처리 후 결과 확인을 위해 정렬 (최신순)
df = df.sort_values(by='날짜', ascending=False)

# CSV 저장
df.to_csv("상명대_공지사항_fiiiinaㅣㅣㅣl.csv", index=False, encoding="utf-8-sig")

print("CSV 저장 완료")
print(df.head())
print("\n컬럼 타입 확인:")
print(df.dtypes) # 날짜 컬럼이 datetime64인지 확인

# %%
# !pip install feedgen

# %%
from feedgen. feed import FeedGenerator
fg = FeedGenerator()
fg.id('http://lernfunk.de/media/654321')
fg.title('Some Testfeed')
fg.author( {'name':'John Doe','email':'john@example.de'} )
fg.link( href='http://example.com', rel='alternate' )
fg.logo('http://ex.com/logo.jpg')
fg.subtitle('This is a cool feed!')
fg.link( href='http://larskiesow.de/test.atom', rel='self' )
fg. language('en')
fg.rss_file('docs/rss.xml')


# %% [markdown]
# 



