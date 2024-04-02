import filecmp

import pytest
from playwright.sync_api import sync_playwright

from lib import open_page, save_to_jsonfile, open_pages


@pytest.fixture
def page():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        yield page
        context.close()
        browser.close()


def test_example_page(page):
    url = 'https://about.readthedocs.com/'
    page.route_from_har("./testhar/rtd.har", update=False)
    html, page_resources, screenshot = open_page(page, url, 'test_scr2.png')
    save_to_jsonfile('testpage2.json', html, page_resources, screenshot)
    assert filecmp.cmp('test_scr.png', 'test_scr2.png', shallow=False)
    assert filecmp.cmp('testpage.json', 'testpage2.json', shallow=False)


def test_example_input_does_not_raise():
    open_pages('dockertest/urls.input', 'dockertest')
