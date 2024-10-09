import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



class Extractor:
    def __init__(self, url: str, save_path: str = "output_context.txt"):
        """
        Initialize the WebPageScraper with the given URL, headers, and output file path.

        Args:
            url (str)       : The URL of the webpage to scrape.
            headers (dict)  : The headers to include in the HTTP request.
            save_path (str) : The path to the output file where extracted text will be saved.
        """
        self.url        = url
        self.soup       = None
        self.headers    = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
            "DNT": "1",
            "Connection": "close",
            "Upgrade-Insecure-Requests": "1"
        }
        self.save_path  = save_path
        self.driver     = webdriver.Firefox()

    def fetch_and_parse(self):
        """Validate the URL, fetch the webpage, and parse the content using BeautifulSoup."""
    
        parsed_url = urlparse(self.url)
        if not parsed_url.scheme:
            self.url = f"http://{self.url}"

        try:
            logger.info("Request initialized")
            utils   = ExtractionUtils(url=self.url)

            soup    = utils.get_request()
            if soup == None:
                try:
                    self.driver.get(self.url)

                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )

                    body = self.driver.find_element(By.TAG_NAME, "body")
                    text_content = body.text

                    with open(self.save_path, "w", encoding="utf-8") as file:
                        file.write(text_content)

                    print(f"Text content saved to {self.save_path}")

                except Exception as e:
                    print(f"An error occurred: {e}")

                finally:
                    self.driver.quit()
            else:
                logger.info("Request cleaning initialized")

                text_file = utils.clean_and_extract_text(soup=soup)
                utils.save_text_to_file(text=text_file)
                logger.info(f"saved the text at {self.save_path}")

                logger.info(f"Successfully fetched and parsed: {self.url}")

        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            logger.info(f"Initialized Selenium fetching")
            try:
                self.driver.get(self.url)

                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )

                body = self.driver.find_element(By.TAG_NAME, "body")
                text_content = body.text

                with open(self.save_path, "w", encoding="utf-8") as file:
                    file.write(text_content)

                print(f"Text content saved to {self.save_path}")

            except Exception as e:
                print(f"An error occurred: {e}")

            finally:
                self.driver.quit()









class ExtractionUtils:

    def __init__(self,url,save_path: str = "output_context.txt"):
        self.url        = url
        self.headers    = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
            "DNT": "1",
            "Connection": "close",
            "Upgrade-Insecure-Requests": "1"
        }
        self.save_path  = save_path


    
    def get_request(self) -> BeautifulSoup or None:
        """
        Send a GET request to the specified URL and return the parsed HTML content using BeautifulSoup.

        Returns:
            BeautifulSoup : The parsed HTML content of the page, or
            None          : If the request fails or times out.
        """
        logger.info("Requesting....")
        try:
            response = requests.get(self.url, headers=self.headers, timeout=15)
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

    
    def clean_and_extract_text(self,soup: BeautifulSoup) -> str or None:
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
    URL  = "https://www.myntra.com/bodysuit/h%26m/-hm-infants-boys-pack-of-6-ribbed-cotton-bodysuit/30244605/buy"
    #URL = "https://www.amazon.in/Samsung-Galaxy-Snapdragon-Phantom-Storage/dp/B0BTYX74HZ/ref=pd_ci_mcx_mh_mcx_views_0?pd_rd_w=hfy8A&content-id=amzn1.sym.fa0aca50-60f7-47ca-a90e-c40e2f4b46a9%3Aamzn1.symc.ca948091-a64d-450e-86d7-c161ca33337b&pf_rd_p=fa0aca50-60f7-47ca-a90e-c40e2f4b46a9&pf_rd_r=MHZ5Y02EQCB7YRH7TN1Q&pd_rd_wg=ZBuwO&pd_rd_r=d48e3b16-3e62-408a-b42a-17490e99d283&pd_rd_i=B0BTYX74HZ"
    extractor = Extractor(url=URL)
    extractor.fetch_and_parse()