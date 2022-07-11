from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    news_title, news_paragraph = mars_news(browser)

    data = {
        'news_title': news_title,
        'news_paragraph': news_paragraph,
        'featured_image': featured_image(browser),
        'facts': mars_facts(),
        'last_modified': dt.datetime.now(),
        'hem_imgs': mars_hemi_imgs(browser)
    }

    browser.quit()
    return data

def mars_news(browser):

    # Visit Mars NASA news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one('div.list_text')
        news_title = slide_elem.find('div', class_='content_title').get_text()
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None
    
    return news_title, news_p

def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    except AttributeError:
        return None
    
    # Use base url to create absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

def mars_facts():
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except BaseException:
        return None
    
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    return df.to_html()

def mars_hemi_imgs(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    hemisphere_image_urls = []

    html = browser.html
    hems_soup = soup(html, 'html.parser')
    titles = hems_soup.find_all('div', class_='item')

    img_links = browser.find_by_tag('img.thumb')
    
    for x in range(0, len(img_links)):
        # img_links[x].click()
         browser.find_by_tag('img.thumb')[x].click()

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

    return hemisphere_image_urls


if __name__ == '__main__':
    print(scrape_all())