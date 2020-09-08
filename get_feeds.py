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
]


for feed in FEEDS:
    NewsFeed = feedparser.parse(feed)
    # print(json.dumps(NewsFeed.entries[0], indent=3, default=str))
    title = NewsFeed.entries[0]["title"]
    print(f"\n\n{feed}\n{title}")

