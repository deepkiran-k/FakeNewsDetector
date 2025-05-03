from flask import Flask, request, jsonify
from input import get_news_text, extract_text_from_url_bs4, is_url, extract_text_from_raw_input
from llm_call import LLMNewsDetector
from web import web_search
import json

app = Flask(__name__)

# Load API keys from creds.json
with open("creds.json", "r") as file:
    creds = json.load(file)

@app.route("/api/extract", methods=["POST"])
def extract_text():
    """
    Extracts the main text content from a URL or processes raw text input.
    """
    data = request.json
    input_str = data.get("input", "").strip()

    if is_url(input_str):
        # If the input is a URL, extract text from the URL
        extracted_text = extract_text_from_url_bs4(input_str)
    else:
        # If the input is raw text, process it directly
        extracted_text = extract_text_from_raw_input(input_str)

    if not extracted_text:
        return jsonify({"error": "Failed to extract meaningful content"}), 400

    return jsonify({"extracted_text": extracted_text})

@app.route("/api/query", methods=["POST"])
def generate_query():
    """
    Generates a search query based on the provided news text using LLM.
    """
    data = request.json
    news_text = data.get("news_text", "").strip()

    if not news_text:
        return jsonify({"error": "News text is required"}), 400

    detector = LLMNewsDetector(creds['groq_api_key'])
    search_query = detector.extract_search_query(news_text)

    if not search_query or "Error" in search_query:
        return jsonify({"error": "Failed to generate a search query"}), 400

    return jsonify({"search_query": search_query})

@app.route("/api/search", methods=["POST"])
def perform_search():
    """
    Performs a web search using the provided query and returns results.
    """
    data = request.json
    query = data.get("query", "").strip()

    if not query:
        return jsonify({"error": "Search query is required"}), 400

    search_results = web_search(
        creds['google_api_key'],
        creds['google_cse_id'],
        query
    )

    if not search_results:
        return jsonify({"error": "No search results found for the given query"}), 400

    return jsonify({"search_results": search_results})

@app.route("/api/report", methods=["POST"])
def generate_report():
    """
    Generates an analysis report based on the news text and search results using LLM.
    """
    data = request.json
    news_text = data.get("news_text", "").strip()
    search_results = data.get("search_results", "")

    if not news_text or not search_results:
        return jsonify({"error": "News text and search results are required"}), 400

    detector = LLMNewsDetector(creds['groq_api_key'])
    report = detector.generate_report_with_web_results(news_text, search_results)

    if not report or "Error" in report:
        return jsonify({"error": "Failed to generate the analysis report"}), 400

    return jsonify({"report": report})

if __name__ == "__main__":
    app.run(debug=True)