from groq import Groq

class LLMNewsDetector:
    def __init__(self, groq_api_key):
        self.rate_limit_delay = 1.0# seconds
        self.client = Groq(api_key = groq_api_key)

    def extract_search_query(self, news_article):
        prompt = f"""         
        Based on the following news article, generate a concise web search query to find related or corroborating information online to assess the credibility of the article. 

        News Article: 
        \"\"\"{news_article}\"\"\"

        Only return the search query string, nothing else.         
        """
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # or "gpt-3.5-turbo" if preferred
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
        Evaluate the following news article and the related search results to determine if the news is true or false. Consider the credibility of the sources, the consistency of the information, and any sensationalist or biased tones.

        News Article: 
        \"\"\"{news_article}\"\"\"

        Search Results: 
        \"\"\"{search_results}\"\"\"
        
        Verdict: (True / False / Inconclusive)
        Explanation (4-5 lines):  if the news is false provide the correct news if the news is true provide details about it 
        
        also provide the links to correct news articles       
        """
        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # or "gpt-3.5-turbo" if preferred
                messages=[
                    {"role": "system", "content": "You are a credible news evaluator."},
                    {"role": "user", "content": prompt}
                ]
            )

            reply = response.choices[0].message.content
            return reply
        except Exception as e:
            print(f"GROQ API call failed: {e}")
            return "Error generating reply."
