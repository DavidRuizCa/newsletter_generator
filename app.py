import gradio as gr

from services.web_searcher import get_news_webs
from services.web_scraper import Website, get_webs_content, read_news
from services.agents import news_sources_extractor, relevant_news_extractor, newsletter_generator

def generate_newsletter(topic):
    # Check if the topic is empty
    if not len(topic):
        raise gr.Error("Topic cannot be empty")
  
    # Orchestration of the complete flow
    yield gr.update(value=f"### ⏳ Searching for {topic} news sources...")
    search_results = get_news_webs(topic)  # Search for news sources
    webs_content = get_webs_content(search_results)  # Extract content from search results

    yield gr.update(value=f"### ⏳ Identifying the best {topic} news sources...")
    news_sources = news_sources_extractor(topic, webs_content)  # Identify the best sources
    
    yield gr.update(value=f"### ⏳ Extracting the most relevant {topic} news articles...")
    news = get_webs_content(news_sources['selected_sources'])  # Retrieve content from selected sources
    relevant_news = relevant_news_extractor(topic, news)  # Extract the most relevant news

    yield gr.update(value=f"### ⏳ Reading the most relevant {topic} news articles...")
    relevant_news_content = read_news(relevant_news['articles'])  # Read and process the relevant news articles
    
    yield gr.update(value=f"### ⏳ Generating the {topic} newsletter...")
    newsletter = newsletter_generator(topic, relevant_news_content)  # Generate the newsletter
    yield gr.update(value=newsletter)

# Create the Gradio interface with a centered layout
with gr.Blocks(theme=gr.themes.Ocean()) as demo:
    with gr.Row():  
        with gr.Column(scale=1):  # Empty column for left margin
            pass
        with gr.Column(scale=6):  # Main content column
            gr.Markdown("# AI-Powered Newsletter Generator", elem_classes="centered-text")
            gr.Markdown("Enter a topic and receive a newsletter within seconds!", elem_classes="centered-text")

            gr.Markdown("""### How It Works
            1. Finds the best news sources for your topic.  
            2. Dives into those sources and tracks down the hottest, most relevant articles.  
            3. Handpicks the must-read ones so you get only the best.  
            4. Summarizes everything into a complete, easy-to-read newsletter—with references!  
            """, elem_classes="centered-text")

            topic_input = gr.Textbox(label="Topic of Interest", placeholder="E.g., Artificial Intelligence, Climate Change...")
            submit_btn = gr.Button("Generate Newsletter", variant="primary")
            output = gr.Markdown("") 
            
            submit_btn.click(
                fn=generate_newsletter,
                inputs=[topic_input],
                outputs=output
            )
        with gr.Column(scale=1):  # Empty column for right margin
            pass

# Launch the application
if __name__ == "__main__":
    demo.launch(inbrowser=True)