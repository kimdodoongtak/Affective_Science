from konlpy.tag import Okt
from collections import Counter
import pandas as pd

df = pd.read_csv("")


# 전체 셀에서 텍스트를 수집 (NaN은 무시)
reviews = []
for col in df.columns:
    reviews += df[col].dropna().astype(str).tolist()
  # 예시로 몇 개 출력
okt = Okt()

# 제거할 의미 없는 형용사
remove_adjs = {'마르다', '이다', '같다', '있다', '없다'}
remove_nouns = {'탕','좀','수','때','또','바로','무료','직원',
                '단계','가성','매장','사장','배달','방문','더',
                '재료','비','여기','주문','이수역','요','것'}
# 커스텀 감성 명사 리스트
custom_nouns = [
    '달달', '얼얼', '쫀득', '꾸덕', '촉촉', '바삭', '진하다','마라탕','마라',
    '깔끔', '시원','내돈내산', '가성비', '존맛탱', '최고', '대박',
    '완전', '진심', '극락', '천국', '최애', '재방문'
]

all_nouns = []
all_adjs = []

for review in reviews:
    morphs = okt.pos(review, stem=True)
    
    for word, tag in morphs:
        if tag == 'Adjective' and word not in remove_adjs:
            all_adjs.append(word)
        elif tag == 'Noun' and word not in remove_nouns:
            all_nouns.append(word)
    
    # 리뷰 내에 커스텀 명사가 있으면 명사 리스트에 추가
    for keyword in custom_nouns:
        if keyword in review:
            all_nouns.append(keyword)
    

top_nouns = Counter(all_nouns).most_common(20)
top_adjs = Counter(all_adjs).most_common(10)

print("키워드(명사) Top 20:")
for noun, count in top_nouns:
    print(f"{noun}: {count}회")

print("\n 형용사 Top 10:")
for adj, count in top_adjs:
    print(f"{adj}: {count}회")