from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait as wait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from apscheduler.schedulers.blocking import BlockingScheduler

import time
import pyautogui
import pyperclip
import telegram
import asyncio

def job():

    # 브라우저 꺼짐 방지
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    # 불필요한 에러메시지 노출 방지
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])

    # Chrome driver Manager를 통해 크롬 드라이버 자동 설치
    service = Service(excutable_path=ChromeDriverManager().install()) 
    driver = webdriver.Chrome(service=service, options = chrome_options)

    # 텔레그램봇 설정
    bot_token = 'bot_token'
    bot = telegram.Bot(token=bot_token)
    chat_id = 'chat_id'

    # 프레시밀 로그인 페이지 접속
    url = 'https://front.cjfreshmeal.co.kr/login?redirectUrl=/mypage'
    driver.get(url)
    driver.implicitly_wait(5)

    # id 입력창 복사/붙여놓기 허용
    id = driver.find_element(By.CSS_SELECTOR, '#userId')
    id.click()
    pyperclip.copy('userId')
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(2)

    # password 입력창 복사/붙여놓기 허용
    pw = driver.find_element(By.CSS_SELECTOR, '#userPw')
    pw.click()
    pyperclip.copy('userPw')
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(2)

    # login 버튼 클릭
    login_btn = driver.find_element(By.CSS_SELECTOR, '#fs_login')
    login_btn.click()
    time.sleep(2)

    # 오늘의 메뉴 페이지 이동
    driver.get('https://front.cjfreshmeal.co.kr/menu/today')

    # 메뉴 정보 출력 #app > section > div.content > section > div.sub-titile-wrap > div.btn-list2.menu-today-page > a:nth-child(2)
    menu_select = driver.find_element(By.CSS_SELECTOR, '#app > section > div.content > section > div.sub-title-wrap > div.btn-list2.menu-today-page > a.active')
    menu_select.click()                                 
    time.sleep(1)

    # 메뉴추출
    menu_main = driver.find_element(By.XPATH, '//*[@id="app"]/section/div[1]/div/div/ul/li[1]/div/a/dl/dt/span')
    menu_sub = driver.find_element(By.XPATH, '//*[@id="app"]/section/div[1]/div/div/ul/li[1]/div/a/dl/dd')

    # style에 있는 이미지 경로 추출
    menu_image_tag = driver.find_element(By.CSS_SELECTOR, '#app > section > div.content > div > div> ul > li:nth-child(1) > div > a > span > div').get_attribute('style')
    if menu_image_tag:
        menu_image = menu_image_tag.split('background-image: url("')[1][:3]
    else:
        menu_image = ''

    print(menu_main.text)

    time.sleep(2)

    # 텔레그램 메시지 전송(비동기전송)
    asyncio.run(bot.sendMessage(chat_id = chat_id, text = menu_main.text + '\n' + menu_sub.text + '\n' +menu_image))

    # schedule.every().monday.at("10:30").do(job)

    # 브라우저 종료
    driver.quit()

def job_end():
    # 스케즐러 종료
    sched.shutdow()

# 스케즐러 실행
sched = BlockingScheduler(timezone='Asia/Seoul')
sched.add_job(job, 'cron', day_of_week='mon-fri', hour='11', minute='35')

sched.start()
