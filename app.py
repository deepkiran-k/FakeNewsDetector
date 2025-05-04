from flask import Flask, render_template, request
from flask_cors import CORS
import json
from input import get_news_text, extract_text_from_url_bs4, is_url, extract_text_from_raw_input
from llm_call import LLMNewsDetector
from web import web_search

app = Flask(__name__)
CORS(app)  # Enables CORS for API routes

# Load credentials once
with open("creds.json", "r") as file:
    creds = json.load(file)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/articles')
def articles():
    return render_template('articles.html')

@app.route('/results', methods=['POST'])
def results():
    try:
        input_data = request.form.get('user_input')

        if not input_data:
            return render_template('results.html', error="No input provided. Please enter a URL or raw text.")

        if is_url(input_data):
            news_text = extract_text_from_url_bs4(input_data)
        else:
            news_text = extract_text_from_raw_input(input_data)

        if not news_text:
            raise ValueError("Failed to extract text from input.")

        # Initialize the detector
        detector = LLMNewsDetector(creds['groq_api_key'])
        search_query = detector.extract_search_query(news_text)

        if not search_query or "Error" in search_query:
            raise ValueError("Search query generation failed.")

        search_results = web_search(creds['google_api_key'], creds['google_cse_id'], search_query)

        if not search_results:
            raise ValueError("No search results found.")

        # Generate the report using web search results
        report = detector.generate_report_with_web_results(news_text, search_results)

        # Check if report is a dictionary and contains expected keys
        if isinstance(report, dict):
            if 'verdict' in report and 'explanation' in report:
                structured_report = {
                    'verdict': report['verdict'],  # Example: 'False'
                    'explanation': report['explanation'],  # Example: 'The news article claims India has a population of 2.4 billion...'
                    'links': report.get('links', [])  # Default to empty list if no links
                }
                return render_template('results.html', **structured_report)
            else:
                raise ValueError("Report does not contain expected keys.")
        else:
            raise ValueError(f"Invalid report format: {type(report)}. Expected a dictionary.")

    except Exception as e:
        return render_template('results.html', verdict='Error', explanation=f"An error occurred: {str(e)}", links=[])

if __name__ == '__main__':
    app.run(debug=True)
