from selenium import webdriver
import pytest

def pytest_addoption(parser):
    parser.addoption("--browser", "-B", action="store", default="chrome", help="choose your browser")
    
# задаем браузер через cli
@pytest.fixture(autouse=True)
def driver(request):
    browser_param = request.config.getoption("--browser")
    if browser_param == "chrome":        
        options = webdriver.ChromeOptions()
        options.page_load_strategy= 'eager'
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(options=options)
        
    elif browser_param == "firefox":
        driver = webdriver.Firefox()
    else:
        raise Exception(f"{request.param} is not supported!")

    request.cls.driver = driver
    request.addfinalizer(driver.close)
