import requests
from bs4 import BeautifulSoup
import re


def extract_text_from_url_bs4(url):
    """
    Extracts the main text content from a news article URL using BeautifulSoup.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove script and style elements
        for script_or_style in soup(["script", "style", "noscript"]):
            script_or_style.decompose()

        # Try to find common content containers
        article_tags = soup.find_all(['article', 'div'], class_=lambda c: c and 'content' in c.lower())

        # Fallback 1: Use all <p> tags within the first identified article or div
        if article_tags:
            paragraphs = article_tags[0].find_all('p')
        else:
            # Fallback 2: Use all <p> tags in the entire document
            paragraphs = soup.find_all('p')

        # Fallback 3: If no <p> tags are present, use raw text from the body
        if not paragraphs and soup.body:
            text = soup.body.get_text(strip=True)
        else:
            text = "\n".join(p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True))

        # Perform a basic length check to ensure meaningful content
        if len(text) < 200:
            raise ValueError("Extracted content is too short to be meaningful.")

        return text

    except Exception as e:
        print(f"[Error scraping {url}]: {e}")
        return None

def is_url(input_str):
    url_pattern = re.compile(r'https?://\S+')
    return bool(url_pattern.match(input_str.strip()))

def extract_text_from_raw_input(raw_text):
    """
    Handles raw text input and returns it as-is.
    """
    return raw_text.strip()

def get_news_text(input_str):
    """
    Determines if the input is a URL or raw article text and returns the extracted content.
    """
    input_str = input_str.strip()

    if is_url(input_str):
        return extract_text_from_url_bs4(input_str)  # Uses BeautifulSoup for URL extraction
    else:
        return extract_text_from_raw_input(input_str)  # Handles raw text input