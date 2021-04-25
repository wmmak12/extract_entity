import sys
sys.path.append('./src')
import extract_entity_api


def test_scrape_entity_html(url_w_html):
    entities_details = extract_entity_api.scrape_entity(url_w_html, './test/data/gic.db')
    assert type(entities_details) == list


def test_scrape_entity_csv():
    url = 'https://data.cityofnewyork.us/api/views/7yq2-hq9c/rows.csv'
    entities_details = extract_entity_api.scrape_entity(url, './test/data/gic.db')
    assert type(entities_details) == list


def test_scrape_entity_none(url_w_no_entity):
    entities_details = extract_entity_api.scrape_entity(url_w_no_entity, './test/data/gic.db')
    assert type(entities_details) == str

