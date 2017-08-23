from time import sleep
from behave import given, when, then
# from django.conf import settings


@when('I open root page')
def open_root_page(context):
    # context.browser.get(context.get_url('/'))
    context.browser.get('http://127.0.0.1:8000/')
    sleep(1)


@when(u'I will click link "{text}"')
def step_impl(context, text):
    context.browser.find_element_by_link_text(text).click()
    sleep(2)


@then(u'I will see title "{title}"')
def step_impl(context, title):
    context.test.assertIn(title, context.browser.title)


@then(u'I will see link "{text}"')
def step_impl(context, text):
    link = context.browser.find_element_by_link_text(text)
    context.test.assertEqual(text, link.text)
