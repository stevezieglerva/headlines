import feedparser
import json

FEEDS = [
    "http://rss.cnn.com/rss/cnn_topstories.rss",
    "https://www.washingtontimes.com/rss/headlines/news/national/",
    "https://nypost.com/news/feed/",
    "https://rss.nytimes.com/services/xml/rss/nyt/US.xml",
    "https://www.aljazeera.com/xml/rss/all.xml",
    "https://www.dailymail.co.uk/articles.rss",
    "http://feeds.foxnews.com/foxnews/national",
    "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
    "https://feeds.thedailybeast.com/rss/articles",
    "https://www.cnbc.com/id/100003114/device/rss/rss.html",
    "https://feeds.npr.org/1001/rss.xml",
    "https://www.huffpost.com/section/front-page/feed?x=1",
    "https://feeds.a.dj.com/rss/RSSWorldNews.xml",
    "https://www.theepochtimes.com/c-us-features/feed",
]

print("_________________")
count = 0
for feed in FEEDS:
    count = count + 1
    NewsFeed = feedparser.parse(feed)
    # print(json.dumps(NewsFeed.entries[0], indent=3, default=str))
    title = NewsFeed.entries[0]["title"].replace(":", "-")
    link = NewsFeed.entries[0]["link"]
    image_url_front = ""
    image_url = ""
    if "media_content" in NewsFeed.entries[0]:
        image_url = NewsFeed.entries[0]["media_content"][0]["url"]
        image_url_front = f"thumbnail: {image_url}"
    summary = NewsFeed.entries[0]["summary"]
    print(f"\n\n{feed}\n{title}\n\t{link}\n\t\t{image_url}")
    entry = json.dumps(NewsFeed.entries[0], indent=3, default=str)

    template = f"""---
title: {title}
date: '2015-07-28'
{image_url_front}
target_link: {link}
---
{summary} """
    with open(f"headlines_site/content/posts/{count}.md", "w") as file:
        file.write(template)

    print(entry)

