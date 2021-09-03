import functools
import heapq
import json
import re
from dataclasses import dataclass
from datetime import datetime
from typing import List

import feedparser

from LeadHeadlines import LeadHeadlines


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


def get_lead_headlines_md(tmsp_datetime: datetime, leads: LeadHeadlines):
    topic = leads.best_keywords
    lead_headlines = leads.lead_headlines
    now = tmsp_datetime.isoformat()
    headlines_list = [f"* {h}" for h in lead_headlines]
    headlines_str = "\n".join(headlines_list)
    md = f"""---
title: "Lead Headlines"
date: {now}
draft: false
---
## Lead headlines for '{topic}':
{headlines_str}



Generated: {now}"""
    return md


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
    all_headlines = []
    for feed in FEEDS:
        count = count + 1
        NewsFeed = feedparser.parse(feed)
        first = True
        for entry in NewsFeed.entries[0:2]:
            all_headlines.append(entry["title"])
            content_type = "first_headline"
            if not first:
                content_type = "second_headline"
            md = convert_rss_data_to_md(entry, content_type)
            with open(
                f"headlines_site/content/{content_type}/{now}_{count}.md", "w"
            ) as file:
                file.write(md)
            first = False

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
            md = convert_rss_data_to_md(entry, "fringe")
            with open(f"headlines_site/content/fringe/{now}_{count}.md", "w") as file:
                file.write(md)

    leads = LeadHeadlines(all_headlines)
    print(repr(leads))
    print(f"\nLead headlines: {leads.lead_headlines}")
    lead_headline_md = get_lead_headlines_md(datetime.now(), leads)
    with open(f"headlines_site/content/lead_headlines.md", "w") as file:
        file.write(lead_headline_md)


if __name__ == "__main__":
    main()
