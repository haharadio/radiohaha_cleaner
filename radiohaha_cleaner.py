#radiohaha Cleaner

#Module import
from selenium import webdriver
from tqdm import tqdm
import os.path
import time
import re

print('태경이 클리너가 작동을 시작했어요.')
print('Cleaner Version: 1.1')

#driver of selenium setting
if os.path.isfile('geckodriver.exe'):
    from selenium.webdriver.firefox.options import Options
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)
    print('Browser: Firefox (Geckodriver)')
else:
    import chromedriver_autoinstaller
    chromedriver_autoinstaller.install()
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options)
    print('Browser: Chrome (Chromedriver)')

#login process
print('\n로그인을 위한 정보를 입력해 주세요.')
loginsuccess = 0
while loginsuccess == 0:
    code = input('\n식별 코드(ID)를 입력해 주세요:\n')
    pw = input('\n비밀번호를 입력해 주세요:\n')
    driver.get("https://sign.dcinside.com/login?s_url=https://www.dcinside.com/")
    driver.find_element("xpath",'//*[@id="id"]').send_keys(code)
    driver.find_element("xpath",'//*[@id="pw"]').send_keys(pw)
    driver.find_element("xpath",'/html/body/div[2]/main/div/article/section/div/div[1]/div/form/fieldset/button').click()
    try:
        loginalert = driver.switch_to.alert
        loginalert.accept()
        print('로그인이 되지않습니다. 로그인 정보를 다시 확인해 주세요')
    except:
        loginsuccess = 1
print('\nLogin Complete\n')

#Cleaning mode setting
print('무엇을 삭제할지 정해주세요.')
print('댓글만 삭제: 1 입력후 엔터')
print('글만 삭제: 2 입력후 엔터')
print('둘 다 삭제: 그냥 엔터')
mode = input()

#time term setting
print('\n삭제 시간 간격을 정해주세요.\n그냥 엔터를 누르면 기본 간격인 4초로 설정됩니다.\n경고: 4초 미만으로 설정하시면 삭제 명령 실행 속도가 인터넷 로딩속도를 추월하여 오류가 발생할 수 있어요.')
term = input()
if term == '':
    term = 4
else:
    term = int(term)
print('\n[클리너 작동시 주의사항]\n오류가 발생했을 시에는 갤로그에 들어가서 아무 글/댓글의 삭제 버튼을 눌러 캡챠를 풀고 프로그램을 다시 실행하여 주세요.')
print('캡챠가 뜨지 않는다면 캡챠에 의한 오류가 아닌 프로그램 내부의 오류이므로 프로그램을 닫고 다시 실행하여 주세요.')
print('프로그램 내부 오류가 계속 발생한다면 개발자에게 알려주세요.')
jgs = re.compile('^\(([0-9]*)\)$')

#Cleaning comment
if mode != '2':
    print('\n댓글 삭제를 시작할게요.')
    driver.get("https://gallog.dcinside.com/" + code +"/comment")
    conbr = jgs.findall(driver.find_element("xpath",'/html/body/div[1]/div[2]/main/article/div/div[3]/section/div[1]/header/div/div[1]/button[1]/span').text)[0]
    for a in tqdm(range(int(conbr)),desc='진행률'):
        driver.find_element("xpath",'/html/body/div[1]/div[2]/main/article/div/div[3]/section/div[1]/div/ul/li[1]/div/div/button').click()
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(term)
    print('댓글 삭제가 완료되었어요')
    
#Cleaning posting
if mode != '1':
    print('\n글 삭제를 시작할게요.')
    driver.get("https://gallog.dcinside.com/" + code +"/posting")
    posbr = jgs.findall(driver.find_element("xpath",'/html/body/div[1]/div[2]/main/article/div/div[3]/section/div[1]/header/div/div[1]/button[1]/span').text)[0]
    for a in tqdm(range(int(posbr)),desc='진행률'):
        driver.find_element("xpath",'/html/body/div[1]/div[2]/main/article/div/div[3]/section/div[1]/div/ul/li[1]/div/div/button').click()
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(term)
    print('글 삭제가 완료되었어요')

#End command
print('\n클리너 작동이 모두 끝났어요.')
input('엔터키를 누르면 프로그램이 종료됩니다')
driver.quit()
