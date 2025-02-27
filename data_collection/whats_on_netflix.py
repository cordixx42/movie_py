'''
Data Focused Python - Class Project

Script which scrapes movie info from whats-on-netflix.com/library/movies
minor issue is that the films don't have genre tags and this takes forever. 

'''
from bs4 import BeautifulSoup as bs4
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import date

# takes url 
# return dataframe
def wonScrape(url):
    # use chrome to get webpage
    driver = webdriver.Chrome()
    driver.get(url)

    # lists of movie values initialization
    title_lst = []
    languages_lst = []
    release_lst = []
    rating_lst = []
    imdb_lst = []

    while True:
        # wait for table element to load
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#netflixlist tbody tr td img')))
        # data sometimes takes a extra bit of time to load 
        time.sleep(5)
        # get page and find the table tbody
        soup = bs4(driver.page_source, 'html.parser')
        tbody = soup.find('tbody')

        # loop through the table of one page - could probably make this another function if we wanted to. 
        for row in tbody.find_all('tr'):  # tr elements specify table rows. They alternate between 'even' and 'odd'
            columns = row.find_all('td') # td elements mark table data
            if len(columns)>=7: # table is a size of 7 columns
                title = columns[2].text.strip()
                language = columns[3].text.strip()
                release_year = columns[4].text.strip()
                rating = columns[5].text.strip()
                imdb_score = columns[6].text.strip()
                # add values to list
                title_lst.append(title)
                languages_lst.append(language)
                release_lst.append(release_year)
                rating_lst.append(rating)
                imdb_lst.append(imdb_score)
        try:
            # try to find the button on the bottom right of the table to go to the next page - 25 rows per page >4000 total rows
            next_page = driver.find_element(By.ID, 'netflixlist_next')
            if 'disabled' not in next_page.get_attribute('class'):
                next_page.click()
                # Need extra wait otherwise does not get past page 45
                WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#netflixlist tbody tr td img')))
            else:
                # no more pages 
                break
        except ValueError as e:
            print('Error, either no more pages or webpage elements changed: ', e)
        # extra few seconds for loading - may have needed due to bad connection. 
        time.sleep(5)
    # out of loop - done with scrape, close driver    
    driver.quit()
    movies_df = pd.DataFrame({'Title': title_lst, 'Language': languages_lst, 'Release':release_lst, 'Rating':rating_lst, 'IMDB':imdb_lst})
    return movies_df

def main():
    url = 'https://www.whats-on-netflix.com/library/movies'
    df = wonScrape(url)
    today = date.today()
    date = today.strftime('%Y%m%d')
    df.to_json(f'whatsOnNetflix{date}.json')
    
if __name__ == '__main__':
    main()