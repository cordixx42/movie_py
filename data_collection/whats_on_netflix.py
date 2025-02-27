import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# takes URL to the WON site. Returns a dataframe of all movies found in the table on the site. 
# this may need to be changed if the site changes. 
# developed and tested on windows with Spyder - Seems that there is may be ad overlays which may get in the way on other systems. 
# each page loads for about 10 seconds so this is quite a long running script. If your internet is faster, this may be able to run with less wait time. 
# as of 02-27-2025 there are 190 pages of tables. Results in 4748 rows of movies. Takes about 30 minutes to run. 

def wonScrape(url):
    # Set up Selenium WebDriver (You must make sure that chromedriver is in your PATH)
    driver = webdriver.Chrome()
    driver.get(url)
   
    # Initialize lists to hold movie data
    title_lst = []
    language_lst = []
    release_year_lst = []
    rating_lst = []
    imdb_score_lst = []
   
    while True:
        # Wait until the table body is populated with data
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#netflixlist tbody tr td img')))
   
        # Give an extra moment for the data to fully load
        time.sleep(5)
   
        # Get the page source and parse it
        soup = BeautifulSoup(driver.page_source, 'html.parser')
   
        # Find the tbody containing the movie list and loop through each row in the tbody and extract metadata
        tbody = soup.find('tbody')

        for row in tbody.find_all('tr'):
            columns = row.find_all('td')
           
            if len(columns) >= 7:
                title = columns[2].text.strip()
                language = columns[3].text.strip()
                release_year = columns[4].text.strip()
                rating = columns[5].text.strip()
                imdb_score = columns[6].text.strip()
               
                title_lst.append(title)
                language_lst.append(language)
                release_year_lst.append(release_year)
                rating_lst.append(rating)
                imdb_score_lst.append(imdb_score)
   
        # Check if there is a next page and access it.
        try:
            next_button = driver.find_element(By.ID, 'netflixlist_next')
            # Wait for any iframe/ad to disappear or be invisible before attempting click
            WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.CSS_SELECTOR, 'iframe')))
            if 'disabled' not in next_button.get_attribute('class'):
                try:
                    # try scrolling away from the ad
                    driver.execute_script("window.scrollBy(0, 300);")
                    next_button.click()
                    # Wait for the next page to load (was a problem for a while. Makes everything take forever.)
                    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#netflixlist tbody tr td img')))
                except:
                    # Try using JavaScript if normal click fails
                    driver.execute_script("arguments[0].click();", next_button)  
                    # Wait for the next page to load (was a problem for a while. Makes everything take forever.)
                    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#netflixlist tbody tr td img')))
            else:
                break  # No more pages
        except Exception as e:
            print('Error, either no more pages or webpage elements changed: ', e)
   
        # Give an extra moment for the next page to load - need to test if this is needed.
        time.sleep(5)
   
    # out of loop - done with scrape, close driver    
    driver.quit()
    movies_df = pd.DataFrame({'Title': title_lst, 'Language': language_lst, 'Release':release_year_lst, 'Rating':rating_lst, 'IMDB':imdb_score_lst})
    return movies_df

def main():
    url = 'https://www.whats-on-netflix.com/library/movies'
    df = wonScrape(url)
    df.to_json('whatsOnNetflix.json')
   
if __name__ == '__main__':
    main()