import json
import re
import time
import typing as t
from datetime import datetime
from random import randint

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from lwc_common.lwc.exceptions import ProfileNotDownloadedError
from lwc_common.lwc.exceptions import CannotSolveGoogleChallenge
from lwc_common.lwc.exceptions import UnclickableButtonError
from lwc_common.lwc.drivers import ChromeDriver
from lwc_common.lwc.drivers import EdgeDriver
from lwc_common.lwc.drivers import FirefoxDriver
from lwc_common.lwc.drivers import OperaDriver


class CrawlerBase:
    linkedin_email: str = None
    linkedin_pwd: str = None
    ANTI_CAPTCHA_API_KEY: str = None
    LINKEDIN_LOGIN_URL: str = "https://www.linkedin.com/uas/login"
    LINKEDIN_BASE_URL: str = "https://www.linkedin.com/feed"
    GOOGLE_BASE_URL: str = "https://www.google.co.uk"
    GOOGLE_CHALLENGE_TIMEOUT = 60
    logger = None

    def __setup__(
            self,
            linkedin_email: str,
            linkedin_pwd: str,
            anti_captcha_api_key: str,
            logger: t.Callable = None
    ):
        self.linkedin_email = linkedin_email
        self.linkedin_pwd = linkedin_pwd
        self.ANTI_CAPTCHA_API_KEY = anti_captcha_api_key
        self.logger = logger or self.create_logger()

    def setup_anti_captcha(self):
        self.get('https://antcpt.com/blank.html')
        opts = {'options': {"antiCaptchaApiKey": self.ANTI_CAPTCHA_API_KEY}}
        self.acp_api_send_request('setOptions', opts)
        time.sleep(3)

    def acp_api_send_request(self, message_type, data=None):
        data = data or {}
        message = {
            # this receiver has to be always set as antiCaptchaPlugin
            'receiver': 'antiCaptchaPlugin',
            # request type, for example setOptions
            'type': message_type,
            # merge with additional data
            **data
        }
        # run JS code in the web page context
        # precisely we send a standard window.postMessage method
        return self.execute_script("""
        return window.postMessage({});
        """.format(json.dumps(message)))

    def solve_google_challenge(self, timeout=GOOGLE_CHALLENGE_TIMEOUT):
        if "/sorry/index" in self.current_url:
            self.logger.log(">>> Captcha hit on Google search, "
                       "sending to Anti-Captcha")
            try:
                challenge_solved = self.custom_wait(
                    lambda: isinstance(self.current_url, str)
                    and ("/sorry/index" not in self.current_url), timeout
                )
                if not challenge_solved:
                    raise CannotSolveGoogleChallenge
                self.logger.log(">>> Google Captcha solved")
                time.sleep(1.5)
            except Exception as exc:
                self.logger.log(">>> Cannot solve challenge:: {exc}")
                raise CannotSolveGoogleChallenge

    def search(self, job_title, location, pages):
        linkedin_urls = []
        self.logger.log(f"Getting profile urls for {job_title} in {location}...")

        self.get(self.GOOGLE_BASE_URL)
        # accept cookies if the popup appears
        accept_cookies_button = self.custom_wait(
            lambda: self.find_elements_by_id('L2AGLb'), 30)
        if accept_cookies_button:
            self.handle_button_interaction(accept_cookies_button, "search")
            time.sleep(1.5)

        # start search
        query_string = f'site:linkedin.com/in/ and "{job_title}" and "{location}"'
        self.fill_form_field("q", query_string, self.find_elements_by_name)
        time.sleep(1.5)
        self.fill_form_field("q", Keys.RETURN, self.find_elements_by_name, clear=False)
        time.sleep(1.5)
        self.solve_google_challenge()

        get_url = lambda x: re.search("https://[a-z]{2,3}\\.linkedin\\.com/(pub|in|profile)/[^?|&]+", x)
        loop_condition = lambda pg: True if pages == 0 else (pg <= pages)

        # loop through pages to get urls
        page = 1
        while loop_condition(page):
            # add valid urls
            url_elements = self.find_elements_by_xpath("//div[@class='yuRUbf']//a[@href]")
            urls = [elm.get_attribute("href") for elm in url_elements]
            linkedin_urls.extend(map(lambda x: get_url(x).group(0), filter(get_url, urls)))
            try:
                # go to next page
                self.find_element_by_xpath("//a[@id='pnnext']").click()
                time.sleep(2)
                self.solve_google_challenge()
            except NoSuchElementException:
                self.logger.log(f"End of Google search at page {page} (No more matches)")
                break
            except CannotSolveGoogleChallenge as exc:
                self.logger.log(f"Could not solve Google challenge "
                                f"met on page {page}. URLs found in "
                                f"previous pages returned")
                break
            page += 1
        return linkedin_urls

    def fill_form_field(
            self, element_id, value,
            finder_method: t.Callable = None,
            clear: bool = True
    ):
        finder_method = finder_method or self.find_elements_by_id
        fields = self.custom_wait(lambda: finder_method(element_id))
        if clear:
            self.handle_button_interaction(fields, action=("clear", None))
        self.handle_button_interaction(fields, action=("send_keys", value))

    def login(self, email=None, password=None, retry=True):
        email = email or self.linkedin_email
        password = password or self.linkedin_pwd
        self.get(self.LINKEDIN_LOGIN_URL)
        self.fill_form_field("username", email)
        time.sleep(1.5)
        self.fill_form_field("password", password)
        time.sleep(1.5)
        submit_btn = self.find_element_by_css_selector('button[type="submit"]')
        submit_btn.click()
        time.sleep(1.5)

        if "/challenge/" in self.current_url:
            self.logger.log(">>> Captcha hit in LinkedIn, sending to Anti-Captcha")
            self.custom_wait(
                lambda: isinstance(self.current_url, str)
                and self.current_url.startswith(self.LINKEDIN_BASE_URL), 120
            )
            self.logger.log(">>> LinkedIn Captcha solved")
            time.sleep(1.5)

        if "authwall" in self.current_url and retry:
            self.logger.log(">>> retrying login...")
            self.login(email, password, retry=False)

    def get_profile_pdf(self, profile_url):
        profile_name = profile_url.split("/in/")[-1].strip('/')
        self.get(profile_url)
        self.custom_wait(lambda: isinstance(self.current_url, str)
                         and profile_name in self.current_url, 30)
        more_buttons = self.custom_wait(
            lambda: self.find_elements_by_css_selector(
            'div[class="artdeco-dropdown artdeco-dropdown--placement-bottom '
            'artdeco-dropdown--justification-left ember-view"] '), 30
        )
        self.handle_button_interaction(more_buttons, profile_name)
        time.sleep(0.5)

        save_to_pdf_buttons = self.custom_wait(
            lambda: self.find_elements_by_css_selector(
                'div[data-control-name="save_to_pdf"]'), 15
        )
        self.handle_button_interaction(save_to_pdf_buttons, profile_name)

        profile_pdf_path = self.custom_wait(self.profile_pdf_downloaded)
        if not profile_pdf_path:
            raise ProfileNotDownloadedError(profile_name=profile_name)
        return profile_pdf_path

    @staticmethod
    def custom_wait(func: t.Callable, timeout: int = 60) -> t.Any:
        """Wait until "timeout" or function "func" returns
        a value that evaluates to True on bool(value).
        Whichever comes first"""
        in_time = lambda init: time.time() - init < timeout
        start = time.time()
        retval = None
        while (not retval) and in_time(start):
            retval = func()
            time.sleep(1)
        return retval

    @staticmethod
    def handle_button_interaction(btn_list, profile_name="", action=("click", None)):
        action, param = action
        for idx, btn in enumerate(btn_list):
            try:
                if param:
                    getattr(btn, action)(param)
                else:
                    getattr(btn, action)()
                return
            except Exception as exc:
                continue
        else:
            raise UnclickableButtonError(profile_name=profile_name)

    def create_logger(self, name=None, id=None):
        class Logger:
            def __init__(inner_self, name, session_id):
                inner_self.name = name
                inner_self.id = session_id

            def log(inner_self, message):
                text = f"[{datetime.now().strftime('%d/%b/%Y %H:%M:%S')}  " \
                       f"{inner_self.name}-{str(inner_self.id)[:5]}]:: {message}"
                print(text)
        name = name or self.name
        id = id or randint(10000, 99999)
        return Logger(name, id)


class ChromeCrawler(ChromeDriver, CrawlerBase):
    def __init__(self,
                 download_dir,
                 linkedin_email: str,
                 linkedin_pwd: str,
                 anti_captcha_api_key: str,
                 executable_path: str,
                 plugin_path: str,
                 headless: bool = True,
                 logger=None,
                 options=None
                 ):
        super().__init__(download_dir=download_dir, headless=headless,
                         executable_path=executable_path,
                         plugin_path=plugin_path,
                         options=options, teardown=False)
        self.__setup__(linkedin_email, linkedin_pwd, anti_captcha_api_key, logger)
        self.setup_anti_captcha()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()


class FirefoxCrawler(FirefoxDriver, CrawlerBase):
    def __init__(self,
                 download_dir,
                 linkedin_email: str,
                 linkedin_pwd: str,
                 anti_captcha_api_key: str,
                 executable_path: str,
                 plugin_path: str,
                 headless: bool = True,
                 logger=None,
                 options=None
                 ):
        super().__init__(download_dir=download_dir, headless=headless,
                         executable_path=executable_path,
                         plugin_path=plugin_path, 
                         options=options, teardown=False)
        self.__setup__(linkedin_email, linkedin_pwd, anti_captcha_api_key, logger)
        self.setup_anti_captcha()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()


class EdgeCrawler(EdgeDriver, CrawlerBase):
    def __init__(self,
                 download_dir,
                 linkedin_email: str,
                 linkedin_pwd: str,
                 anti_captcha_api_key: str,
                 executable_path: str,
                 plugin_path: str,
                 headless: bool = True,
                 logger=None,
                 options=None
                 ):
        super().__init__(download_dir=download_dir, headless=headless,
                         executable_path=executable_path,
                         plugin_path=plugin_path,
                         options=options, teardown=False)
        self.__setup__(linkedin_email, linkedin_pwd, anti_captcha_api_key, logger)
        self.setup_anti_captcha()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()


class OperaCrawler(OperaDriver, CrawlerBase):
    def __init__(self,
                 download_dir,
                 linkedin_email: str,
                 linkedin_pwd: str,
                 anti_captcha_api_key: str,
                 executable_path: str,
                 plugin_path: str,
                 headless: bool = True,
                 logger=None,
                 options=None
                 ):
        super().__init__(download_dir=download_dir, headless=headless,
                         executable_path=executable_path,
                         plugin_path=plugin_path,
                         options=options, teardown=False)
        self.__setup__(linkedin_email, linkedin_pwd, anti_captcha_api_key, logger)
        self.setup_anti_captcha()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.teardown:
            self.quit()
