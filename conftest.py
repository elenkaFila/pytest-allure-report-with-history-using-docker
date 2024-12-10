from selenium import webdriver
import pytest
from datetime import datetime
import pytest_html
from pathlib import Path
import os

driver = None

#pytest --html=report.html
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    now = datetime.now()
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])
    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            now = datetime.now()
            report_dir = Path('Reports', now.strftime("%d_%m_%Y"))
            report_dir.mkdir(parents=True, exist_ok=True)
            item.config.option.htmlpath = report_dir / f"report_{now.strftime('%H%M%S')}.html"
            report_directory = os.path.dirname(item.config.option.htmlpath)
            item.config.option.self_contained_html = True
            #file_name = report.nodeid.replace("::", "_") + ".png"
            file_name = "screenshot_" + now.strftime("%H%M%S_%d_%m_%Y") + ".png"
            destination_file = os.path.join(report_directory, file_name)            
            driver.save_screenshot(destination_file)
            if file_name:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % file_name
                extra.append(pytest_html.extras.html(html))
        report.extra = extra

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    now = datetime.now()
    report_dir = Path('Reports', now.strftime("%d_%m_%Y"))
    report_dir.mkdir(parents=True, exist_ok=True)
    pytest_html = report_dir / f"report_{now.strftime('%H%M%S')}.html"
    config.option.htmlpath = pytest_html
    config.option.self_contained_html = True


    
def pytest_addoption(parser):
    parser.addoption("--browser", "-B", action="store", default="chrome", help="choose your browser")
    
# задаем браузер через cli
@pytest.fixture(autouse=True)
def driver(request):
    global driver
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
