import requests as r
from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
import time

def extract_full_body_html(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_selector('a.OTyAN')
        found = False
        if page.wait_for_selector('a.OTyAN'):
            print("Found it!")

        time.sleep(1)
        page.click('a.OTyAN')

        return page.inner_html("body")

def extract_full_tree(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_selector('a.OTyAN')
        found = False
        if page.wait_for_selector('a.OTyAN'):
            print("Found it!")

        time.sleep(1)
        page.click('a.OTyAN')

        html = page.inner_html("body")
        return HTMLParser(html)
def get_the_thing(url):
    attrs = {}
    list_of_keywords = ['price range', 'cuisines', 'special diets', 'meals', 'features']
    # html = extract_full_body_html(url)
    tree = extract_full_tree(url)
    elements = tree.css("div[class]")
    for i in range(len(elements)):
        if elements[i].text().lower() in list_of_keywords:
            print(elements[i].text())


if __name__ == '__main__':
    # url = "https://www.tripadvisor.com.my/Restaurants-g298570-oa0-Kuala_Lumpur_Wilayah_Persekutuan.html#EATERY_LIST_CONTENTS"
    # tripUrl = "https://www.tripadvisor.com.my/"
    # html = extract_full_body_html(url)
    # tree = HTMLParser(html)
    # infoContainers = tree.css("div.roxNU")  # List of all containers with details
    # for div in infoContainers:
    #     print(type(div))
    #     attrs = {
    #         "Restaurant Name": "-",
    #         "Rating": "-",
    #         "Total Rating": "-",
    #         "Short Cuisine": "-",
    #         "Price": "-",
    #         "Link:": "-"
    #     }
    #     name = div.css_first("div > div > span > a").text()
    #     # d.css_first('img[class*="CapsuleImage"]')
    #     rating = div.css_first("svg.UctUV").attrs["aria-label"]
    #     totalRating = div.css_first("span.IiChw").text()
    #     cuisinePrice = div.css("div.mIBqD span.SUszq")
    #     shortCuisine = cuisinePrice[0].text()
    #     shortCuisine = shortCuisine.split(", ")
    #     if len(cuisinePrice) > 1:
    #         priceSymbol = cuisinePrice[1].text()
    #     else:
    #         priceSymbol = "-"
    #     link = tripUrl + div.css_first("div > div > span > a").attrs["href"]
    #     reviewLink = link + "#REVIEWS"
    #     attrs["Restaurant Name"] = name
    #     attrs["Rating"] = rating
    #     attrs["Total Rating"] = totalRating
    #     attrs["Short Cuisine"] = shortCuisine
    #     attrs["Price"] = priceSymbol
    #     attrs["Link"] = link
    #     print(attrs)

    get_the_thing("https://www.tripadvisor.com.my/Restaurant_Review-g298570-d4355273-Reviews-Ishin_Japanese_Dining-Kuala_Lumpur_Wilayah_Persekutuan.html")