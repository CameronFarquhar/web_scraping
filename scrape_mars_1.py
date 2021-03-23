from bs4 import BeautifulSoup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pymongo
import pandas as pd

def scrape_mars_data():
    #grab first news article on mars.nasa webpage
    
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url_news = "https://mars.nasa.gov/news"
    browser.visit(url_news)

    title = browser.find_by_css('div.content_title a').text

    paragraph = browser.find_by_css('div.article_teaser_body').text

    # grab mars surface image using splinter
    #acces the webpage and click on the FULL IMAGE

    url_surf_img = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url_surf_img)
    browser.links.find_by_partial_text('FULL IMAGE').click()

    # parse the FULL IMAGE page and grab the url

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    mars_source_image = soup.find('img', class_='fancybox-image')["src"]

    featured_image_url = f"https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{mars_source_image}"

    # visit mars facts and grab the table contents and load them into html format

    mars_facts_url = "https://space-facts.com/mars/"
    tables = pd.read_html(mars_facts_url)
    table_df = tables[0]
    panda_table = pd.DataFrame(table_df)
    panda_table.to_html('mars_facts_table.html')

    # visit astrology site and grab title and img link to each mars hemisphere
    
    astrogeology_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(astrogeology_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemisphere_image_urls = []

    xpath = '//div//a[@class="itemLink product-item"]/img'

    for x in range (4):
        # grab titles
        titles = browser.find_by_xpath('//h3')[x]
        title = titles.text

        # click respective image url
        results = browser.find_by_xpath(xpath)
        img = results[x]
        img.click()
        browser.links.find_by_partial_text('Open').click()

        # parse the page
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        # grab image url
        hemisphere_image = soup.find('img', class_='wide-image')["src"]
        hemisphere_image_list = f"https://astrogeology.usgs.gov/{hemisphere_image}"

        # append title and image url to dictionary
        title_image_dict = {"title": title, "img_url":hemisphere_image_list}
        hemisphere_image_urls.append(title_image_dict)

        browser.back()

    browser.quit()

    mars_data = {
    "title": title,
    "paragraph": paragraph,
    "featured_image_url": featured_image_url,
    "hemisphere_image_urls": hemisphere_image_urls
    }

    return mars_data