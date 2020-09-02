from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd 
import cssutils

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "D:\chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()
    
    mars_data = {}

    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(5)

    html = browser.html
    soup = bs(html, "html.parser")

    #NASA MARS NEWS
    articles = soup.find_all("div", class_='list_text')

    news_date = articles[0].find('div', class_='list_date').text #RETURN
    news_title = articles[0].find("div", class_="content_title").text #RETURN
    news_p = articles[0].find('div', class_='article_teaser_body').text #RETURN


    #JPL MARS SPACE IMAGES - FEATURED IMAGES
    img_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(img_url)
    time.sleep(5)

    img_html = browser.html
    img_soup = bs(img_html, 'html.parser')

    div_style = img_soup.find('article')['style']
    style = cssutils.parseStyle(div_style)
    url = style['background-image']
    url = url.replace('url(', '').replace(')', '') 

    featured_image_url = ('https://www.jpl.nasa.gov/' + url) #RETURN


    #MARS FACTS
    facts_url = 'https://space-facts.com/mars/' 
    browser.visit(facts_url)
    time.sleep(5)

    facts_table = pd.read_html(facts_url) 

    facts_table[2].columns = ['Description', 'Value']
    facts_table[2].set_index('Description', inplace=True)
    facts_table[2] #RETURN


    #MARS HEMISPHERES
    hemi_img_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemi_img_url)
    time.sleep(5)

    hemi_img_html = browser.html
    hemi_img_soup = bs(hemi_img_html, 'html.parser')

    img_info = hemi_img_soup.find_all('div', class_='description')

    img_title0 = img_info[0].find("h3").get_text()
    img_title1 = img_info[1].find("h3").get_text()
    img_title2 = img_info[2].find("h3").get_text()
    img_title3 = img_info[3].find("h3").get_text()

    img_link0 = "https://astrogeology.usgs.gov/search" + img_info[0].find('a')['href']
    img_link1 = "https://astrogeology.usgs.gov/search" + img_info[1].find('a')['href']
    img_link2 = "https://astrogeology.usgs.gov/search" + img_info[2].find('a')['href']
    img_link3 = "https://astrogeology.usgs.gov/search" + img_info[3].find('a')['href']

    title=[img_title0,img_title1,img_title2,img_title3]
    img_url=[img_link0,img_link1,img_link2,img_link3]

    hemisphere_image_urls = [{"title":img_title0, "img_url":img_link0}, #RETURN
                            {"title":img_title1, "img_url":img_link1},  #RETURN
                            {"title":img_title2, "img_url":img_link2},  #RETURN
                            {"title":img_title3, "img_url":img_link3}]  #RETURN


    #ADD INFORMATION TO DICTIONARY
    mars_data = {
        'news_date': news_date, 
        'news_title': news_title,
        'news_p':news_p,
        'featured_image_url': featured_image_url, 
        'table':facts_table[2],
        'hemisphere_image_urls': hemisphere_image_urls
    }
    
    browser.quit()
    
    return mars_data

if __name__ == '__main__':
    scrape()
