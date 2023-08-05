import os

# ====================================================
#                      PATHS
# ====================================================
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BIN_DIR = os.path.join(PROJECT_ROOT, "bin")
PROFILE_DOWNLOAD_DIR = os.path.join(PROJECT_ROOT, "profiles")
MASTER_LIST = os.path.join(PROJECT_ROOT, "master.json")

# create necessary directories and files
os.makedirs(PROFILE_DOWNLOAD_DIR, exist_ok=True)
open(MASTER_LIST, "a").close()

# ====================================================
#                    WEB_DRIVERS
# ====================================================
CHROME_LINUX_DRIVER_PATH = os.path.join(BIN_DIR, "chromedriver_linux64", "chromedriver")
CHROME_PLUGIN_PATH = os.path.join(BIN_DIR, "chromedriver_linux64", "anticaptcha-plugin.crx")

FIREFOX_LINUX_DRIVER_PATH = os.path.join(BIN_DIR, "geckodriver-v0.30.0-linux64", "geckodriver")
FIREFOX_WIN_DRIVER_PATH = os.path.join(BIN_DIR, "geckodriver-v0.30.0-win64", "geckodriver.exe")
FIREFOX_MAC_DRIVER_PATH = os.path.join(BIN_DIR, "geckodriver-v0.30.0-macos", "geckodriver")
FIREFOX_PLUGIN_PATH = os.path.join(BIN_DIR, "geckodriver-v0.30.0-linux64", "anticaptcha-plugin.xpi")

EDGE_LINUX_DRIVER_PATH = os.path.join(BIN_DIR, "edgedriver_linux64", "msedgedriver")
EDGE_WIN_DRIVER_PATH = os.path.join(BIN_DIR, "edge_webdrive", "msedgedriver.exe")
OPERA_LINUX_DRIVER_PATH = os.path.join(BIN_DIR, "opera_driver_linux", "operadriver_linux64")
OPERA_WIN_DRIVER_PATH = os.path.join(BIN_DIR, "opera_driver_wins", "operadriver.exe")

# ====================================================
#                       SECRETS
# ====================================================
ANTI_CAPTCHA_API_KEY = os.getenv("ANTI_CAPTCHA_API_KEY")

CRAWLER_GCS_BUCKET_NAME = os.getenv("bucket_name")
GOOGLE_CREDENTIALS_FILE = os.path.join(PROJECT_ROOT, "credentials.json")
