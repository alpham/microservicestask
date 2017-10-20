from lxml import etree
import requests

__all__ = ['parse_from']


def _get_page(url):
    res = requests.get(url)
    return res.content


def parse_from(url, xpath):
    htmlparser = etree.HTMLParser()
    html = _get_page(url)
    tree = etree.fromstring(html, htmlparser)
    return tree.xpath(xpath)


def extract_from(element, items):
    obj = {}
    for key, xpath in items.items():
        obj[key] = element.xpath(xpath)[0]
    return obj
