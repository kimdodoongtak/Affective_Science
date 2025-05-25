import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openpyxl import Workbook

# 크롬 드라이버 설정
chrome_options = Options()
chrome_options.add_argument("--start-maximized")

# 크롬 드라이버 실행
driver = webdriver.Chrome(options=chrome_options)

# 타겟 URL
target_url = '_'

# 엑셀 워크북 생성
now = datetime.datetime.now()
xlsx = Workbook()
list_sheet = xlsx.create_sheet('output')
list_sheet.append(['content', 'date', 'tag_text'])

try:
    driver.get(target_url)

    # 리뷰 영역 로딩 대기
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'li.place_apply_pui.EjjAW'))
        )
        print("리뷰 목록 로딩 완료!")
    except TimeoutException:
        print("리뷰 목록이 로딩되지 않음")
        driver.quit()
        exit()

    time.sleep(1)

    collected_reviews = 0
    max_reviews = 100

    while collected_reviews < max_reviews:
        reviews = driver.find_elements(By.CSS_SELECTOR, 'li.place_apply_pui.EjjAW')

        for review in reviews[collected_reviews:]:
            if collected_reviews >= max_reviews:
                break

            try:
                date = ''
                blind_spans = review.find_elements(By.CSS_SELECTOR, 'span.pui__blind')
                for span in blind_spans:
                    if '년' in span.text and '월' in span.text:
                        date = span.text.strip()
                        break

                content = review.find_element(By.CSS_SELECTOR, 'div.pui__vn15t2 > a').text

                try:
                    more_tag_button = review.find_element(By.CSS_SELECTOR, 'a.pui__jhpEyP.pui__ggzZJ8')
                    driver.execute_script("arguments[0].click();", more_tag_button)
                    time.sleep(0.3)
                except NoSuchElementException:
                    pass  # 태그 더보기 버튼 없음

                tag_elements = review.find_elements(By.CSS_SELECTOR, 'div.pui__HLNvmI > span.pui__jhpEyP')
                tags = [tag.text.strip() for tag in tag_elements]
                tag_text = ', '.join(tags)

                list_sheet.append([content, date, tag_text])
                collected_reviews += 1

            except Exception as e:
                print("리뷰 추출 중 오류:", e)
                continue

        # 더보기 버튼 클릭 시도
        try:
            more_button = driver.find_element(By.CSS_SELECTOR, 'a.fvwqf')
            driver.execute_script("arguments[0].click();", more_button)
            time.sleep(1.5)
        except NoSuchElementException:
            print("더 이상 누를 더보기 버튼이 없습니다")
            break
        except ElementClickInterceptedException:
            print("클릭이 막혔습니다")
            time.sleep(1)

finally:
    file_path = f'{now.strftime("%Y-%m-%d_%H-%M-%S")}.xlsx'
    xlsx.save(file_path)
    driver.quit()
    print(f"🎉 리뷰 수집 완료! 총 {collected_reviews}개 저장됨 → {file_path}")