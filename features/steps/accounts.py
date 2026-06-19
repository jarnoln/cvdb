from time import sleep
from behave import given, when, then
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


@given('a signed up user')
def signed_up_user(context):
    user, _ = get_user_model().objects.get_or_create(
        username=context.username,
        defaults={'email': context.email},
    )
    user.set_password(context.password)
    user.save()
    EmailAddress.objects.get_or_create(
        user=user,
        email=context.email,
        defaults={'verified': True, 'primary': True},
    )


@when('I open root page')
def open_root_page(context):
    context.browser.get(context.get_url('/'))
    sleep(1)


@when(u'I click link "{text}"')
def step_impl(context, text):
    context.browser.find_element(By.LINK_TEXT, text).click()
    sleep(2)


@when(u'I click element "{element_id}"')
def step_impl(context, element_id):
    context.browser.find_element(By.ID, element_id).click()
    sleep(2)


@when(u'I click button "{text}"')
def step_impl(context, text):
    xpath = '//button[text()="{}"]'.format(text)
    context.browser.find_element(By.XPATH, xpath).click()
    sleep(2)


@when(u'I fill signup form')
def step_impl(context):
    context.browser.find_element(By.ID, 'id_username').send_keys(context.username)
    context.browser.find_element(By.ID, 'id_email').send_keys(context.email)
    context.browser.find_element(By.ID, 'id_password1').send_keys(context.password)
    context.browser.find_element(By.ID, 'id_password2').send_keys(context.password)
    sleep(2)
    context.browser.find_element(By.ID, 'id_password2').send_keys(Keys.ENTER)
    sleep(4)


@when(u'I fill login form')
def step_impl(context):
    context.browser.find_element(By.ID, 'id_login').send_keys(context.username)
    context.browser.find_element(By.ID, 'id_password').send_keys(context.password)
    context.browser.find_element(By.ID, 'id_password').send_keys(Keys.ENTER)
    sleep(2)


@then(u'I will see title "{title}"')
def step_impl(context, title):
    context.test.assertIn(title, context.browser.title)


@then(u'I will see link "{text}"')
def step_impl(context, text):
    link = context.browser.find_element(By.LINK_TEXT, text)
    context.test.assertEqual(text, link.text)


@then(u'I will see element "{element_id}"')
def step_impl(context, element_id):
    context.browser.find_element(By.ID, element_id)


@then(u'I will see button "{text}"')
def step_impl(context, text):
    xpath = '//button[text()="{}"]'.format(text)
    context.browser.find_element(By.XPATH, xpath)