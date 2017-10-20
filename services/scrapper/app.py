from flask import Flask, jsonify, url_for, request, Response
from library.scrapper import parse_from, extract_from
import logging
import json

logging.basicConfig()
logger = logging.getLogger(__name__)

app = Flask(__name__)
SERVICE_NAME = 'scrapper'

SEARCH_RESULT_XPATH = '//div[contains(@class,"search-results-content")]//div[contains(@class,"single-item")]'
ITEMS_TO_SCRAP = {
    'name': './/*[contains(@class,"itemTitle")]/text()',
    'price': './/*[contains(@class,"itemPrice")]/text()',
}


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


@app.route('/search')
def search():
    q = request.args.get('q', default='misc', type=str)
    page = request.args.get('page', default=1, type=int)
    url = 'https://egypt.souq.com/eg-en/{}/s/?page={}'.format(q, page)

    def __do_clean(element):
        result = extract_from(element, ITEMS_TO_SCRAP)
        for key, value in result.items():
            result[key] = clean_data(key, value)
        return result

    def clean():
        elements = parse_from(url, SEARCH_RESULT_XPATH).__iter__()
        prev_element = next(elements)
        yield '['
        for element in elements:
            yield json.dumps(__do_clean(prev_element)) + ','
            prev_element = element
        yield json.dumps(__do_clean(prev_element)) + ']'

    return Response(clean(), content_type='application/json')


def clean_data(name, value):
    from communications import services
    try:
        res = services.call('cleansing/clean_{}'.format(name))({'value': value})
        if res.status_code == 200:
            return res.content.decode("utf-8")
        else:
            raise
    except Exception as e:
        logger.error('Cannot clean data : {}'.format(str(e)))
        return value


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
