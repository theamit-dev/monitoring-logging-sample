import socket
import uuid
from datetime import datetime

import sentry_sdk
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from logger import logger


class MyHttpTransport(sentry_sdk.transport.HttpTransport):
    def _get_pool_options(self, ca_certs):
        # Ignore SSL Errors
        options = super()._get_pool_options(ca_certs)
        options["cert_reqs"] = "CERT_NONE"
        return options


sentry_sdk.init(
    dsn="https://8fe00044c3d44ff7a8fc81a62b050211@o4505435493498880.ingest.sentry.io/4505436212756480",

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,
    http_proxy='http://127.0.0.1:9000',
    https_proxy='http://127.0.0.1:9000',
    # debug=True,
    transport=MyHttpTransport,

)

app = FastAPI()

log_detail = {
    'server': f'{socket.gethostname()}',
    'app': 'monitoring-logging-sample',
    'component': 'logging demo',
}

ret = {
    "ver": "1.0",
    "t": "sample",
    "data": {},
    "meta": {
        "timestamp": "2023-06-28T09:30:00Z",
        "server": log_detail['server'],
        "reqid": "625fcbaa5118c815ab2b64fb",
        "msg": ""
    }
}


@app.get("/debug/")
async def debug():
    ret['data'] = {'log_type': 'DEBUG'}
    ret['meta']['timestamp'] = datetime.now()
    ret['meta']['reqid'] = f'{uuid.uuid4()}'

    log_detail['reqid'] = ret['meta']['reqid']
    log_detail['subcomponent'] = 'debug'
    logger.debug('Entered login() method. Username: "amita".', extra=log_detail)
    return ret


@app.get("/info/")
async def info():
    ret['data'] = {'log_type': 'INFO'}
    ret['meta']['timestamp'] = datetime.now()
    ret['meta']['reqid'] = f'{uuid.uuid4()}'

    log_detail['reqid'] = ret['meta']['reqid']
    log_detail['subcomponent'] = 'info'

    logger.info('User "amita" successfully logged in.', extra=log_detail)
    return ret


@app.get("/warn/")
async def warn():
    ret['data'] = {'log_type': 'WARN'}
    ret['meta']['timestamp'] = datetime.now()
    ret['meta']['reqid'] = f'{uuid.uuid4()}'

    log_detail['reqid'] = ret['meta']['reqid']
    log_detail['subcomponent'] = 'warn'

    logger.warn('Password expiration date approaching for user "amita". Please update the password.', extra=log_detail)
    return ret


@app.get("/error/")
async def error():
    ret['data'] = {'log_type': 'ERROR'}
    ret['meta']['timestamp'] = datetime.now()
    ret['meta']['reqid'] = f'{uuid.uuid4()}'

    log_detail['reqid'] = ret['meta']['reqid']
    log_detail['subcomponent'] = 'error'

    logger.error('An unexpected error occurred while processing the request', extra=log_detail)
    return ret


@app.get("/crtitical/")
async def crtitical():
    ret['data'] = {'log_type': 'CRTITICAL'}
    ret['meta']['timestamp'] = datetime.now()
    ret['meta']['reqid'] = f'{uuid.uuid4()}'

    log_detail['reqid'] = ret['meta']['reqid']
    log_detail['subcomponent'] = 'crtitical'

    logger.critical('Database connection lost. Application cannot proceed', extra=log_detail)
    return ret


@app.get("/server_error/")
async def server_error():
    division_by_zero = 1 / 0
    return None


app.mount("/", StaticFiles(directory="fe", html=True, check_dir=False), name="fe")
