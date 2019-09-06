# Import dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
from selenium import webdriver
import os
import pandas as pd
import requests
import time

# Using splinter, initialize a browser instance with chrome driver to be used for each scraping task.

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser('chrome', **executable_path, headless=False)

# Create the scrape function to be imported in app.py

def scrape():
    browser = init_browser()
    mars = {}
    
    #NASA MARS NEWS
    # Save url to a variable
    mars_url = "https://mars.nasa.gov/news/"
    
    # Navigate to the url to be scraped.
    browser.visit(mars_url)
    
    # Pause to give browser time to load and read
    time.sleep(10)
    
    # Create bs object and use lxml as an HTML parser
    soup = bs(browser.html, 'html.parser')
    
    # Scrape/pull list of class = content_title with an a tag
    content_titles = soup.select('.content_title >a')
    
    # Retrieve first title 
    article_title = content_titles[0].text

    # Add article_title to mars dictionary.
    mars["title"] = article_title

    # Scrape/pull list of class = article_teaser_body
    article_bodies = soup.select('.article_teaser_body')
    
    # If length of article bodies is more than 0 display the first one. Else display "none".
    if len(article_bodies) > 0:
        article_body = article_bodies [0].text
    else: 
        article_body = "none"
    
    # Add article_body to mars dictionary.    
    mars["article"] = article_body
        
    #JPL MARS SPACE IMAGES
    
    # Save given url to a variable
    mars_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    
    # Navigate to url to be scraped 
    browser.visit(mars_image_url)

    # Verify if the element with class, carousel item is present using style or css and wait the specified time
    browser.is_element_present_by_css('.carousel_item', wait_time=3)
    
    # Create bs object and parse using python's html.parser.
    soup = bs(browser.html, 'html.parser')
    
    # Pause..
    time.sleep(5)

    # Scrape a list of url's under the class carousel_item
    carousel_items = soup.select('.carousel_item')

    # Pull the first element in the class carousel items with style.
    carousel_item2 = carousel_items[0]['style']

    # Parse  by splitting the element and retrieving string in quotes.
    img_url = carousel_item2.split("'")[1]

    # Save base url to a variable
    mars_image_baseurl = 'https://www.jpl.nasa.gov'

    # Add the img_url to the base url to get the full image url
    featured_image_url = mars_image_baseurl + img_url
    mars['featured_image_url'] = featured_image_url
    

    #Mars Weather

    # Save url to a variable
    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
    
    #Navigate to the url to be scraped 
    browser.visit(mars_weather_url)

    # Create bs object; parse using html.parser
    soup = bs(browser.html, 'html.parser')

    # Get first item from class tweet-text.
    tweet = soup.select('.tweet-text')[0].text

    # Append tweet to mars dictionary with key 'mars_weather'
    mars['mars_weather'] = tweet
    

    #MARS Table of Facts

    # Save url to a variable
    space_url = 'https://space-facts.com/mars'

    #Navigate to the url
    browser.visit(space_url)

    # Create bs object and use html.parser from python
    soup = bs(browser.html, 'html.parser')

    # Convert first table found to a dataframe
    tabledf = pd.read_html(space_url)[0]

    # Reconfigure dataframe by renaming columns and --
    tabledf = tabledf.rename(columns = {'Mars - Earth Comparison':'Description','Mars':'Value'})
    
    # Create a new df by dropping the Earth column
    tabledf2 = tabledf[['Description','Value']].copy()

    # Convert new df to html table
    mars_html_table = tabledf2.to_html(index=False)

    # Add to the mars dictionary.
    mars['mars_facts'] = mars_html_table
    
    #MARS Hemispheres

    # Save url to a variable
    mars_hem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    
    # Navigate to the url to be scraped.
    browser.visit(mars_hem_url)

    # Create bs object and parse with lxml as HTML parser
    soup = bs(browser.html, 'lxml')

    # Create an empty list called hem_img_list to hold a dictionary of titles and image links
    hem_img_list = []

    # Scrape page for list of class = description with a tag
    hem_data =  soup.select('.description > a')

    # For each line in hem_data, parse title using h3 tag and extracting the text
    # Remove "Enhanced" from each title.

    # Save base url as a variable and add link. Use each resulting url to find the image url
    # utilizing the class, downloads  with a tag and extracting the href. Add the list to the 
    # mars dictionary 
    for datum in hem_data:
        title = datum.find("h3").text
        title = title.replace("Enhanced", "")
        link = datum.get('href')
        base_url = 'https://astrogeology.usgs.gov'
        med_url = base_url+link
        browser.visit(med_url)
        soup=bs(browser.html, 'lxml')
        downloads = soup.find("div", class_="downloads")
        img_url = downloads.find("a")["href"]
        hem_img_list.append({"title": title, "link":img_url})
        mars['mars_hem'] = list(hem_img_list)     
    
    # Define mars dictionary
    mars = {
        "title": article_title,
        "article": article_body,
        "featured_image_url": featured_image_url,
        "mars_weather": tweet,
        "mars_facts": mars_html_table,
        "mars_hem": list(hem_img_list)
    }
    
    # Quit the browser
    browser.quit()

    # Return the mars dictionary
    return mars