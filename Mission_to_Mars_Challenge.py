# import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit Mars NASA news site
url = 'https://redplanetscience.com'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use base url to create absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df.to_html()

browser.quit()

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)

# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
html = browser.html
hems_soup = soup(html, 'html.parser')
img_links = browser.find_by_tag('img.thumb')
titles = hems_soup.find_all('div', class_='item')
for x in range(0, len(img_links)):
#for x in range(0, 1):
    img_links[x].click()
    jpg_html = browser.html
    jpg_soup = soup(jpg_html, 'html.parser')
    jpg_src = jpg_soup.find('img', class_='wide-image').get('src')
    hemisphere_image_urls.append(
        {
            'img_url': 'https://marshemispheres.com/' + jpg_src,
            'title': titles[x].find('h3').text
        }
    )
    browser.back()

# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# 5. Quit the browser
browser.quit()