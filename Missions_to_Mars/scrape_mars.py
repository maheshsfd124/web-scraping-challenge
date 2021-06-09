from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver 
    executable_path = {'executable_path': 'chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

    #### URL of page to be scraped - MARS NEWS ####
    url = "https://redplanetscience.com/"
    browser.visit(url)
    html = browser.html
    time.sleep(1)
    soup = BeautifulSoup(html, 'html.parser')
    
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text

    #### URL of page to be scraped - JPL IMAGES ####
    url = "https://spaceimages-mars.com/"
    browser.visit(url)
    html = browser.html
    time.sleep(1)
    soup = BeautifulSoup(html, 'html.parser')

    full_img = soup.find('img', class_='headerimage fade-in')['src']
    featured_image_url = url + full_img

    url = "https://galaxyfacts-mars.com/"
    tables = pd.read_html(url)
    
    df=tables[0]
    df
    df= df.rename(columns= {0:"Description",1:"Mars",2:"Earth"})
    df=df.set_index('Description')
    df
    
    html_table = df.to_html()
    html_table.replace('\n','')

    url = "https://marshemispheres.com/"
    browser.visit(url)
    html = browser.html
    time.sleep(1)
    # Create BeautifulSoup object and parse
    soup = BeautifulSoup(html, 'html.parser')

    # Obtain high resolution images for each of Mar's hemispheres
    results = soup.find_all('div', class_='item')
    hemisphere_image_urls = []
    for result in results:
        hemi_dict = {}
        # Use Beautiful Soup's find() method to navigate and retrieve attributes
        title = result.find('h3').text
        link = result.find('a')['href']
        
        hemi_dict['title'] = title
        hemi_url = url + link
        
        try:
            browser.visit(hemi_url)
            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')
            
            images = soup.find_all('div', class_='downloads')
        
            for image in images:
                full_image = image.find('a')['href']
                hemi_dict['img_url'] = url + full_image
                hemisphere_image_urls.append(hemi_dict)
        except:
            print("Scraping Complete")

    print(hemisphere_image_urls)

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_table": html_table,
        "hemisphere_image_urls": hemisphere_image_urls
    }
    print(mars_data)
    browser.quit()

    # Return results
    return mars_data