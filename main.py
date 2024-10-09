from beautiful_extraction import WebPageScraper
from selenium_extraction import SeleniumExtractor
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataExtraction:
    def __init__(self,URL):
        self.url        = URL 
        self.scraper    = WebPageScraper(url=URL)
        self.extractor  = SeleniumExtractor(url=URL)
    def main(self):
        try:
            self.scraper.fetch_and_parse()
            extracted_text = self.scraper.clean_and_extract_text()

            if extracted_text and extracted_text != "No content found.":
                self.scraper.save_text_to_file(extracted_text)
                logger.error("soup extraction handled the page and extracted the content")
            else:
                self.extractor.fetch_and_extract_text()
                logger.error("Selenium extraction handled the page and extracted the content")

        except Exception as e:
            logger.error(f"Error during scraping: {e}")


if __name__ == "__main__":
    #URL         = "https://www.amazon.in/hz/mobile/mission?p=Awvb5PYPCdXItKNk4syR9w%2F8ZaEI%2FEWhSLq8neDBm2ZDN%2FiUpGTmmeLEaXhYjTydaUP1RHT%2BGq3wDqgl1VsLnYaGIm60jpyMp%2FENkU67HV9BrEL%2FMuJsyHoJAVbyza4fZgpw53GCiKuku%2Fy6GnDuUrki5PD6ijLBckEJuQwlkV8YnUajF8b2lBzL6SGo3urB4TT0o%2FR62IB%2BV2LZ0IeGB44TjQMhlNRmqGLs%2F2BBqbtKgkq5wujUsFBrDZ0FiTFqh%2Bby52Ea62F3hAMzSd%2BOTPSnmrUyiMI74568Ei%2Bew%2Bss36R%2FWtp6EjUVrIQjRTr7ofP3t9V4LiQBhk%2FtgSCTT7q71PLF%2F2t8%2FvM%2Fbi%2B%2FQp3Iaq7f5dfeJuXVim8CRIFFRTbNoNTKrlb1XZ%2FWlRnIDe5gYKbo0TfEJ1B%2F57iLhT8%3D&" 
    URL = "https://www.myntra.com/bodysuit/h%26m/-hm-infants-boys-pack-of-6-ribbed-cotton-bodysuit/30244605/buy"
    DataExtraction(URL=URL).main()