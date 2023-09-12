import requests as r
from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
import pandas as pd
def extract_full_body_html(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_load_state("domcontentloaded")

        return page.inner_html("body")

if __name__ == '__main__':
    maxRecord = 5000
    numberOfPages = maxRecord//30
    start = 0
    tripUrl = "https://www.tripadvisor.com.my"
    klData = []
    for i in range(numberOfPages+1):
        url = f"https://www.tripadvisor.com.my/Restaurants-g298570-oa{start}-Kuala_Lumpur_Wilayah_Persekutuan.html#EATERY_LIST_CONTENTS"

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


            # if div.css_first("svg.UctUV"):#.attrs["aria-label"]:
            #     rating = div.css_first("svg.UctUV").attrs["aria-label"]
            #
            # if div.css_first("span.IiChw"):#.text():
            #     totalRating = div.css_first("span.IiChw").text()

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

            # if len(cuisinePrice) > 0:
            #     shortCuisine = cuisinePrice[0].text()
            #     shortCuisine = shortCuisine.split(", ")
            # if len(cuisinePrice) > 1:
            #     priceSymbol = cuisinePrice[1].text()
            # else:
            #     priceSymbol = "-"
            #
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
            klData.append(attrs)
        start += 30

    df = pd.DataFrame(klData)
    df.to_excel("KLData.xlsx", index=False)
