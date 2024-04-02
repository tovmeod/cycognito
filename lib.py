import base64
import json
import os
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright


def open_pages(input_path, output_basedir):
    with open(input_path, "r") as f:
        for line in f:
            domain = urlparse(line).netloc
            output_dir = os.path.join(output_basedir, domain)
            os.makedirs(output_dir, exist_ok=True)
            screenshot_path = os.path.join(output_dir, "screenshot.png")
            html, page_resources, screenshot = open_site(line, screenshot_path)
            save_to_jsonfile(os.path.join(output_dir, 'browse.json'), html, page_resources, screenshot)


def open_page(page, url, screenshot_path):
    page_resources = []

    # Intercept requests to capture URLs and status codes
    def log_request(response):
        page_resources.append((response.url, response.status))

    page.on('response', log_request)
    page.goto(url)
    html = page.content()
    page.screenshot(full_page=True, path=screenshot_path)
    screenshot = page.screenshot(full_page=True)  # defaults to png

    return html, page_resources, screenshot


def open_site(url, screenshot_path):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        context = browser.new_context()
        page = context.new_page()
        html, page_resources, screenshot = open_page(page, url, screenshot_path)

        context.close()
        browser.close()

        return html, page_resources, screenshot


def save_to_jsonfile(output_path, html, page_resources, screenshot):
    with open(output_path, "w") as f:
        json.dump({
            'html': html, 'resources': page_resources, 'screenshot': base64.b64encode(screenshot).decode('utf-8')
        }, f, indent=4)
