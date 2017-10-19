from flask import Flask, url_for, jsonify

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({
        'scrapper': url_for('scrapper_handshake', _external=True),
        'cleansing': url_for('cleansing_handshake', _external=True),
    })


@app.route('/scrapper')
def scrapper_handshake():
    return jsonify({
        'scrap': url_for('scrap_page', url="<url>", css_selectors="<css_selectors>", _external=True),
        'status': url_for('scrapper_status', _external=True)
    })


@app.route('/scrapper/status')
def scrapper_status():
    return jsonify(dict(healty=True))


@app.route('/scrap/<url>/<css_selectors>')
def scrap_page(url, css_selectors):
    return jsonify({
        'result': True
    })


@app.route('/cleansing')
def cleansing_handshake():
    return jsonify({
        'valid': True
    })


if __name__ == '__main__':
    app.run()
