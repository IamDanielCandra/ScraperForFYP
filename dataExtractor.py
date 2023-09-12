# Script made by Daniel Candra TP060288
# Usage: to get remaining data from link
import requests as r
from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
import time
import pandas as pd


def extract_full_tree(url):

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url)
            page.wait_for_load_state("domcontentloaded")
        except TimeoutError:
            page.close()
            page = browser.new_page()
            page.goto(url)
            page.wait_for_load_state("domcontentloaded")

        html = page.inner_html("body")
        tree = HTMLParser(html)

        # Check if there is "View all details" kind of buttons
        overlay1Exist = tree.css("a.OTyAN")
        overlay2Exist = tree.css("a.yhUxi")
        if len(overlay1Exist) > 0:  # if overlay type 1 exist, update the html
            page.wait_for_selector('a.OTyAN')
            time.sleep(1)
            page.click('a.OTyAN')
            tree = HTMLParser(page.inner_html("body"))

        elif len(overlay2Exist) > 0:  # if overlay type 2 exist, update the html
            page.wait_for_selector('a.yhUxi')
            time.sleep(1)
            page.click('a.yhUxi')
            tree = HTMLParser(page.inner_html("body"))

        page.close()
        browser.close()
        return tree


def get_the_thing(url):
    attrs = {
        'Price Range': '-',
        'Cuisines': '-',
        'Special Diets': '-',
        'Meals': '-',
        'Features': '-'
    }
    list_of_keywords = ['Price Range', 'Cuisines', 'Special Diets', 'Meals', 'Features']
    # html = extract_full_body_html(url)
    tree = extract_full_tree(url)
    elements = tree.css("div[class]")
    for i in range(len(elements)):
        if elements[i].text().lower().title() in list_of_keywords:
            if len(elements[i + 1].text().split(", ")) > 1:
                attrs[elements[i].text().lower().title()] = elements[i+1].text().split(", ")
            else:
                attrs[elements[i].text().lower().title()] = elements[i + 1].text()
    return attrs


if __name__ == '__main__':
    # Remove duplicates
    Extra = pd.read_excel('Extra\ExtraData.xlsx')
    # print(len(PJData))
    # PJData.drop_duplicates(ignore_index=True, inplace=True)
    # PJData.drop_duplicates(subset=['Link'], ignore_index=True, inplace=True)
    # PJData.to_excel("PJData.xlsx", index=False)
    # print(len(PJData))

    extractedData = []
    current = 2000
    total = len(Extra)
    stop = total
    while current < total:
        data = get_the_thing(Extra.loc[current, 'Link'])
        print(data)
        extractedData.append(data)
        print(len(extractedData))
        current += 1

    df = pd.DataFrame(extractedData)
    df.to_excel("Extra\ExtraDetail3.xlsx", index=False)
