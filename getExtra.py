import requests as r
from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
import pandas as pd
def extract_full_body_html(url):
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

        body = page.inner_html("body")
        return body


if __name__ == '__main__':

    maxRecord = 650
    numberOfPages = maxRecord // 30
    start = 0
    tripUrl = "https://www.tripadvisor.com.my"
    melakaData = []
    for i in range(numberOfPages + 1):
        url = f"https://www.tripadvisor.com.my/Restaurants-g298298-oa{start}-Ipoh_Kinta_District_Perak.html#EATERY_LIST_CONTENTS"

        html = extract_full_body_html(url)
        tree = HTMLParser(html)
        infoContainers = tree.css("div.roxNU")  # List of all containers with details
        for div in infoContainers:

            attrs = {
                "Restaurant Name": "-",
                "Rating": "-",
                "Total Rating": "-",
                "Short Cuisine": "-",
                "Price": "-",
                "Link": "-",
                "Review Link": "-",
            }
            name = div.css_first("div > div > span > a").text()

            if len(div.css("a.UqnPZ")) > 0:
                rating = '-'
                totalRating = '-'
            else:
                rating = div.css_first("svg.UctUV").attrs["aria-label"]
                totalRating = div.css_first("span.IiChw").text()

            cuisinePrice = div.css("div.mIBqD span.SUszq")

            if len(cuisinePrice) == 1:
                if "$" in cuisinePrice[0].text():
                    priceSymbol = cuisinePrice[0].text()
                    shortCuisine = "-"
                else:
                    shortCuisine = cuisinePrice[0].text()
                    shortCuisine = shortCuisine.split(", ")
                    priceSymbol = "-"
            elif len(cuisinePrice) == 2:
                shortCuisine = cuisinePrice[0].text()
                shortCuisine = shortCuisine.split(", ")
                priceSymbol = cuisinePrice[1].text()
            else:
                priceSymbol = "-"
                shortCuisine = "-"

            link = tripUrl + div.css_first("div > div > span > a").attrs["href"]
            reviewLink = link + "#REVIEWS"
            attrs["Restaurant Name"] = name
            attrs["Rating"] = rating
            attrs["Total Rating"] = totalRating
            attrs["Short Cuisine"] = shortCuisine
            attrs["Price"] = priceSymbol
            attrs["Link"] = link
            attrs["Review Link"] = reviewLink
            print(attrs)
            melakaData.append(attrs)
        start += 30

    df = pd.DataFrame(melakaData)
    # df.drop_duplicates(ignore_index=True, inplace=True)
    df.drop_duplicates(subset=['Link'], ignore_index=True, inplace=True)
    df.to_excel("Extra\IpohData.xlsx", index=False)
