import json
import os
import random
import shutil
import time
from datetime import datetime

from lwc_common.lwc import FirefoxCrawler as Crawler
from lwc_common.wrappers import CloudSQLWrapper, GcsWrapper

# ================================================
#               SETUP CONSTANTS
# ================================================
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROFILE_DOWNLOAD_DIR = os.path.join(PROJECT_ROOT, "profiles")
GOOGLE_CREDENTIALS_FILE = os.path.join(PROJECT_ROOT, "credentials.json")
MASTER_LIST = os.path.join(PROJECT_ROOT, "master.json")

# create necessary directories and files
os.makedirs(PROFILE_DOWNLOAD_DIR, exist_ok=True)
open(MASTER_LIST, "a").close()

LINKEDIN_USERNAME = "anonymousthe105th@gmail.com"
LINKEDIN_PASSWORD = "anonEmus"
LWC_PDF_BUCKET = "data2bots_lwc_storage_bucket"
ANTI_CAPTCHA_API_KEY = "e19825c31e38afca163308eedd482ece"
TEARDOWN_PARTITION = 25

DB_USER = "postgres"
DB_PASSWD = "dummypassword"
DB_NAME = "search_payload_db"
host = "34.90.231.54"
port = 5432


# ================================================
#               INIT OBJECTS
# ================================================
bot = None
gcs_helper = GcsWrapper(GOOGLE_CREDENTIALS_FILE, LWC_PDF_BUCKET)
csql_helper = CloudSQLWrapper(host, port, DB_NAME, DB_USER, DB_PASSWD)


# ================================================
#                   FUNCS
# ================================================
class Logger:
    def __init__(self, name, session_id):
        self.name = name
        self.id = session_id

    def log(self, message):
        text = f"[{datetime.now().strftime('%d/%b/%Y %H:%M:%S')}  {self.name}-{str(self.id)[:5]}]:: {message}"
        print(text)


def setup_crawler(headless=False, login_linkedin=True, logger=None):
    download_dir = PROFILE_DOWNLOAD_DIR
    shutil.rmtree(download_dir, ignore_errors=True)
    os.makedirs(download_dir, exist_ok=True)
    logger = Logger("setup", random.randint(10000, 99999))
    bot = Crawler(
        download_dir=PROFILE_DOWNLOAD_DIR,
        linkedin_email=LINKEDIN_USERNAME,
        linkedin_pwd=LINKEDIN_PASSWORD,
        anti_captcha_api_key=ANTI_CAPTCHA_API_KEY,
        headless=headless,
        logger=logger
    )
    logger.log(f"Starting {bot.name.capitalize()}....")
    logger.log("================")
    if login_linkedin:
        logger.log("Logging in to LinkedIn....")
        bot.login(LINKEDIN_USERNAME, LINKEDIN_PASSWORD)
    logger.log(f"Current page: {bot.current_url}")
    return bot


# =========================================================
#                    EXPOSED FUNCS
# =========================================================

def search(job_title, location="", pages=0):
    logger = Logger("search", random.randint(10000, 99999))
    urls = []
    global bot
    try:
        bot = bot or setup_crawler(login_linkedin=False)
        urls = bot.search(job_title, location, pages)
        logger.log("Teardown started")
    except Exception as exc:
        logger.log(
            f"{exc.__class__.__name__} while getting profiles"
            f" for {job_title} in {location}:: "
            f"{getattr(exc, 'message', str(exc))}"
        )
    finally:
        # cleanup
        bot.teardown = True
        logger.log("Teardown started")
        bot.__exit__(None, None, None)
        bot = None

    logger.log(f"{len(urls)} profile urls found")
    master = json.loads(open(MASTER_LIST).read() or "{}")
    partition = gcs_helper.format_gcs_partition(job_title, location)
    monitor = master.get(partition, {})
    monitor["new"] = list(set(urls)
                          .union(set(monitor.get("new", [])))
                          .union(set(monitor.get("failure", [])))
                          .difference(set(monitor.get("success", []))))
    master[partition] = monitor
    json.dump(master, open(MASTER_LIST, "w"), indent=4)
    return monitor, 200


def scrape_url(url, upload=False, teardown=False, job_title=None, location=None):
    if upload and not (job_title and location):
        msg = "To upload parsed data please supply 'job_title'" \
              " and 'location'", 400
        return msg

    global bot
    gcs_partition = gcs_helper.format_gcs_partition(job_title, location)
    logger = Logger("scrape", url[url.find("/in/") + 4:][:10])
    pdf_path = ""
    try:
        bot = bot or setup_crawler()
        bot.teardown = teardown
        profile_name = url.split("/in/")[-1].strip('/').partition("/")[0]
        logger.log(f"Getting {profile_name}'s profile document....")
        pdf_path = bot.get_profile_pdf(url)
        logger.log(f"Current page: {bot.current_url}")
        sink_filename = f"{profile_name}--profile.pdf"
        os.rename(pdf_path, pdf_path.replace("Profile.pdf", sink_filename))

    except Exception as exc:
        logger.log(
            f"{exc.__class__.__name__} while getting {url}'s pdf:: "
            f"{getattr(exc, 'message', str(exc))}")
    finally:
        # cleanup
        if bot.teardown:
            logger.log("Teardown started")
            bot.__exit__(None, None, None)
            bot = None

        status = 200 if pdf_path else 400
        csql_helper.update_lists(gcs_partition, url, success=(status == 200))
        print()
    return pdf_path, status


def scrape(job_title, location="", upload=True):
    # remove any previous successful url
    master = json.loads(open(MASTER_LIST).read() or "{}")
    partition = gcs_helper.format_gcs_partition(job_title, location)
    monitor = master.get(partition, {})
    new = set(monitor.get("new", []))
    prev_fails = set(monitor.get("failure", []))
    prev_successes = set(monitor.get("success", []))

    urls = (new | prev_fails) - prev_successes
    num_urls = len(urls)
    profiles = []
    times = {}

    # debug param
    custom_break = False

    for idx, url in enumerate(urls, start=1):
        # teardown at the last url
        start = time.perf_counter()
        teardown = (idx == num_urls) or (idx % TEARDOWN_PARTITION == 0)
        print(f">>> processing number {idx} out of {num_urls}")
        profile, status = scrape_url(
            url, upload=upload,  teardown=teardown, job_title=job_title,
            location=location
        )
        if profile:
            profiles.append(profile)
        times[url] = {"idx": idx, "time": time.perf_counter() - start}
        if custom_break:
            break
    return times, 200


if __name__ == "__main__":
    # jt, loc = "data scientist", "netherlands"
    # # all_urls, _ = search(jt, loc)
    # rv, _ = scrape(jt, loc, upload=True)
    # print(f"{rv}")
    #
    # period = [rv[x]["time"] for x in rv]
    # avg = round(sum(period) / len(period), 2)
    # max_, min_ = round(max(period), 2), round(min(period), 2)
    #
    # print(f"Average time per profile is {avg}")
    # print(f"Max time per profile is {max_}")
    # print(f"Min time per profile is {min_}")
    # print(f"Total time spent: {round(sum(period), 2)}")
    base = csql_helper.get_declarative_base()
    pass
