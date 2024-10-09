from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class SeleniumExtractor:
    def __init__(self, url: str, output_file: str = "output_content.txt"):
        """
        Initialize the WebPageTextExtractor with the given URL and output file.

        Args:
            url (str)           : The URL of the webpage to scrape.
            output_file (str)   : The path to the output file where extracted text will be saved.
        """
        self.url            = url
        self.output_file    = output_file
        self.driver         = webdriver.Firefox()

    def fetch_and_extract_text(self):
        """Fetch the webpage and extract text content from the body."""
        try:
            self.driver.get(self.url)

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            body = self.driver.find_element(By.TAG_NAME, "body")
            text_content = body.text

            with open(self.output_file, "w", encoding="utf-8") as file:
                file.write(text_content)

            print(f"Text content saved to {self.output_file}")

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            self.driver.quit()


"""if __name__ == "__main__":
    #URL         = "https://www.amazon.in/hz/mobile/mission?p=Awvb5PYPCdXItKNk4syR9w%2F8ZaEI%2FEWhSLq8neDBm2ZDN%2FiUpGTmmeLEaXhYjTydaUP1RHT%2BGq3wDqgl1VsLnYaGIm60jpyMp%2FENkU67HV9BrEL%2FMuJsyHoJAVbyza4fZgpw53GCiKuku%2Fy6GnDuUrki5PD6ijLBckEJuQwlkV8YnUajF8b2lBzL6SGo3urB4TT0o%2FR62IB%2BV2LZ0IeGB44TjQMhlNRmqGLs%2F2BBqbtKgkq5wujUsFBrDZ0FiTFqh%2Bby52Ea62F3hAMzSd%2BOTPSnmrUyiMI74568Ei%2Bew%2Bss36R%2FWtp6EjUVrIQjRTr7ofP3t9V4LiQBhk%2FtgSCTT7q71PLF%2F2t8%2FvM%2Fbi%2B%2FQp3Iaq7f5dfeJuXVim8CRIFFRTbNoNTKrlb1XZ%2FWlRnIDe5gYKbo0TfEJ1B%2F57iLhT8%3D&" 
    URL = "https://www.myntra.com/bodysuit/h%26m/-hm-infants-boys-pack-of-6-ribbed-cotton-bodysuit/30244605/buy"
    extractor   = SeleniumExtractor(url=URL)
    extractor.fetch_and_extract_text()"""