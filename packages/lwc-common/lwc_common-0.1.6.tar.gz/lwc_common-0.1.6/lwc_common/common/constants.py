import os

# ====================================================
#                      PATHS
# ====================================================
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PROFILE_DOWNLOAD_DIR = os.path.join(PROJECT_ROOT, "profiles")
MASTER_LIST = os.path.join(PROJECT_ROOT, "master.json")

# create necessary directories and files
os.makedirs(PROFILE_DOWNLOAD_DIR, exist_ok=True)
open(MASTER_LIST, "a").close()

# ====================================================
#                       SECRETS
# ====================================================
CRAWLER_GCS_BUCKET_NAME = os.getenv("bucket_name")
GOOGLE_CREDENTIALS_FILE = os.path.join(PROJECT_ROOT, "credentials.json")
