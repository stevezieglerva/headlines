import heapq
import json
import re
from datetime import datetime
from typing import List

import feedparser

STOP_WORDS = [
    "a",
    "about",
    "above",
    "after",
    "again",
    "against",
    "all",
    "am",
    "an",
    "and",
    "any",
    "are",
    "aren't",
    "as",
    "at",
    "be",
    "because",
    "been",
    "before",
    "being",
    "below",
    "between",
    "both",
    "but",
    "by",
    "can't",
    "cannot",
    "could",
    "couldn't",
    "did",
    "didn't",
    "do",
    "does",
    "doesn't",
    "doing",
    "don't",
    "down",
    "during",
    "each",
    "few",
    "for",
    "from",
    "further",
    "had",
    "hadn't",
    "has",
    "hasn't",
    "have",
    "haven't",
    "having",
    "he",
    "he'd",
    "he'll",
    "he's",
    "her",
    "here",
    "here's",
    "hers",
    "herself",
    "him",
    "himself",
    "his",
    "how",
    "how's",
    "i",
    "i'd",
    "i'll",
    "i'm",
    "i've",
    "if",
    "in",
    "into",
    "is",
    "isn't",
    "it",
    "it's",
    "its",
    "itself",
    "let's",
    "me",
    "more",
    "most",
    "mustn't",
    "my",
    "myself",
    "no",
    "nor",
    "not",
    "of",
    "off",
    "on",
    "once",
    "only",
    "or",
    "other",
    "ought",
    "our",
    "ours	ourselves",
    "out",
    "over",
    "own",
    "same",
    "shan't",
    "she",
    "she'd",
    "she'll",
    "she's",
    "should",
    "shouldn't",
    "so",
    "some",
    "such",
    "than",
    "that",
    "that's",
    "the",
    "their",
    "theirs",
    "them",
    "themselves",
    "then",
    "there",
    "there's",
    "these",
    "they",
    "they'd",
    "they'll",
    "they're",
    "they've",
    "this",
    "those",
    "through",
    "to",
    "too",
    "under",
    "until",
    "up",
    "very",
    "was",
    "wasn't",
    "we",
    "we'd",
    "we'll",
    "we're",
    "we've",
    "were",
    "weren't",
    "what",
    "what's",
    "when",
    "when's",
    "where",
    "where's",
    "which",
    "while",
    "who",
    "who's",
    "whom",
    "why",
    "why's",
    "with",
    "won't",
    "would",
    "wouldn't",
    "you",
    "you'd",
    "you'll",
    "you're",
    "you've",
    "your",
    "yours",
    "yourself",
    "yourselves",
    "new",
    "weeks",
]


class TopX:
    """
    Class that maintains the top N values in an array. Tuples can used to maintain the a list of top word frequencies (Ex: (5743, "the") and (473, "is")).
    """

    def __init__(self, topn):
        self.__topn = topn
        self.values = []

    def add(self, item):
        self.values.append(item)
        self.values = heapq.nlargest(self.__topn, self.values)


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


def get_lead_headlines_md(tmsp_datetime: datetime, topic: str, lead_headlines: list):
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


class LeadHeadlines:
    def __init__(self, headlines: List[str]) -> None:
        self.prep_to_raw_mapping = self.__prep_data(headlines)
        self.lead_headlines = self.__get_lead_headlines(headlines)

    def __str__(self):
        return f"""best_keywords: {self.best_keywords}
lead_headlines: {self.lead_headlines}
"""

    def __ngrams(self, input, n) -> List[str]:
        input_to_process = input.split(" ")
        output = []
        for i in range(len(input_to_process) - n + 1):
            output.append(input_to_process[i : i + n])
        return [" ".join(x) for x in output]

    def __prep_data(self, raw_headlines: List[str]) -> dict:
        prep_to_raw_mapping = {}
        for raw_headline in raw_headlines:
            input_list = raw_headline.split(" ")
            input_list_lower = [w.lower() for w in input_list]
            input_no_stop_words = [w for w in input_list_lower if w not in STOP_WORDS]
            input_no_possessives = [w.replace("'s", "") for w in input_no_stop_words]
            input_no_punc = [
                re.sub(r"[^a-zA-Z0-9 -']", " ", w) for w in input_no_possessives
            ]
            input_trim = [w.strip() for w in input_no_punc]
            input_line = " ".join(input_trim)
            prep_to_raw_mapping[input_line] = raw_headline
        print(json.dumps(prep_to_raw_mapping, indent=3, default=str))
        return prep_to_raw_mapping

    def __get_top_gram(self, headlines: list, gram_length: int):
        top_gram = TopX(3)
        counts_gram1 = {}
        for i in headlines:
            results = self.__ngrams(i, gram_length)
            for gram in results:
                # print(f"\t{gram}")
                counts_gram1[gram] = counts_gram1.get(gram, 0) + 1

        for k, v in counts_gram1.items():
            item = (v, k)
            top_gram.add(item)

        best_gram = top_gram.values[0]
        top_frequency = top_gram.values[0][0]
        ties = [gram for gram in top_gram.values if gram[0] == top_frequency]
        if len(ties) > 1:
            ties.sort(key=lambda x: x[1])
            print(f"Ties: {ties}")
            best_gram = ties[0]

        return best_gram

    def __get_best_keywords(self, headlines: list):
        top_gram1 = self.__get_top_gram(headlines, 1)
        top_gram2 = self.__get_top_gram(headlines, 2)
        top_gram3 = self.__get_top_gram(headlines, 3)

        top_all = TopX(1)
        top_all.add(top_gram1)
        top_all.add(top_gram2)
        top_all.add(top_gram3)

        print(top_gram1)
        print(top_gram2)
        print(top_gram3)

        if top_gram1[0] == 1 and top_gram2[0] == 1 and top_gram3[0] == 1:
            return ""

        if top_gram3[0] >= top_gram2[0] and top_gram3[0] >= top_gram1[0]:
            print("returning 3")
            return top_gram3[1]
        if top_gram2[0] >= top_gram1[0]:
            return top_gram2[1]

        if top_gram1[1] in top_gram2[1]:
            return top_gram2[1]
        return top_gram1[1]

    def __get_lead_headlines(self, headlines: list):
        prepped_headlines = [h for h in self.prep_to_raw_mapping.keys()]
        self.best_keywords = self.__get_best_keywords(prepped_headlines)
        if self.best_keywords == "":
            return []
        print(f"best_keyword: {self.best_keywords}")
        return [
            raw
            for prepped, raw in self.prep_to_raw_mapping.items()
            if self.best_keywords in prepped
        ]


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

    best_keywords = get_best_keywords(all_headlines)
    lead_headlines = get_lead_headlines(all_headlines)
    print(f"\nLead headlines: {lead_headlines}")
    lead_headline_md = get_lead_headlines_md(
        datetime.now(), best_keywords, lead_headlines
    )
    with open(f"headlines_site/content/lead_headlines.md", "w") as file:
        file.write(lead_headline_md)


if __name__ == "__main__":
    main()
