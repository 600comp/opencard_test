# docker-compose: https://habr.com/ru/company/ruvds/blog/450312/
# https://pypi.org/project/pytest-httpretty/ Перехват запросов

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def pytest_addoption(parser):
    parser.addoption('--url', action="store", default="http://192.168.0.34")
    parser.addoption('--browser', action="store", default='chrome')

@pytest.fixture(autouse=True)
def url(request):
    return request.config.getoption('--url').lower()

@pytest.fixture
def driver(request):
    browser = request.config.getoption('--browser').lower()
    _driver = None

    if browser == 'firefox':
        _driver = webdriver.Firefox()

    elif browser == 'opera':
        _driver = webdriver.Opera()
    else:
        chrome_options = Options()
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--incognito")
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

        _driver = webdriver.Chrome(options=chrome_options)

    _driver.get(request.config.getoption('--url').lower())
    _driver.maximize_window()

    def close_browser():
        _driver.quit()

    request.addfinalizer(close_browser)

    return _driver
