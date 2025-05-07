from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
from input import get_news_text, extract_text_from_url_bs4, is_url, extract_text_from_raw_input
from llm_call import LLMNewsDetector
from web import web_search
from db_connect import create_db_connection, store_search_result, get_latest_search_results, get_dashboard_data

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
        if isinstance(report, dict) and 'verdict' in report and 'explanation' in report:
            # Structured report
            structured_report = {
                'verdict': report['verdict'],  # Example: 'False'
                'explanation': report['explanation'],  # Example: 'The news article claims India has a population of 2.4 billion...'
                'links': report.get('links', [])  # Default to empty list if no links
            }

            # Store the result in the database
            try:
                conn = create_db_connection(creds['dbhost'], creds['dbuser'], creds['dbname'])  # Update with your DB details
                store_search_result(
                    conn,
                    user_id=1,  # Replace with the actual user ID if using authentication
                    search_query=input_data,
                    verdict=structured_report['verdict'],
                    explanation=structured_report['explanation'],
                    relevant_links=", ".join(structured_report['links'])  # Convert links list to a comma-separated string
                )
                conn.close()
            except Exception as db_error:
                print(f"Error storing search result: {db_error}")

            return render_template('results.html', **structured_report)

        else:
            raise ValueError("Report does not contain expected keys or is not in the correct format.")

    except Exception as e:
        return render_template('results.html', verdict='Error', explanation=f"An error occurred: {str(e)}", links=[])

@app.route('/search')
def search():
    try:
        # Replace with actual user ID if using authentication
        user_id = 1

        # Fetch the latest search results from the database
        conn = create_db_connection(creds['dbhost'], creds['dbuser'], creds['dbname'])  # Update with your DB details
        results = get_latest_search_results(conn, user_id, limit=10)
        conn.close()

        # Render the search history page with the results
        return render_template('search.html', results=results)

    except Exception as e:
        return render_template('search.html', results=[], error=str(e))

@app.route('/dashboard-data')
def dashboard_data():
    try:
        conn = create_db_connection(creds['dbhost'], creds['dbuser'], creds['dbname'])

        # Call the refactored function to fetch dashboard data
        data = get_dashboard_data(conn)

        conn.close()
        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
