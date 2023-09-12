# Script made by Daniel Candra TP060288
# Usage: to get reviews from link
import playwright.sync_api
import requests as r
from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
from httpx import get
import time
import pandas as pd


def extract_full_tree(url):

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto(url)
        except playwright.sync_api.Error:
            page.close()
            page = browser.new_page()
            page.goto(url)

        html = page.inner_html("body")
        tree = HTMLParser(html)
        page.close()
        browser.close()
        return tree


def get_reviews_data(url):
    attrs = {
        'Total English Review': '-',
        'Review Pages': '-',
        'Review': '-',
    }
    tree = extract_full_tree(url)
    totalEnglishReview = tree.css_first("label[for='filters_detail_language_filterLang_en'] > span.count") #.text()
    if totalEnglishReview:# If there are english reviews
        totalEnglishReview = int(totalEnglishReview.text().strip("(").strip(")").replace(",", ""))
        reviewContainer = tree.css("div.review-container")
        # print(len(reviewContainer))
        review = []
        for container in reviewContainer:  # Loop through review container
            partial = container.css_first("div.is-9 > div.prw_reviews_text_summary_hsx > div.entry > p.partial_entry")
            partial = partial.text().rstrip("More").replace("...", " ")
            review.append(partial)

        reviewYear = []
        reviewDates = tree.css("span.ratingDate")
        for reviewDate in reviewDates: # Loop through dates
            year = int(reviewDate.attributes['title'].split(" ")[-1])
            reviewYear.append(year)

        usedReview = []
        for i in range(len(review)): #Only using review that is five years recent
            if reviewYear[i] > 2018:
                usedReview.append(review[i])

        reviewPages = []
        maxReview = totalEnglishReview
        numberOfPages = maxReview//15
        start = 0
        if maxReview % 15 != 0:
            if numberOfPages == 0:
                pageUrl = url.replace("-Reviews-", f"-Reviews-or{0}-")
                reviewPages.append(pageUrl)
            else:
                for i in range(numberOfPages + 1):
                    pageUrl = url.replace("-Reviews-", f"-Reviews-or{start}-")
                    reviewPages.append(pageUrl)
                    start += 15
        else:
            if numberOfPages == 0:
                pageUrl = url.replace("-Reviews-", f"-Reviews-or{0}-")
                reviewPages.append(pageUrl)
            else:
                for i in range(numberOfPages + 1):
                    if i == numberOfPages:
                        pass
                    else:
                        pageUrl = url.replace("-Reviews-", f"-Reviews-or{start}-")
                        reviewPages.append(pageUrl)
                        start += 15

        attrs['Total English Review'] = totalEnglishReview
        attrs['Review'] = usedReview
        attrs['Review Pages'] = reviewPages
        print(len(review))
    return attrs


if __name__ == '__main__':
    RestaurantData = pd.read_excel('getReview.xlsx')
    extractedData = []
    current = 2500
    total = len(RestaurantData)  # 4984
    stop = 2500

    while current < total:
        if RestaurantData.loc[current, 'Total Rating'] == '-':
            data = {
                'Total English Review': '-',
                'Review Pages': '-',
                'Review': '-',
            }
            print(data)
            extractedData.append(data)
            print(len(extractedData))
        else:
            data = get_reviews_data(RestaurantData.loc[current, 'Review Link'])
            print(data)
            extractedData.append(data)
            print(len(extractedData))
        current += 1

    df = pd.DataFrame(extractedData)
    df.to_excel("urev2.xlsx", index=False)
