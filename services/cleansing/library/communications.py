import os
import requests
import logging
logging.basicConfig()
logger = logging.getLogger(__name__)

def __handshake__():
    url = '{}://{}/'.format(__scheme, __api_url)
    logger.critical('vvvvvvvvvvvvvvv')
    logging.critical(url)
    res = requests.get(url)
    logger.critical('xxxxxx')
    return res.json()


__api_url = os.environ.get('SERVICES_API', 'service_api')
__scheme = os.environ.get('API_SCHEME', 'http')
__api_map = {}


def __update():
    global __api_map
    logger.critical('yyyyyyyyyyy')
    __api_map = __handshake__()

logger.critical('wwwwwwwwww')
__update()
logger.critical(';khjsgasdhl')

def services():
    return __api_map['services']


def api():
    return __api_map['api']


def _call_services(path, delimiter='/'):
    service_name, function_name = path.split(delimiter)
    url = services().get(service_name).get(function_name).get('url')
    if url:
        def __call_with_params(params={}):
            return requests.get(url, params=params)

        return __call_with_params
    else:
        return lambda params: 'Error'


def _call_api(path, delimiter='/'):
    service_name, function_name = path.split(delimiter)
    url = api().get(service_name).get(function_name).get('url')
    if url:
        def __call_with_params(params={}):
            return requests.get(url, params=params)

        return __call_with_params
    else:
        return lambda params: 'Error'


api.call = _call_api
api.update = __update

services.call = _call_services
services.update = __update
