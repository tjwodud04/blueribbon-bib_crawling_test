from selenium import webdriver
from selenium.webdriver.common.by import By

# 셀레니움 크롬 드라이버 옵션 세팅(Selenium driver option setting)
# service = webdriver.ChromeService("C:/Users/USER/Downloads/chrome-win64/chrome.exe")
options = webdriver.ChromeOptions()
# options.add_argument('headless') # 창 띄우지 않기 (No chrome window)
options.add_argument("no-sandbox")
options.add_experimental_option("detach", True) # 동작 이후 창 닫지 않음
options.add_argument("disable-gpu")   # 가속 사용 x
options.add_argument("lang=ko_KR")    # 가짜 플러그인 탑재
options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')  # user-agent 이름 설정

# driver = webdriver.Chrome(service=service, options=options)
driver = webdriver.Chrome(options=options)

driver.get('https://guide.michelin.com/kr/ko/selection/south-korea/restaurants/bib-gourmand')
driver.maximize_window()
driver.implicitly_wait(7)

store_click = driver.find_element(By.XPATH, value='/html/body/main/section[1]/div[1]/div/div[2]/div[1]/div/a').click()

driver.implicitly_wait(5)

store_name = driver.find_element(By.XPATH, value='/html/body/main/div[4]/div[1]/div/div[2]/section[1]/div[1]/h1')
print("가게명 : ", store_name.text)

store_location = driver.find_element(By.XPATH, value='/html/body/main/div[4]/div[1]/div/div[2]/section[1]/div[1]/ul/li[1]')
print("위치 : ", store_location.text)

food_type = driver.find_element(By.XPATH, value='/html/body/main/div[4]/div[1]/div/div[2]/section[1]/div[1]/ul/li[2]/span')
print("음식 타입 : ", food_type.text[4:])

guide_opinion = driver.find_element(By.XPATH, value='/html/body/main/div[4]/div[1]/div/div[2]/section[1]/div[2]/div[3]/p')
print("미슐랭 가이드 의견 : ", guide_opinion.text)

service_list = list()
extra_service = driver.find_elements(By.XPATH, value='/html/body/main/div[4]/div[1]/div/div[2]/section[2]/div[2]/ul')
for e in extra_service :
    items = e.text.split('\n')
    for i in range(len(items)) :
        service_list.append(items[i])

print("제공되는 추가 서비스 : ", service_list)

phone = driver.find_element(By.XPATH, value='/html/body/main/div[4]/div[1]/div/div[2]/section[4]/div[2]/div/div/div/div/div/a')
print("가게 전화번호 : ", phone.get_attribute("href"))

image_list = list()
image_numbers = driver.find_element(By.XPATH, value='/html/body/main/div[3]/div/button/span[1]')
image_button = driver.find_element(By.XPATH, value='/html/body/main/div[3]/div').click()
driver.implicitly_wait(3)

for i in range(1,int(image_numbers.text)+1) :
    image_web_location = driver.find_elements(By.XPATH, value=f'/html/body/main/div[5]/section/div/div/div/div/div/div[1]/div/div[{str(i)}]/div/div[1]/div/img')
    for e in image_web_location :
        image_link = e.get_attribute("src")
        try :
            button_click = driver.find_element(By.XPATH, value='/html/body/main/div[5]/section/div/div/div/div/div/div[2]/div[2]').click()
        except Exception:
            pass
        image_list.append(image_link)
    driver.implicitly_wait(3)

print("이미지 링크 : ", image_list)

# driver.quit() # driver 종료