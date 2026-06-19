from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep


def before_all(context):
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1280,1024')
    context.browser = webdriver.Chrome(options=options)
    context.username = 'test_user'
    context.email = 'test_user@example.com'
    context.password = 'test_password'


def after_all(context):
    sleep(1)
    context.browser.quit()


def before_feature(context, feature):
    pass