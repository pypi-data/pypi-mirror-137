import os.path
import sys

from selenium import webdriver
from msedge.selenium_tools import Edge, EdgeOptions

from lwc_common.common import constants


class ChromeDriver(webdriver.Chrome):
    """
    Creates a class ChromeDriver that inherits from webdriver.Chrome
    """
    drivers = {
        "linux": constants.CHROME_LINUX_DRIVER_PATH,
        "win32": None,
        "darwin": None
    }
    download_dir: str = constants.PROFILE_DOWNLOAD_DIR

    def __init__(self, download_dir=None, headless=True, teardown=False, executable_path=None, options=None):
        """
        Instantiates a ChromeDriver object.
        :param driver_path: Defines the path of the chrome driver executable.
        :param teardown: Boolean, defines the state of the chrome instance after call.
                         True: Chrome instance closes immediately, after run.
                         False: Chrome instance is persisted.
        :param options: Defines a list of optional arguments for the chrome driver.
        """
        self.download_dir = download_dir or self.download_dir
        self.options = options or self.create_custom_options(self.download_dir, headless)
        self.teardown = teardown
        self.driver_path = self.drivers.get(sys.platform)
        super().__init__(
            executable_path=executable_path or self.driver_path,
            options=self.options
        )

    @staticmethod
    def create_custom_options(download_dir=None, headless=True, option_obj=None):
        opts = option_obj or webdriver.ChromeOptions()
        opts.add_argument('--disable-dev-shm-usage')
        # opts.add_argument('--no-sandbox')
        if headless:
            opts.add_argument("--headless")
        prefs = {"download.default_directory": download_dir}
        opts.add_experimental_option("prefs", prefs)

        # to prevent bot detection
        opts.add_argument('--disable-blink-features=AutomationControlled')
        opts.add_experimental_option("excludeSwitches", ["enable-automation"])
        opts.add_experimental_option('useAutomationExtension', False)

        # Chrome Anti-Captcha plugin extension
        opts.add_extension(constants.CHROME_PLUGIN_PATH)
        return opts

    def profile_pdf_downloaded(self):
        for dir_, _, files in os.walk(self.download_dir):
            input_file_path = os.path.join(dir_, "Profile.pdf")
            part_file = os.path.join(dir_, "Profile.pdf.crdownload")
            if os.path.isfile(input_file_path) \
                    and (not os.path.exists(part_file)):
                return input_file_path
        return ""


class OperaDriver(webdriver.Opera):
    """As of Selenium version "3.141.0" `webdriver.Opera`
    depends on Chromium. So we just subclass our own customized
    Chrome class here"""
    drivers = {
        "linux": constants.OPERA_LINUX_DRIVER_PATH,
        "win32": constants.OPERA_WIN_DRIVER_PATH,
        "darwin": None
    }
    download_dir: str = constants.PROFILE_DOWNLOAD_DIR

    def __init__(self, download_dir=None, headless=True, teardown=False, executable_path=None, options=None):
        self.download_dir = download_dir or self.download_dir
        self.options = options or self.opera_options(self.download_dir, headless)
        self.teardown = teardown
        self.driver_path = self.drivers.get(sys.platform)
        super().__init__(
            executable_path=executable_path or self.driver_path,
            options=self.options
        )

    @staticmethod
    def opera_options(download_dir=None, headless=True):
        options = ChromeDriver.create_custom_options(download_dir, headless)
        return options


class FirefoxDriver(webdriver.Firefox):
    drivers = {
        "linux": constants.FIREFOX_LINUX_DRIVER_PATH,
        "win32": constants.FIREFOX_WIN_DRIVER_PATH,
        "darwin": constants.FIREFOX_MAC_DRIVER_PATH
    }
    download_dir: str = constants.PROFILE_DOWNLOAD_DIR

    def __init__(self, download_dir=None, headless=True, teardown=False, executable_path=None, options=None):
        self.teardown = teardown
        self.download_dir = download_dir or self.download_dir
        def_profile, def_options = self.firefox_options(self.download_dir, headless)
        self.options = options or def_options
        super().__init__(
            executable_path=executable_path or self.drivers.get(sys.platform),
            firefox_profile=def_profile,
            options=self.options,
            service_log_path=os.path.join(constants.PROJECT_ROOT, "geckodriver.log")
        )
        self.install_addon(constants.FIREFOX_PLUGIN_PATH, temporary=True)
        self.firefox_profile.add_extension(extension=constants.FIREFOX_PLUGIN_PATH)
        self.firefox_profile.set_preference("security.fileuri.strict_origin_policy", False)
        self.firefox_profile.update_preferences()

    @staticmethod
    def firefox_options(download_dir, headless):
        profile = webdriver.FirefoxProfile()
        profile.set_preference(
            "browser.helperApps.neverAsk.saveToDisk",
            "application/pdf;text/plain;application/text;text/xml;application/xml"
        )
        profile.set_preference(
            "browser.download.manager.showWhenStarting", False
        )
        profile.set_preference("browser.download.dir", download_dir)
        profile.set_preference("browser.download.folderList", 2)
        profile.set_preference("pdfjs.disabled", True)
        profile.set_preference("browser.helperApps.alwaysAsk.force", False)

        options = webdriver.FirefoxOptions()
        options.log.level = "trace"  # Debug
        options.headless = headless
        return profile, options

    def profile_pdf_downloaded(self):
        for dir_, _, files in os.walk(self.download_dir):
            input_file_path = os.path.join(dir_, "Profile.pdf")
            part_file = os.path.join(dir_, "Profile.pdf.part")
            if os.path.isfile(input_file_path) \
                    and (not os.path.exists(part_file)):
                return input_file_path
        return ""


class EdgeDriver(Edge):
    drivers = {
        "linux": constants.EDGE_LINUX_DRIVER_PATH,
        "win32": constants.EDGE_WIN_DRIVER_PATH,
        "darwin": None
    }
    download_dir: str = constants.PROFILE_DOWNLOAD_DIR

    def __init__(self, download_dir=None, headless=True, teardown=False, executable_path=None, options=None):
        self.download_dir = download_dir or self.download_dir
        self.teardown = teardown
        self.options = options or self.edge_options(self.download_dir, headless)
        self.options.binary_location = self.drivers.get(sys.platform)
        super().__init__(
            executable_path=executable_path or self.drivers.get(sys.platform),
            options=self.options
        )

    @staticmethod
    def edge_options(download_dir=None, headless=True):
        options = EdgeOptions()
        options.use_chromium = True
        options = ChromeDriver.create_custom_options(download_dir, headless, option_obj=options)
        return options

    def launch_browser(self):
        # An Edge browser is return to the calling Object
        self.maximize_window()
        return self

    def __enter__(self):
        return self
