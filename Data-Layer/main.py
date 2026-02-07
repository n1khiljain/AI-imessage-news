# Fetch data from TechCrunch (news scraping)
import requests as re
from bs4 import BeautifulSoup as bs
import feedparser

URL = "https://techcrunch.com/feed"

def get_data(url):

    feed = feedparser.parse(url)
    
    articles = []

    for entry in feed.entries[:10]:
        articles.append(
            {
                'title': entry.title,
                'link': entry.link,
                'published': entry.published,
                'summary': entry.summary
            }
        )
    
    return articles


if __name__ == '__main__':
    articles = get_data(URL)
    for article in articles:
        print(article["title"])
        print(article["summary"])


