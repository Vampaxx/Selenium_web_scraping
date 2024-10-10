import uuid
import time
import random 
import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Extractor:
    def __init__(self, url: str):
        """
        Initialize the WebPageScraper with the given URL and output file path.

        Args:
            url (str)       : The URL of the webpage to scrape.
            save_path (str) : The path to the output file where extracted content will be saved.
        """
        unique_filename = str(uuid.uuid4())
        self.save_path  = f"{unique_filename}.txt"
        self.url        = url
        self.driver     = None
        self.utils      = ExtractionUtils(url=url)

    def fetch_and_parse(self):
        """Validate the URL, fetch the webpage, and parse the content using BeautifulSoup and Selenium."""
        parsed_url = urlparse(self.url)
        if not parsed_url.scheme:
            self.url = f"http://{self.url}"
        try:
            logger.info("Request initialized")
            soup        = self.utils.get_request()
            page_text   = self.utils.clean_and_extract_text(soup=soup)

            if page_text == "No content found." or soup == None:
                try:
                    logger.info("Selenium initializing....")
                    options     = Options()
                    options.set_preference("network.cookie.cookieBehavior", 0)  
                    self.driver = webdriver.Firefox(options=options)
                    
                    self.driver.get(self.url)

                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )

                
                    html_content = self.driver.page_source

                    # Get all script tags separately
                    script_tags = self.driver.find_elements(By.TAG_NAME, 'script')
                    script_content = ""
                    for script in script_tags:
                        script_content += script.get_attribute('outerHTML') + "\n"

                    # Save HTML and Script to file
                    with open(self.save_path, "w", encoding="utf-8") as file:
                        file.write(f"HTML Content:\n{html_content}\n\n")
                        file.write(f"Script Content:\n{script_content}\n")

                    print(f"HTML and script content saved to {self.save_path}")

                except Exception as e:
                    print(f"An error occurred: {e}")

                finally:
                    self.driver.quit()


            else:
                paragraphs = soup.find_all('p')
                if paragraphs:
                    text_content = ' '.join(para.get_text(separator=' ', strip=True) for para in paragraphs)

                    if "accepting cookies" in text_content:
                        try:
                            logger.info("Selenium initializing....")
                            options     = Options()
                            options.set_preference("network.cookie.cookieBehavior", 0)  
                            self.driver = webdriver.Firefox(options=options)
                            
                            self.driver.get(self.url)

                            WebDriverWait(self.driver, 10).until(
                                EC.presence_of_element_located((By.TAG_NAME, "body"))
                            )
                        
                            html_content = self.driver.page_source

                            # Get all script tags separately
                            script_tags = self.driver.find_elements(By.TAG_NAME, 'script')
                            script_content = ""
                            for script in script_tags:
                                script_content += script.get_attribute('outerHTML') + "\n"

                            # Save HTML and Script to file
                            with open(self.save_path, "w", encoding="utf-8") as file:
                                file.write(f"HTML Content:\n{html_content}\n\n")
                                file.write(f"Script Content:\n{script_content}\n")

                            print(f"HTML and script content saved to {self.save_path}")

                        except Exception as e:
                            print(f"An error occurred: {e}")

                        finally:
                            self.driver.quit()








                    else:
                        logger.info("Saving........")
                        cleaned_text = self.utils.clean_and_extract_text(soup)
                        self.utils.save_text_to_file(text=cleaned_text)
                        logger.info(f"Text saved to {self.save_path}")

        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")


class ExtractionUtils:

    def __init__(self, url):
        self.url = url
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
            "DNT": "1",
            "Connection": "close",
            "Upgrade-Insecure-Requests": "1"
        }
        unique_filename = str(uuid.uuid4())
        self.save_path  = f"{unique_filename}.txt"
        

    def get_request(self) -> BeautifulSoup or None:
        """
        Send a GET request to the specified URL and return the parsed HTML content using BeautifulSoup.

        Returns:
            BeautifulSoup : The parsed HTML content of the page, or
            None          : If the request fails or times out.
        """
        logger.info("Requesting....")
        try:
            sessions = requests.Session() 
            time.sleep(random.uniform(2, 5))
            #response = requests.get(self.url, headers=self.headers, timeout=15)
            response = sessions.get(self.url,headers=self.headers,timeout=15) 
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            logger.info("Request completed successfully.")
            return soup

        except requests.exceptions.Timeout:
            logger.error("Request timed out after 15 seconds.")
            return None

        except requests.exceptions.RequestException as e:
            # Catch any other request exceptions (network errors, invalid responses, etc.)
            logger.error(f"An error occurred during the request: {e}")
            return None

    def clean_and_extract_text(self, soup: BeautifulSoup) -> str or None:
        """Remove unwanted tags and extract text from paragraph (<p>) tags.

        Returns:
            str: The cleaned text extracted from the webpage.
        """
        if soup:
            for unwanted in soup(["script", "style", "a"]):
                unwanted.extract()
            paragraphs = soup.find_all('p')
            if paragraphs:
                text_content = ' '.join(para.get_text(separator=' ', strip=True) for para in paragraphs)
                logger.info("Text successfully extracted from paragraph tags.")
                return text_content
            else:
                logger.warning("No paragraph tags found in the response.")
                return "No content found."
        logger.warning("No soup object available for text extraction.")
        return None

    def save_text_to_file(self, text: str) -> None:
        """Save the extracted text to a specified output file.

        Args:
            text (str): The text content to save.
        """
        with open(self.save_path, 'w', encoding='utf-8') as file:
            file.write(text)
            logger.info(f"Extracted text saved to {self.save_path}")


if __name__ == "__main__":

    #URL  = "https://www.myntra.com/bodysuit/h%26m/-hm-infants-boys-pack-of-6-ribbed-cotton-bodysuit/30244605/buy"
    #URL = "https://www.amazon.in/Samsung-Galaxy-Snapdragon-Phantom-Storage/dp/B0BTYX74HZ/ref=pd_ci_mcx_mh_mcx_views_0?pd_rd_w=hfy8A&content-id=amzn1.sym.fa0aca50-60f7-47ca-a90e-c40e2f4b46a9%3Aamzn1.symc.ca948091-a64d-450e-86d7-c161ca33337b&pf_rd_p=fa0aca50-60f7-47ca-a90e-c40e2f4b46a9&pf_rd_r=MHZ5Y02EQCB7YRH7TN1Q&pd_rd_wg=ZBuwO&pd_rd_r=d48e3b16-3e62-408a-b42a-17490e99d283&pd_rd_i=B0BTYX74HZ"
    #URL = "https://www.flipkart.com/henzila-solid-men-black-light-green-track-pants/p/itm7bb2014418642?pid=TKPGZMR2KEHK5J8D&lid=LSTTKPGZMR2KEHK5J8D9BMFN3&marketplace=FLIPKART&store=clo&srno=b_1_1&otracker=browse&fm=organic&iid=en_mu7ClL5wFn7dZn6s3WaREDjfDO-rFUjPi0V-xAhgkb9TIKP_JqxzYhIu1lTZjXxyBQBHEo_livcNoXBo6JZaNg%3D%3D&ppt=hp&ppn=homepage&ssid=p254geucel8lyww01728531823030"
    #URL = "https://www.facebook.com/AmazonIN/?_rdr"
    #URL = "https://vstat.info/Amazon.com"
    #URL = "https://www.amazon.com/"
    #URL = "https://www.swiggy.com/city/kannur/hotel-karthika-mk-road-thavakkara-rest477085"
    URL = "https://www.swiggy.com/"
    extractor = Extractor(url=URL)
    extractor.fetch_and_parse()
