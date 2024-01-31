from logging import DEBUG, basicConfig, getLogger

import google.cloud.logging
from cumplo_common.dependencies.authentication import authenticate
from fastapi import Depends, FastAPI

from cumplo_herald.routers import common
from cumplo_herald.utils.constants import IS_TESTING, LOG_FORMAT

basicConfig(level=DEBUG, format=LOG_FORMAT)
logger = getLogger(__name__)

if not IS_TESTING:
    client = google.cloud.logging.Client()
    client.setup_logging(log_level=DEBUG)


app = FastAPI()

app.include_router(common.router, dependencies=[Depends(authenticate)])
