import feedparser
import json


NewsFeed = feedparser.parse("http://rss.cnn.com/rss/cnn_topstories.rss")

print(json.dumps(NewsFeed.entries[0:1], indent=3, default=str))

