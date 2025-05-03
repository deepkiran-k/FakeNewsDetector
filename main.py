import json
from input import get_news_text, extract_text_from_url_bs4, is_url, extract_text_from_raw_input
from llm_call import LLMNewsDetector
from web import web_search


def main():
    try:
        # Step 1: Load configuration from JSON file
        with open("creds.json", "r") as file:
            creds = json.load(file)

        print("Configuration loaded successfully.")

        # Step 2: Retrieve user input (either a URL or raw text)
        input_data = input("Enter a news URL or the raw news text: ").strip()

        # Step 3: Determine the type of input and process accordingly
        if is_url(input_data):
            print("Input is identified as a URL. Extracting content...")
            news_text = extract_text_from_url_bs4(input_data)
        else:
            print("Input is identified as raw text. Processing...")
            news_text = extract_text_from_raw_input(input_data)

        if not news_text:
            raise ValueError("Failed to extract meaningful content from the input.")

        print("News text processed successfully.")

        # Step 4: Initialize LLMNewsDetector
        detector = LLMNewsDetector(creds['groq_api_key'])

        # Step 5: Generate search query using LLM
        print("Generating search query using Groq AI...")
        search_query = detector.extract_search_query(news_text)
        if not search_query or "Error" in search_query:
            raise ValueError("Failed to generate a search query.")

        print(f"Search query generated: {search_query}")

        # Step 6: Perform web search using the generated query
        print("Performing web search to gather corroborating information...")
        search_results = web_search(
            creds['google_api_key'],
            creds['google_cse_id'],
            search_query
        )
        if not search_results:
            raise ValueError("No search results found for the given query.")

        print("Web search completed successfully.")

        # Step 7: Generate analysis report using LLM
        print("Generating analysis report with Groq AI...")
        report = detector.generate_report_with_web_results(news_text, search_results)
        if not report or "Error" in report:
            raise ValueError("Failed to generate the analysis report.")

        print("Report generated successfully.")
        print("----- Analysis Report -----")
        print(report)

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
