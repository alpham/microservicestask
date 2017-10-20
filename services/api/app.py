from flask import Flask, url_for, jsonify
import requests
import os
import json
import logging

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


__init()


@app.route('/')
def index():
    links = []
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


if __name__ == '__main__':
    app.run()
