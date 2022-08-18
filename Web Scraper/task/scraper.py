import string
import requests
from bs4 import BeautifulSoup
import os

demanded_language = "en-US,en;q=0.5"
root = string.Template("https://www.nature.com/nature/articles?sort=PubDate&year=2020&page=$page")

n_pages = int(input())
article_type = input()

for i in range(1, n_pages + 1):
    os.mkdir(f"Page_{i}")
    url = root.substitute(page=i)
    response = requests.get(url)
    bs = BeautifulSoup(response.content, "html.parser").find_all("article")
    news_articles = list()
    for article in bs:
        x = article.find_all("span", {"data-test": "article.type"})
        for l in x:
            if l.text.strip() == article_type:
                news_articles.append(article.find("a"))
        for news_article in news_articles:
            headline = news_article.text
            for c in string.punctuation:
                if c in headline:
                    headline = headline.replace(c, "")
            headline = headline.replace(" ", "_")
            article_code = requests.get("https://www.nature.com" + news_article.attrs["href"]).content
            article_page = BeautifulSoup(article_code, "html.parser")\
                .find("div", {"class": "c-article-body u-clearfix"})
            with open(f"./Page_{i}/{headline}.txt", 'w') as file:
                file.write(article_page.text)
