from flask import Flask, jsonify, url_for, request
import json

app = Flask(__name__)
SERVICE_NAME = 'cleansing'

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
    return jsonify({SERVICE_NAME: dict(links)})


@app.route('/clean/price')
def clean_price():
    value = request.args.get('value', default='0', type=str)
    rtn = ''.join([d for d in value if d.isdigit() or d in ['.']])
    return rtn


@app.route('/clean/name')
def clean_name():
    value = request.args.get('value', default='', type=str)
    rtn = value.strip()
    return rtn


if __name__ == '__main__':
    app.run()
