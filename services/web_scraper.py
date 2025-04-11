from bs4 import BeautifulSoup
import requests
from loguru import logger

# A class to represent a Webpage

# Some websites need you to use proper headers when fetching them:
headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

class Website:
    def __init__(self, url):
        self.url = url
        self.title = "No title found"
        self.text = ""
        self.links = []
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status() 
            self.body = response.content
            
            soup = BeautifulSoup(self.body, 'html.parser')
            self.title = soup.title.string if soup.title else "No title found"
            
            if soup.body:
                for irrelevant in soup.body(["script", "style", "img", "input"]):
                    irrelevant.decompose()
                self.text = soup.body.get_text(separator="\n", strip=True)

            self.links = [link.get('href') for link in soup.find_all('a') if link.get('href')]

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch {url}: {e}")

    def get_contents(self):
        return f"Webpage Title:\n{self.title}\nWebpage Contents:\n{self.text}\nWebpage Links:\n{self.links}\n\n"
    
def get_webs_content(webs):
    logger.info(f"Looking for news sources in {len(webs)} websites")
    selected_sources = []
    for web in webs:
        try:
            site = Website(web["href"])
            website_data = {
                "title": site.title,
                "content": site.text,
                "links": site.links
            }
            selected_sources.append(website_data)
            logger.info(f"Content extracted from {web['href']}")
        except Exception as e:
            logger.error(f"Error processing {web['href']}: {str(e)}")
            print(f"Error processing {web['href']}: {str(e)}")
            
    return selected_sources


def read_news(relevant_news):
    logger.info(f"Reading articles")
    articles = []
    for article in relevant_news:
        try:
            site = Website(article['href'])
            website_data = {
                "title": site.title,
                "content": site.text,
                "url": article['href']
            }
            articles.append(website_data)
            logger.info(f"Content extracted from {article['href']}")
        except Exception as e:
            logger.error(f"Error processing {relevant_news['href']}: {str(e)}")
            print(f"Error processing {relevant_news['href']}: {str(e)}")
    return articles