from bs4 import BeautifulSoup
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

executable_path = {'executable_path' : ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

news_url="https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&year=2021%3Apublish_date&category=19%2C165%2C184%2C204&blank_scope=Latest"
browser.visit(news_url)

html = browser.html
soup = BeautifulSoup(html, 'html.parser')

latest_news = soup.find_all('div', {'class' : 'content_title'})
news_title = latest_news[1].text
print(news_title)

latest_teaser = soup.find_all('div', {'class' : 'article_teaser_body'})
news_p = latest_teaser[0].text
print(news_p)

image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(image_url)

html = browser.html
soup=BeautifulSoup(html, 'html.parser')


image_soup = soup.find_all('a', class_='showimg')

picture = image_soup[0]['href']

featured_image_url = image_url.replace('index.html', picture)
print(featured_image_url)


fact_url = 'https://space-facts.com/mars/'
tables = pd.read_html(fact_url)
fact_df = tables[0]
fact_df


mars_fact_df = fact_df.rename(columns = {0 : 'Aspect', 1 : 'Measurement'})
mars_fact_df


mars_table_str = mars_fact_df.to_html()
mars_table_str


hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(hemi_url)


html = browser.html
soup = BeautifulSoup(html, 'html.parser')


hemi_soup = soup.find_all('div', {'class' : 'description'})

hemi_titles = []

for item in hemi_soup:
    wrong_name = item.text.split('/')
    title = wrong_name[0].replace(' Enhancedimage', '')
    hemi_titles.append(title)

print(hemi_titles)


base_url  = 'https://astrogeology.usgs.gov'
hemi_images = []

hemi_url_list = ['https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced',
                'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced',
                'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced',
                'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced']

for url in hemi_url_list:
    browser.visit(url)
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    hemi_soup = soup.find('img', {'class' : 'wide-image'})
    
    hemi_images.append(base_url + hemi_soup['src'])
    
print(hemi_images)


hemisphere_image_urls = []

for url in range(0, len(hemi_titles)):
    hemisphere_image_urls.append({'title':hemi_titles[url], 'img_url':hemi_images[url]})

hemisphere_image_urls