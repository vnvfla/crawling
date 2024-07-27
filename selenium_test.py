from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait as wait

from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By

import time
import pyautogui
import pyperclip

# 브라우저 꺼짐 방지
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

# 불필요한 에러메시지 노출 방지
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

# Chrome driver Manager를 통해 크롬 드라이버 자동 설치
service = Service(excutable_path=ChromeDriverManager().install()) 
driver = webdriver.Chrome(service=service, options = chrome_options)

# 프레시밀 로그인 페이지 접속
url = 'https://front.cjfreshmeal.co.kr/login?redirectUrl=/mypage'
driver.get(url)

driver.implicitly_wait(5)

# id 입력창 복사/붙여놓기 허용
id = driver.find_element(By.CSS_SELECTOR, '#userId')
id.click()
pyperclip.copy('userid')
pyautogui.hotkey('ctrl', 'v')
time.sleep(2)

# password 입력창 복사/붙여놓기 허용
pw = driver.find_element(By.CSS_SELECTOR, '#userPw')
pw.click()
pyperclip.copy('userpw')
pyautogui.hotkey('ctrl', 'v')
time.sleep(2)

# login 버튼 클릭
login_btn = driver.find_element(By.CSS_SELECTOR, '#fs_login')
login_btn.click()
time.sleep(2)

# 오늘의 메뉴 페이지 이동
driver.get('https://front.cjfreshmeal.co.kr/menu/today')

# 메뉴 정보 출력
menu_view = driver.find_element(By.XPATH, '//*[@id="app"]/section/div[1]/div/div/div')
print(menu_view.text)

time.sleep(2)

# 브라우저 종료
driver.quit()
