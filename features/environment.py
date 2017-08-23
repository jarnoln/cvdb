from selenium import webdriver
from time import sleep


def before_all(context):
    context.browser = webdriver.Firefox()
    context.username = 'test_user'
    context.email = 'test_user@example.com'
    context.password = 'test_password'


def after_all(context):
    sleep(1)
    context.browser.close()  # Use close instead of quit (because quit gives error)
    # context.browser = None


def before_feature(context, feature):
    pass
