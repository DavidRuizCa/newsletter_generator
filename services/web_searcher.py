from duckduckgo_search import DDGS
from loguru import logger

def get_news_webs(topic):
    logger.info(f"Searching results for news sites on {topic}")
    results = DDGS().text(f"Best reliable news sites for {topic} latest news", max_results=5)
    logger.info(f"Found search results for news sites on {topic}")

    return results