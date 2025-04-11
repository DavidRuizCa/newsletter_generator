from config.settings import OPENAI_API_KEY
from openai import OpenAI
import json
from loguru import logger

MODEL = 'gpt-4o-mini'
openai = OpenAI(api_key=OPENAI_API_KEY)

def get_openai_response(system_prompt, user_prompt):
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    result = response.choices[0].message.content
    return result

def get_openai_json_response(system_prompt, user_prompt):
    response = openai.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"}
    )
    result = response.choices[0].message.content
    return result

def news_sources_extractor(topic, webs_content):
    logger.info(f"Compiling relevant sources for {topic} news")
    
    system_prompt_news_pages_link_extractor = f"""You are a curator tasked with identifying potential news sources about {topic}.

    You will analyze search results that recommend websites for {topic} information.

    YOUR TASK:
    - From the provided search results, identify 3-5 links that appear to be the most relevant sources for {topic} information.
    - Prioritize links that are mentioned multiple times across different search results.
    - Only select news websites. Avoid company websites, product pages, or corporate blogs.
    - Focus on URLs that appear to be standalone websites rather than social media pages.
    - Look for clues in the descriptions that suggest the sites focus specifically on {topic}.\n"""

    system_prompt_news_pages_link_extractor += """YOUR RESPONSE MUST BE IN THIS FORMAT (JSON):
    { 
    "selected_sources": [ 
        { 
        "name": "Name extracted from the URL or description", 
        "href": "https://example.com", 
        "reason_for_selection": "Brief explanation based on available information" 
        },
        ...
    ] 
    }
    """
    system_prompt_news_pages_link_extractor += """
    IMPORTANT: Base your selections only on the information available in the search results. Do not make assumptions about authority, update frequency, or bias unless explicitly mentioned in the search results.
    """

    user_prompt_news_pages_link_extractor = f"Here is a list of search results that recommend websites for the latest news on {topic}. You will find title, content, and a list of links contained in the website.\n"
    user_prompt_news_pages_link_extractor += f"Please decide which of these are relevant web links for gathering news for a {topic} newsletter, respond with the full https URL in JSON format."
    user_prompt_news_pages_link_extractor += "Here is the list of search results:\n"
    user_prompt_news_pages_link_extractor += json.dumps(webs_content)

    result = get_openai_json_response(system_prompt_news_pages_link_extractor, user_prompt_news_pages_link_extractor)
    
    return json.loads(result)


def relevant_news_extractor(topic, news):
    logger.info(f"Compiling relevant news for {topic}")

    system_prompt_news_selector = f"""You are an expert news content analyzer. Your task is to process the extracted content from a news website landing page and identify the most relevant news articles related to the {topic} topic.  

    YOUR TASK:  
    - Analyze the provided webpages content and extract only the 7-9 links to news articles that are directly related to the {topic} topic.  
    - Exclude advertisements, general section links, or unrelated content.  
    - Ensure that the extracted articles provide valuable insights or updates on the given topic.  
    - Try to vary your sources. Select articles from different websites whenever possible to avoid relying too heavily on a single source.\n"""  

    system_prompt_news_selector += """YOUR RESPONSE MUST BE IN THIS FORMAT (JSON):  
    {  
    "articles": [  
        {  
        "title": "Extracted article title",  
        "href": "https://example.com"  
        },  
        ...  
    ]  
    }  \n"""  

    user_prompt_news_selector = f"""Here is the extracted content from a several news websites along with a specific topic. Your task is to filter and extract the most relevant news articles related to this topic.  

    It is really important that you respond with the full https URL.

    TOPIC: {topic}  

    CONTENT FROM THE NEWS PAGES:  
    {news}  

    Please return a structured JSON with only the most relevant news articles."""

    result = get_openai_json_response(system_prompt_news_selector, user_prompt_news_selector)
    
    return json.loads(result)

def newsletter_generator(topic, articles):
    logger.info(f"Generating {topic} newsletter")

    system_prompt_newsletter_generator = f"""You are an assistant specialized in creating engaging and informative newsletters. Your task is to generate a well-structured newsletter about the {topic} topic and a set of articles.  

    You should follow the following structure. You don't need to name each section 'Title', 'Headline', etc., but you should include all the information in the same order.:
    - Title
    - Headline
    - Introduction
    - Summaries of the selected articles including article title, publication date and a link to the full article.


    ### YOUR TASK:  
    - Create a professional and compelling newsletter based on the provided articles.
    - Write a catchy headline that will grab the reader's attention.
    - Summarize each article concisely, highlighting the most important information, making it informative, engaging and entertaining.  
    - Include article links so readers can explore further.
    - Include the publication date of each article.
    - **Respond in Markdown format. Starting with '"""' and ending with '"""'**.\n"""

    user_prompt_newsletter_generator = f"""You will receive a set of articles along with a topic. 

    Your task is to generate a newsletter that summarizes the key insights from these articles.
    It is really important that the publication date of each article is included in the summary.  

    ### **Topic:**  
    {topic}  

    ### **Articles:** 
    {articles} 

    Return only the completed newsletter in markdown format.  
    """

    result = get_openai_response(system_prompt_newsletter_generator, user_prompt_newsletter_generator)

    return result