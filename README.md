# AI-Powered Newsletter Generator

This application generates a newsletter based on a user-provided topic using AI. It searches for relevant news sources, extracts the most important articles, and summarizes them into a concise, easy-to-read newsletter.

## Features

1. **Search for News Sources**: Finds the best and most reliable news sources for the given topic.
2. **Content Extraction**: Extracts content from the identified sources.
3. **Relevance Filtering**: Selects the most relevant articles for the topic.
4. **Newsletter Generation**: Summarizes the articles into a well-structured newsletter with references.

## How It Works

1. Enter a topic of interest in the input box.
2. The app searches for news sources related to the topic.
3. It identifies the most relevant sources and extracts their content.
4. The app generates a newsletter summarizing the key insights from the articles.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/DavidRuizCa/newsletter_generator.git
   ```
2. Navigate to the `Newsletter` folder:
   ```bash
   cd Newsletter
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```bash
   python app.py
   ```
2. Open the Gradio interface in your browser.
3. Enter a topic in the input box and click "Generate Newsletter".
4. View the generated newsletter in the output section.

## Requirements

- Python 3.8 or higher
- Required Python libraries (install via `requirements.txt`)

## Folder Structure

```
Newsletter/
├── app.py                # Main application file
├── services/             # Contains helper modules for web scraping, searching, and AI agents
├── README.md             # Documentation for the app
├── requirements.txt      # List of dependencies
```

## Notes

- Ensure you have an active internet connection to fetch news sources and generate newsletters.
- The app uses OpenAI's GPT model for summarization. Make sure to set up your API key in the environment variables.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## 👤 Contact

Developed by [David Ruiz Casares](https://www.linkedin.com/in/david-ruiz-casares/).
