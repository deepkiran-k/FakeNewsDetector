from groq import Groq


class LLMNewsDetector:
    def __init__(self, groq_api_key):
        self.rate_limit_delay = 1.0# seconds
        self.client = Groq(api_key = groq_api_key)

    def extract_search_query(self, news_article):
        prompt = f"""
        You are a fact-checking assistant. Based on the news article below, generate a concise and general web search query that will help verify the truth of the claims in the article. Avoid including specific news sources in the query.

        News Article:
        \"\"\"{news_article}\"\"\"

        Only return the search query string.
        """

        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # or "gpt-3.5-turbo" if preferred llama-3.3-70b-versatile
                messages=[
                    {"role": "system", "content": "You are a credible news evaluator."},
                    {"role": "user", "content": prompt}
                ]
            )

            search_query = response.choices[0].message.content
            return search_query
        except Exception as e:
            print(f"Groq API call failed: {e}")
            return "Error generating search query."


    def generate_report_with_web_results(self, news_article, search_results):
        prompt = f"""
            You are a fact-checking assistant. Your task is to assess the credibility of a news article based on available web search results, or, if no relevant results are found, based on your own knowledge and reasoning.

            News Article:
            \"\"\"{news_article}\"\"\"

            Search Results:
            \"\"\"{search_results}\"\"\"

            Instructions:
            - Analyze the credibility of the news article.
            - If relevant and reliable search results are available, use them to assess the truthfulness.
            - If no search results are found, rely on your general knowledge and reasoning to evaluate the article.
            - Consider the presence or absence of coverage in credible sources, consistency of details, and tone of the article.

            Output Format:
            Verdict: (True / False / Inconclusive)  
            Explanation (4-5 lines): If false, provide the likely correct information. If true, elaborate on the event with any additional context.  
            Relevant Links: (If applicable, list links to trusted sources; if none available, write 'None found')  
            """
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                {"role": "system", "content": "You are a credible news evaluator."},
                {"role": "user", "content": prompt}
                ]
            )

            reply = response.choices[0].message.content

            # Parse the reply into a dictionary
            report = {}
            lines = reply.splitlines()
            for line in lines:
                if line.startswith("Verdict:"):
                    report['verdict'] = line.split(":", 1)[1].strip()
                elif line.startswith("Explanation:"):
                    report['explanation'] = line.split(":", 1)[1].strip()
                elif line.startswith("Relevant Links:"):
                    links = line.split(":", 1)[1].strip()
                    report['links'] = links.split(", ") if links != "None found" else []

            return report
        except Exception as e:
            print(f"GROQ API call failed: {e}")
            return {"verdict": "Error", "explanation": "Error generating the report.", "links": []}