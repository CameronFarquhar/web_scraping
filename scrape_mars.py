#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import BeautifulSoup
from bs4 import BeautifulSoup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pymongo
import pandas as pd


# In[ ]:





# In[2]:


url = "https://mars.nasa.gov/news"


# In[3]:


response = requests.get(url)
# Create BeautifulSoup object; parse with 'html.parser'
soup = BeautifulSoup(response.text, 'lxml')


# In[4]:


print(soup.prettify())


# In[5]:


results_t = soup.find('div', class_='content_title')

news_title = results_t.text.strip('\n')

news_title


# In[6]:


results_p = soup.find('div', class_="rollover_description_inner")

news_p = results_p.text.strip('\n')

news_p


# In[7]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[8]:


url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)


# In[9]:


browser.links.find_by_partial_text('FULL IMAGE').click()


# In[10]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')

mars_source_image = soup.find('img', class_='fancybox-image')["src"]

featured_image_url = f"https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{mars_source_image}"
featured_image_url


# In[11]:


mars_facts_url = "https://space-facts.com/mars/"


# In[12]:


tables = pd.read_html(mars_facts_url)
tables


# In[13]:


table_df = tables[0]
table_df


# In[14]:


panda_table = pd.DataFrame(table_df)


# In[15]:


panda_table.to_html('mars_facts_table.html')


# In[39]:


executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[40]:


astrogeology_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(astrogeology_url)


# In[41]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[46]:


hemisphere_image_urls = []

xpath = '//div//a[@class="itemLink product-item"]/img'

for x in range (4):
    
    titles = browser.find_by_xpath('//h3')[x]
    title = titles.text
    
    results = browser.find_by_xpath(xpath)
    img = results[x]
    img.click()
    browser.links.find_by_partial_text('Open').click()
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemisphere_image = soup.find('img', class_='wide-image')["src"]
    hemisphere_image_list = f"https://astrogeology.usgs.gov/{hemisphere_image}"
    
    title_image_dict = {"title": title, "img_url":hemisphere_image_list}
    hemisphere_image_urls.append(title_image_dict)
    
    browser.back()


# In[ ]:




