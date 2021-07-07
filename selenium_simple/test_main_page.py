from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

CART = (By.CSS_SELECTOR, 'div#cart')
CART_BTN = (By.CSS_SELECTOR, 'button.btn-lg.dropdown-toggle')
EMPTY_TEXT_CART = (By.CSS_SELECTOR, 'ul.dropdown-menu.pull-right p')
ALERT_SUCCESS = (By.CSS_SELECTOR, 'div.alert.alert-success.alert-dismissible')
ALERT_DISMISS = (By.CSS_SELECTOR, 'button[data-dismiss="alert"]')
ALLERT_MESSAGE = ' Success: You have added MacBook to your shopping cart! ×'
TOP_PANEL = (By.CSS_SELECTOR, 'nav#top')

CART_OPEN = (By.CSS_SELECTOR, 'div#cart.open')
ADD_MAC_BOOK = (By.CSS_SELECTOR, 'button[onclick="cart.add(\'43\');"]')
DROP_MENU = (By.CSS_SELECTOR, 'ul.dropdown-menu.pull-right')
DROP_MENU_PRICES = (By.CSS_SELECTOR, f'{DROP_MENU[1]} tr')
DROP_MENU_DEL_BTN = (By.CSS_SELECTOR, f'button.btn-danger')


def test_empty_cart(driver):
    WebDriverWait(driver, 3).until(EC.element_to_be_clickable(CART_BTN)).click()
    WebDriverWait(driver, 3).until(EC.visibility_of_element_located(CART_OPEN))
    assert 'Your shopping cart is empty!' == driver.find_element(*EMPTY_TEXT_CART).text, 'Козина не пуста'


def test_add_in_cart(driver):
    driver.find_element(*ADD_MAC_BOOK).click()
    driver.execute_script("window.scrollTo(0, 0);")

    WebDriverWait(driver, 3).until(EC.element_to_be_clickable(CART_BTN)).click()
    WebDriverWait(driver, 3).until(EC.visibility_of_element_located(CART_OPEN))
    result = [
        'MacBook x 1 $602.00',
        'Sub-Total $500.00',
        'Eco Tax (-2.00) $2.00',
        'VAT (20%) $100.00',
        'Total $602.00'
    ]
    prices = [row.text for row in driver.find_elements(*DROP_MENU_PRICES)]
    assert result == prices, 'Не совпадает информация по ценам товара'


def test_allert_add_porition(driver):
    driver.find_element(*ADD_MAC_BOOK).click()
    driver.execute_script("window.scrollTo(0, 0);")

    allert_message = WebDriverWait(driver, 3).until(EC.visibility_of_element_located(ALERT_SUCCESS))
    assert ALLERT_MESSAGE == allert_message.get_attribute('textContent'), \
        'Некорректное сообщение'


def test_close_allert_add_porition(driver):
    driver.find_element(*ADD_MAC_BOOK).click()
    driver.execute_script("window.scrollTo(0, 0);")

    WebDriverWait(driver, 3).until(EC.visibility_of_element_located(ALERT_SUCCESS))
    driver.find_element(*ALERT_DISMISS).click()
    try:
        message = driver.find_element(*ALERT_SUCCESS).text
    except NoSuchElementException:
        result = True
    else:
        result = False

    assert result, f'Присутствует сообщение добавления товара: "{message}"'


def test_deleted_all_positions_cart(driver):
    driver.find_element(*ADD_MAC_BOOK).click()
    driver.execute_script("window.scrollTo(0, 0);")

    WebDriverWait(driver, 3).until(EC.element_to_be_clickable(CART_BTN)).click()
    WebDriverWait(driver, 3).until(EC.visibility_of_element_located(CART_OPEN))

    [position.click() for position in driver.find_elements(*DROP_MENU_DEL_BTN)]
    test_empty_cart(driver)
