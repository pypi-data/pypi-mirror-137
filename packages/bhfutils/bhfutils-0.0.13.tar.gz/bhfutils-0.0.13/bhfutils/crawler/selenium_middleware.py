# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import time

from scrapy import signals
from selenium import webdriver
from selenium_stealth import stealth
from scrapy.exceptions import NotConfigured
from selenium.webdriver.common.by import By
from scrapy.http import HtmlResponse, Response
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SeleniumDownloaderMiddleware:
    """Scrapy middleware handling the requests using selenium"""

    def __init__(self, platform, driver_executable_path, driver_arguments,
                 browser_executable_path):
        """Initialize the selenium webdriver

        Parameters
        ----------
        driver_name: str
            The selenium ``WebDriver`` to use
        driver_executable_path: str
            The path of the executable binary of the driver
        driver_arguments: list
            A list of arguments to initialize the driver
        browser_executable_path: str
            The path of the executable binary of the browser
        """

        driver_options = webdriver.ChromeOptions()
        if browser_executable_path:
            driver_options.binary_location = browser_executable_path
        driver_options.add_argument("--headless")
        driver_options.add_argument("start-maximized")
        driver_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        driver_options.add_experimental_option('useAutomationExtension', False)
        for argument in driver_arguments:
            driver_options.add_argument(argument)

        self.driver = webdriver.Chrome(options=driver_options, executable_path=driver_executable_path)

        stealth(self.driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform=platform,
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
                )

    @classmethod
    def from_crawler(cls, crawler):
        """Initialize the middleware with the crawler settings"""

        platform = crawler.settings.get('PLATFORM')
        driver_executable_path = crawler.settings.get('SELENIUM_DRIVER_EXECUTABLE_PATH')
        browser_executable_path = crawler.settings.get('SELENIUM_BROWSER_EXECUTABLE_PATH')
        driver_arguments = crawler.settings.get('SELENIUM_DRIVER_ARGUMENTS')

        if not platform or not driver_executable_path:
            raise NotConfigured(
                'SELENIUM_DRIVER_NAME and SELENIUM_DRIVER_EXECUTABLE_PATH must be set'
            )

        middleware = cls(
            platform=platform,
            driver_executable_path=driver_executable_path,
            driver_arguments=driver_arguments,
            browser_executable_path=browser_executable_path
        )

        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)

        return middleware

    def process_request(self, request, spider):
        for cookie_name, cookie_value in request.cookies.items():
            self.driver.add_cookie(
                {
                    'name': cookie_name,
                    'value': cookie_value
                }
            )

        self.driver.get(request.url)

        if "wait_text_to_be_present" in request.meta:
            try:
                if isinstance(request.meta['wait_text_to_be_present'], dict):
                    time.sleep(2)
                    conditionsDict = request.meta['wait_text_to_be_present']
                    for condition in conditionsDict:
                        if self.driver.current_url.startswith(condition):
                            WebDriverWait(self.driver, 30).until(
                                EC.text_to_be_present_in_element(
                                    (By.CSS_SELECTOR, conditionsDict[condition]), '')
                            )
                else:
                    WebDriverWait(self.driver, 30).until(
                        EC.text_to_be_present_in_element(
                            (By.CSS_SELECTOR, request.meta['wait_text_to_be_present']), '')
                    )
            except TimeoutException:
                return Response('', status=504)
            del request.meta['wait_text_to_be_present']

        if "wait_to_be_clickable" in request.meta:
            try:
                if isinstance(request.meta['wait_to_be_clickable'], dict):
                    time.sleep(2)
                    conditionsDict = request.meta['wait_to_be_clickable']
                    for condition in conditionsDict:
                        if self.driver.current_url.startswith(condition):
                            WebDriverWait(self.driver, 30).until(
                                EC.element_to_be_clickable(
                                    (By.CSS_SELECTOR, conditionsDict[condition]))
                            )
                else:
                    WebDriverWait(self.driver, 30).until(
                        EC.element_to_be_clickable(
                            (By.CSS_SELECTOR, request.meta['wait_to_be_clickable']))
                    )
            except TimeoutException:
                return Response('', status=504)
            del request.meta['wait_to_be_clickable']

        if "post_load_script" in request.meta:
            try:
                scriptCommands = request.meta['post_load_script']
                for scriptCommand in scriptCommands:
                    exec(scriptCommand)
            except:
                return Response('', status=504)
            del request.meta['post_load_script']

        body = str.encode(self.driver.page_source)

        # Expose the driver via the "meta" attribute
        request.meta.update({'driver': self.driver})

        return HtmlResponse(
            self.driver.current_url,
            body=body,
            encoding='utf-8',
            request=request
        )

    def spider_closed(self):
        """Shutdown the driver when spider is closed"""

        self.driver.quit()
