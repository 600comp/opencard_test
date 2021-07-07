from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

URL = 'index.php?route=account/login'
URL_ADMIN = 'admin'
CONTENT_AUTH_HEADER = (By.CSS_SELECTOR, 'div.well h2')
ALERT_WARNING = (By.CSS_SELECTOR, 'div.alert.alert-danger.alert-dismissible')
LOGIN_BTN = (By.CSS_SELECTOR, 'input[value=Login]')
CONTINUE_BTN = (By.CSS_SELECTOR, 'a.btn.btn-primary')
LOGIN_FIELD = (By.NAME, 'email')
PASSWORD_FIELD = (By.NAME, 'password')

CONTENT_H1_HEADER = (By.CSS_SELECTOR, '#content h1')
CONTINUE_REGISTER_BTN = (By.CSS_SELECTOR, 'input[value=Continue]')

ALLERT_1HOUR_MESSAGE = ' Warning: Your account has exceeded allowed number of login attempts. Please try again in 1 hour.'
ALLERT_MESSAGE = ' Warning: No match for E-Mail Address and/or Password.'
ALLERT_REGISTER_MESSAGE = ' Warning: You must agree to the Privacy Policy!'
LOGOUT_HEADER_TEXT = 'Account Logout'

CONTENT_H2_HEADER = (By.CSS_SELECTOR, '#content h2')
MY_ACCOUNT_MENU = (By.CSS_SELECTOR, 'a[title="My Account"]')
LOGOUT_MENU_BTN = (By.XPATH, '//li[@class="dropdown open"]//a[.="Logout"]')

ADMIN_LOGIN = 'user'
ADMIN_PASSWORD = 'bitnami'

USER_LOGIN = 'test@user.ru'
USER_PASSWORD = 'A12345678'


def test_empty_fields(driver, url):
    driver.get(f'{url}/{URL}')
    driver.find_element(*LOGIN_BTN).click()

    allert_message = WebDriverWait(driver, 3).until(EC.visibility_of_element_located(ALERT_WARNING))
    assert allert_message.get_attribute('textContent') in (ALLERT_MESSAGE, ALLERT_1HOUR_MESSAGE), 'Некорректное сообщение'


def test_correct_auth(driver, url):
    driver.get(f'{url}/{URL}')
    WebDriverWait(driver, 3).until(EC.visibility_of_element_located(CONTENT_AUTH_HEADER))
    driver.find_element(*LOGIN_FIELD).send_keys(USER_LOGIN)
    driver.find_element(*PASSWORD_FIELD).send_keys(USER_PASSWORD)
    driver.find_element(*LOGIN_BTN).click()

    result = [
        'My Account',
        'My Orders',
        'My Affiliate Account',
        'Newsletter',
    ]
    h2 = [row.text for row in driver.find_elements(*CONTENT_H2_HEADER)]
    assert result == h2, 'Не совпадает информация по ценам товара'


def test_logout(driver, url):
    print(f'{url}/{URL}')
    driver.get(f'{url}/{URL}')
    WebDriverWait(driver, 3).until(EC.visibility_of_element_located(CONTENT_AUTH_HEADER))
    driver.find_element(*LOGIN_FIELD).send_keys(USER_LOGIN)
    driver.find_element(*PASSWORD_FIELD).send_keys(USER_PASSWORD)
    driver.find_element(*LOGIN_BTN).click()
    WebDriverWait(driver, 3).until(EC.visibility_of_element_located(MY_ACCOUNT_MENU))
    driver.find_element(*MY_ACCOUNT_MENU).click()
    driver.find_element(*LOGOUT_MENU_BTN).click()

    assert LOGOUT_HEADER_TEXT == driver.find_element(*CONTENT_H1_HEADER).text, 'Не произошел разлогин'


def test_new_customer(driver, url):
    test_open_register_page(driver, url)

    driver.find_element(*CONTINUE_REGISTER_BTN).click()
    allert_message = WebDriverWait(driver, 3).until(EC.visibility_of_element_located(ALERT_WARNING))
    assert ALLERT_REGISTER_MESSAGE == allert_message.get_attribute('textContent'), 'Некорректное сообщение ошибки'


def test_open_register_page(driver, url):
    driver.get(f'{url}/{URL}')
    driver.find_element(*CONTINUE_BTN).click()
    content_header = WebDriverWait(driver, 3).until(EC.visibility_of_element_located(CONTENT_H1_HEADER)).text
    assert 'Register Account' == content_header, 'Находимся не на странице регистрации'


