from logging import DEBUG, ERROR, basicConfig, getLogger

import google.cloud.logging
from cumplo_common.dependencies.authentication import authenticate
from cumplo_common.middlewares import PubSubMiddleware
from fastapi import Depends, FastAPI

from cumplo_herald.routers import common
from cumplo_herald.utils.constants import IS_TESTING, LOG_FORMAT

# NOTE: Mute noisy third-party loggers
for module in ("google", "urllib3", "werkzeug", "twilio"):
    getLogger(module).setLevel(ERROR)

getLogger("cumplo_common").setLevel(DEBUG)

if IS_TESTING:
    basicConfig(level=DEBUG, format=LOG_FORMAT)
else:
    client = google.cloud.logging.Client()
    client.setup_logging(log_level=DEBUG)

app = FastAPI()
app.add_middleware(PubSubMiddleware)

app.include_router(common.router, dependencies=[Depends(authenticate)])
