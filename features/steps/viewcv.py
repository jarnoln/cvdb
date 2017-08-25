from time import sleep
from behave import given, when, then
from selenium.webdriver.common.keys import Keys
# from django.conf import settings


@when('I open root page')
def open_root_page(context):
    # context.browser.get(context.get_url('/'))
    context.browser.get('http://127.0.0.1:8000/')
    sleep(1)


@when(u'I click link "{text}"')
def step_impl(context, text):
    context.browser.find_element_by_link_text(text).click()
    sleep(2)


@when(u'I click element "{element_id}"')
def step_impl(context, element_id):
    context.browser.find_element_by_id(element_id).click()
    sleep(2)


@when(u'I click button "{text}"')
def step_impl(context, text):
    xpath = '//button[text()="{}"]'.format(text)
    context.browser.find_element_by_xpath(xpath).click()
    sleep(2)


@when(u'I fill signup form')
def step_impl(context):
    context.browser.find_element_by_id('id_username').send_keys(context.username)
    context.browser.find_element_by_id('id_email').send_keys(context.email)
    context.browser.find_element_by_id('id_password1').send_keys(context.password)
    context.browser.find_element_by_id('id_password2').send_keys(context.password)
    context.browser.find_element_by_id('id_password2').send_keys(Keys.ENTER)
    sleep(2)


@when(u'I fill login form')
def step_impl(context):
    context.browser.find_element_by_id('id_login').send_keys(context.username)
    context.browser.find_element_by_id('id_password').send_keys(context.password)
    context.browser.find_element_by_id('id_password').send_keys(Keys.ENTER)
    sleep(2)


@then(u'I will see title "{title}"')
def step_impl(context, title):
    context.test.assertIn(title, context.browser.title)


@then(u'I will see link "{text}"')
def step_impl(context, text):
    link = context.browser.find_element_by_link_text(text)
    context.test.assertEqual(text, link.text)


@then(u'I will see element "{element_id}"')
def step_impl(context, element_id):
    context.browser.find_element_by_id(element_id)


@then(u'I will see button "{text}"')
def step_impl(context, text):
    xpath = '//button[text()="{}"]'.format(text)
    context.browser.find_element_by_xpath(xpath)
