from flask import Flask, jsonify, url_for
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
    return jsonify({'scrapper': dict(links)})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
