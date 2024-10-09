import logging
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from utils import *



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebPageScraper:
    def __init__(self, url: str, save_path: str = "output_context.txt"):
        """
        Initialize the WebPageScraper with the given URL, headers, and output file path.

        Args:
            url (str)       : The URL of the webpage to scrape.
            headers (dict)  : The headers to include in the HTTP request.
            save_path (str) : The path to the output file where extracted text will be saved.
        """
        self.URL        = url
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

    def fetch_and_parse(self):
        """Validate the URL, fetch the webpage, and parse the content using BeautifulSoup."""
    
        parsed_url = urlparse(self.URL)
        if not parsed_url.scheme:
            self.URL = f"http://{self.URL}"

        try:
            self.soup = get_request(URL=self.URL,headers=self.headers)
            logger.info(f"Successfully fetched and parsed: {self.URL}")

        except requests.exceptions.MissingSchema:
            logger.error(f"Invalid URL: {self.URL} - Missing schema.")
            raise ValueError(f"Invalid URL: {self.URL} - Please provide a valid URL.")
        
        except requests.exceptions.ConnectionError:
            logger.error(f"Connection error while trying to reach {self.URL}.")
            raise ConnectionError(f"Failed to connect to {self.URL}.")
        
        except requests.exceptions.Timeout:
            logger.error(f"Timeout error while trying to reach {self.URL}.")
            raise TimeoutError(f"Request to {self.URL} timed out.")
        
        except requests.exceptions.HTTPError as err:
            logger.error(f"HTTP error occurred: {err}")
            raise RuntimeError(f"HTTP error occurred: {err}")
        
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            raise RuntimeError(f"An unexpected error occurred: {e}")

    def clean_and_extract_text(self) -> str:
        """Remove unwanted tags and extract text from paragraph (<p>) tags.

        Returns:
            str: The cleaned text extracted from the webpage.
        """
        if self.soup:
            for unwanted in self.soup(["script", "style", "a"]):
                unwanted.extract()
            paragraphs = self.soup.find_all('p')
            if paragraphs:
                text_content = ' '.join(para.get_text(separator=' ', strip=True) for para in paragraphs)
                logger.info("Text successfully extracted from paragraph tags.")
                return text_content
            else:
                logger.warning("No paragraph tags found in the response.")
                return "No content found."
        logger.warning("No soup object available for text extraction.")
        return None

    def save_text_to_file(self, text: str):
        """Save the extracted text to a specified output file.

        Args:
            text (str): The text content to save.
        """
        with open(self.save_path, 'w', encoding='utf-8') as file:
            file.write(text)
            logger.info(f"Extracted text saved to {self.save_path}")




if __name__ == "__main__":
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
        "DNT": "1",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1"
    }
    
    URL     = "https://www.amazon.in/hz/mobile/mission?p=Awvb5PYPCdXItKNk4syR9w%2F8ZaEI%2FEWhSLq8neDBm2ZDN%2FiUpGTmmeLEaXhYjTydaUP1RHT%2BGq3wDqgl1VsLnYaGIm60jpyMp%2FENkU67HV9BrEL%2FMuJsyHoJAVbyza4fZgpw53GCiKuku%2Fy6GnDuUrki5PD6ijLBckEJuQwlkV8YnUajF8b2lBzL6SGo3urB4TT0o%2FR62IB%2BV2LZ0IeGB44TjQMhlNRmqGLs%2F2BBqbtKgkq5wujUsFBrDZ0FiTFqh%2Bby52Ea62F3hAMzSd%2BOTPSnmrUyiMI74568Ei%2Bew%2Bss36R%2FWtp6EjUVrIQjRTr7ofP3t9V4LiQBhk%2FtgSCTT7q71PLF%2F2t8%2FvM%2Fbi%2B%2FQp3Iaq7f5dfeJuXVim8CRIFFRTbNoNTKrlb1XZ%2FWlRnIDe5gYKbo0TfEJ1B%2F57iLhT8%3D&ref_=ci_mcx_mi&pf_rd_r=5NDCMJ3514XZZF96VSK8&pf_rd_p=652a835d-9e23-4efd-9931-74188247a57a&pd_rd_r=744eadd7-6515-444f-bbec-acd0af863342&pd_rd_w=E6X0m&pd_rd_wg=SBqVS"
    scraper = WebPageScraper(url=URL, headers=headers)
    
    try:

        scraper.fetch_and_parse()
        extracted_text  = scraper.clean_and_extract_text()
        if extracted_text and extracted_text != "No content found.":
            scraper.save_text_to_file(extracted_text)  # Only save if the extracted text is valid
        else:
            logger.info("No valid content to save.")
    except Exception as e:
        logger.error(f"Error during scraping: {e}")