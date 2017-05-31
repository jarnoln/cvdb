from behave import given, when, then
# from django.conf import settings


@when('I open root page')
def open_root_page(context):
    # context.browser.get(context.get_url('/'))
    context.browser.get('http://127.0.0.1:8000/')


@then(u'I will see title "{title}"')
def step_impl(context, title):
    context.test.assertIn(title, context.browser.title)
