from selenium import webdriver
from time import sleep


def before_all(context):
    context.browser = webdriver.Firefox()


def after_all(context):
    sleep(1)
    context.browser.close()  # Use close instead of quit (because quit gives error)
    context.browser = None


def before_feature(context, feature):
    pass
