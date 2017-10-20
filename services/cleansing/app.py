from flask import Flask, jsonify, url_for, request
import json

app = Flask(__name__)


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
    return jsonify({'cleansing': dict(links)})


@app.route('/clean/price')
def clean_price():
    price = request.args.get('price', default='0', type=str)
    rtn = ''.join([d for d in price if d.isdigit() or d in ['.']])
    return rtn


if __name__ == '__main__':
    app.run()
