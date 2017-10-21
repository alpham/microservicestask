from flask import Flask, url_for, jsonify, request
import requests
import os
import json
import logging
from communications import services

logging.basicConfig()
logger = logging.getLogger(__name__)

app = Flask(__name__)


def __init():
    with open('api.json', 'r') as f:
        json_res = json.load(f)
    for service in os.environ.get('ENTRYPOINTS', 'service_scrapper,service_cleansing').split(','):
        try:
            res = requests.get('{}://{}/'.format(os.environ.get('SCHEME', 'http'), service))
            # TODO: handle errors
            json_obj = res.json()
            json_res.update(json_obj)
        except Exception as e:
            logger.critical(' Cannot define `{}`'.format(service))
    with open('api.json', 'w') as f:
        json.dump(json_res, f)


@app.route('/')
def index():
    links = []
    __init()
    for rule in app.url_map.iter_rules():
        if rule.defaults:
            kw = rule.defaults.copy()
            kw.update({'_external': True})
        else:
            kw = {'_external': True}
        options = {}
        for arg in rule.arguments:
            options[arg] = "{{0}}".format(arg)
        options.update(kw)
        if rule.endpoint in ['static']:
            continue
        url = url_for(rule.endpoint, **options)
        links.append((rule.endpoint, {"url": url, 'methods': list(rule.methods)}))
    with open('api.json', 'r') as f:
        return jsonify({
            'api': dict(links),
            'services': json.load(f)
        })


@app.route('/search')
def search():
    q = request.args.get('q', default='misc', type=str)
    page = request.args.get('q', default='1', type=int)
    res = services.call('scrapper/search')({'q': q, 'page': page})
    if res.status_code:
        return jsonify(res.json())
    else:
        return jsonify({})


if __name__ == '__main__':
    app.run()
