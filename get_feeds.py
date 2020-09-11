import sys

print(sys.executable)
print("\n".join(sys.path))

import feedparser
import json
import re
from datetime import datetime


def escape_field(text):
    text = text.replace('"', '\\"')
    return text


def get_thumbnail_url(rss_entry):
    image_url_front = ""
    image_url = ""
    if "media_content" in rss_entry:
        image_url = rss_entry["media_content"][0]["url"]
        image_url_front = f"thumbnail: {image_url}"
    return image_url_front


def convert_rss_data_to_md(rss_entry, content_type):
    title = escape_field(rss_entry["title"])
    link = rss_entry["link"]
    published = rss_entry.get("published", "")
    image_url_front = get_thumbnail_url(rss_entry)
    summary = rss_entry["summary"]
    print(f"\n\n{title}")
    template = f"""---
title: "{title}"
date: {published}
{image_url_front}
target_link: {link}
type: {content_type}
categories:
    - {content_type}
---
{summary}"""
    return template


def get_about_file_md(tmsp_datetime):
    now = tmsp_datetime.isoformat()
    about = f"""---
title: "About"
date: {now}
draft: false
---
## Collection of top headlines for news site RSS feeds.

This site is auto-generated from a mixed collection of RSS feeds from different newsites to provide a mixture of view points. 
It grabs the [first](/first_headline) and [second](/second_headline) RSS entry from each feed. It also grabs some headlines from more [fringe](/fringe) websites.

Generated: {now}"""
    return about


def main():
    now = datetime.now().isoformat()
    about = get_about_file_md(datetime.now())
    with open(f"headlines_site/content/about.md", "w") as file:
        file.write(about)

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
        entry = NewsFeed.entries[0]
        md = convert_rss_data_to_md(entry, "first_headline")
        with open(
            f"headlines_site/content/first_headline/{now}_{count}.md", "w"
        ) as file:
            file.write(md)

        entry = NewsFeed.entries[1]
        md = convert_rss_data_to_md(entry, "second_headline")
        with open(
            f"headlines_site/content/second_headline/{now}_{count}.md", "w"
        ) as file:
            file.write(md)

    print("_________________")
    count = 0
    for feed in [
        "http://channels.feeddigest.com/rss/92907.xml",
        "http://feeds.feedburner.com/breitbart?format=xml",
        "https://www.wonkette.com/feeds/feed.rss",
        "http://feeds.dailykosmedia.com/dailykosofficial",
    ]:
        NewsFeed = feedparser.parse(feed)

        for entry in NewsFeed.entries[0:3]:
            count = count + 1
            title = escape_field(entry["title"])
            link = entry["link"]
            published = entry.get("published", "")
            image_url_front = ""
            image_url = ""
            if "media_content" in entry:
                image_url = entry["media_content"][0]["url"]
                image_url_front = f"thumbnail: {image_url}"
            summary = entry["summary"]
            print(f"\n\n{feed}\n{title}")
            template = f"""---
    title: "{title}"
    date: {published}
    {image_url_front}
    target_link: {link}
    type: fringe
    categories:
        - fringe
    ---
        {summary} """
            with open(f"headlines_site/content/fringe/{now}_{count}.md", "w") as file:
                file.write(template)


if __name__ == "__main__":
    main()
