from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    HOST_BUTTON = ('xpath','//button[text()="Host"]')
    JOIN_BUTTON = ('xpath','//button[text()="Join"]')

    def __init__(self, driver) -> None:
        self.driver: WebDriver = driver
        self.wait = WebDriverWait(driver, 10, poll_frequency=1)
        
    def open(self):
        self.driver.get(self.PAGE_URL)

    def element_get_attribute(self, locator, attribute):
        return self.element_is_present(locator).get_attribute(attribute)

    def is_opened(self):
        self.wait.until(EC.url_to_be(self.PAGE_URL))

    def click_on_element(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()
    
    def element_is_present(self, locator):
        self.wait.until(EC.presence_of_element_located(locator))
        return True

    def click_button_join(self):
        self.click_on_element(self.JOIN_BUTTON)
        
    def click_button_host(self):
        self.click_on_element(self.HOST_BUTTON)
