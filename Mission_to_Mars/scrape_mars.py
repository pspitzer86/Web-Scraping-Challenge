# Import Dependencies

from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

# Defined function setting up Splinter

def init_browser():
    executable_path = {'executable_path' : ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

# Function to visit the url for each website, parse the htmls made of each site and setting variables for the tag and class needed for each scrape
# All but the hemisphere website uses find_all() method, setting an if statement to look for which between find_all() and find() to use.

def clam_chowder(browser, url, tag, class_name, find_all):
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    if find_all:
        return soup.find_all(tag, {'class' : class_name})
    else: 
        return soup.find(tag, {'class' : class_name})


# Defined scrape function using clam_chowder function to scrape all needed features and create a dictionary from them.  Altered jupyter notebook.
    
def scrape():

    browser = init_browser()

    mars_d = {}

    news_url="https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&year=2021%3Apublish_date&category=19%2C165%2C184%2C204&blank_scope=Latest"
    
    latest_news = clam_chowder(browser, news_url, 'div', 'content_title', True)
    mars_d['news_title'] = latest_news[1].text


    latest_teaser = clam_chowder(browser, news_url, 'div', 'article_teaser_body', True)
    mars_d['news_p'] = latest_teaser[0].text



    image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'

    image_soup = clam_chowder(browser, image_url, 'a', 'showimg', True)

    picture = image_soup[0]['href']

    mars_d['featured_image_url'] = image_url.replace('index.html', picture)



    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


    hemi_soup = clam_chowder(browser, hemi_url, 'div', 'description', True)

    hemi_titles = []

    for item in hemi_soup:
        wrong_name = item.text.split('/')
        title = wrong_name[0].replace(' Enhancedimage', '')
        hemi_titles.append(title)


    base_url  = 'https://astrogeology.usgs.gov'
    hemi_images = []

    hemi_url_list = ['https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced',
                    'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced',
                    'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced',
                    'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced']

    for url in hemi_url_list:

        hemi_soup = clam_chowder(browser, url, 'img', 'wide-image', False)
        hemi_images.append(base_url + hemi_soup['src'])


    hemisphere_image_urls = []

    for url in range(0, len(hemi_titles)):
        hemisphere_image_urls.append({'title':hemi_titles[url], 'img_url':hemi_images[url]})

    mars_d['hemisphere_image_urls'] = hemisphere_image_urls



    fact_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(fact_url)
    fact_df = tables[0]


    mars_fact_df = fact_df.rename(columns = {0 : 'Aspect', 1 : 'Measurement'})

    mars_table_str = mars_fact_df.to_html(index=False)
    mars_table_string = mars_table_str.replace('text-align: right;', 'text-align: left;')

    mars_d['mars_fact_table'] = mars_table_string

    return mars_d