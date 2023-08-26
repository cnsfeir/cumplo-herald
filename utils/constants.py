import os

from dotenv import load_dotenv

load_dotenv()


IS_TESTING = bool(os.getenv("IS_TESTING"))
LOG_FORMAT = "\n [%(levelname)s] %(message)s"
PUSH_NOTIFICATIONS_QUEUE = os.getenv("PUSH_NOTIFICATIONS_QUEUE", "push-notifications")
