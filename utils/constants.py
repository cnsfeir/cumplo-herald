import os

from dotenv import load_dotenv

load_dotenv()


IS_TESTING = bool(os.getenv("IS_TESTING"))
LOG_FORMAT = "\n [%(levelname)s] %(message)s"
IFTTT_QUEUE = os.getenv("IFTTT_QUEUE", "push-notifications")
