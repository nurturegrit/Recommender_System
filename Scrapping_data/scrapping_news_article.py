"""
pip install beautifulsoup4
pip install requests
pip install pandas

By using requests to fetch webpage and beautifulsoup to parse HTML.
Scrapping from nbc news
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os


def scrape_headlines_and_link(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        print(f"The response code is {response.status_code}")
        soup = BeautifulSoup(response.content, "html.parser")
        headlines = []
        for h2 in soup.find_all("h2"):
            headline_text = h2.get_text(strip=True)
            link = h2.find("a")
            if link and "href" in link.attrs:
                link = link["href"]
                if not link.startswith("http"):
                    link = requests.compat.urljoin(url, link)
                headlines.append({"headline": headline_text, "link": link})
        return headlines
    except Exception as e:
        print(f"error while scrapping {url} : {e}")
        return []


def scrape_article_content(article_url):
    try:
        response = requests.get(article_url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.content, "html.parser")
        article_body = soup.find("article") or soup.find("div", class_="main-content")
        if article_body:
            para = article_body.find_all("p")
            content = " ".join([p.get_text(strip=True) for p in para])
            return content.strip()
        return None
    except Exception as e:
        print(f"Error scraping article {article_url}: {e}")
        return None


url = "https://www.nbcnews.com/"
data = []
processed_items = set()

print(f"Scraping headlines from: {url}")
h_l = scrape_headlines_and_link(url)
for item in h_l:
    identifier = (item["headline"], item["link"])
    if identifier not in processed_items:
        processed_items.add(identifier)
        print(f"Scraping article: {item['link']}")
        content = scrape_article_content(item["link"])
        if content:
            data.append({"headline": item["headline"], "content": content})

df = pd.DataFrame(data)
df.drop_duplicates(subset=["headline", "content"], inplace=True)
df.to_csv("scraped_news.csv", index=False)

print(f"Data saved to {os.path.join(os.getcwd(), 'scraped_news.csv')}")
