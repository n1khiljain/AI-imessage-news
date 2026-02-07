# Fetch data from TechCrunch (news scraping)
import requests as re
from bs4 import BeautifulSoup as bs
import feedparser

URL = "https://techcrunch.com/feed"

def get_data(url):

    feed = feedparser.parse(url)
    
    articles = []

    for entry in feed.entries[:10]:
        article_text = get_article_text(entry.link)
        articles.append(
            {
                'title': entry.title,
                'link': entry.link,
                'published': entry.published,
                'summary': entry.summary,
                'text': article_text
            }
        )
    
    return articles

def get_article_text(url):
    """
    Get the text of an article from a URL passed in.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    response = re.get(url, headers=headers)
    soup = bs(response.text, 'html.parser')
    
    article = soup.find('article') or soup.find('div', class_='entry-content')
    
    if article:
        # Get all paragraph text
        paragraphs = article.find_all('p')
        text = '\n\n'.join(p.get_text(strip=True) for p in paragraphs)
        return text
    return None


if __name__ == '__main__':
    articles = get_data(URL)
    
"""
articles: List[dict] - A list of article dictionaries

Structure:
    articles = [
        {
            'title': str,      # Article headline (e.g., "OpenAI launches new model")
            'link': str,       # Full URL to the article
            'published': str,  # Publication date (e.g., "Thu, 06 Feb 2026 12:00:00 +0000")
            'summary': str,    # Short description/excerpt (may contain HTML)
            'text': str|None   # Full article text (paragraphs joined by newlines), or None if fetch failed
        },
        ...
    ]

Usage examples:
    articles[0]['title']       # Get first article's title
    articles[2]['link']        # Get third article's URL
    
    for article in articles:
        print(article['title'])
        
    # Get all titles as a list
    titles = [a['title'] for a in articles]
"""

