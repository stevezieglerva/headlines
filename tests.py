import unittest
from unittest.mock import patch, Mock, MagicMock, PropertyMock
from get_feeds import *


class UnitTests(unittest.TestCase):
    def test_convert_rss_data_to_md__given_rss_data_with_thumbnail__correct_md_text_returned(
        self,
    ):
        # Arrange
        rss_entry = {
            "title": "The warning isn't new. Experts have long cautioned the months ahead will be challenging. Here's why.",
            "link": "http://rss.cnn.com/~r/rss/cnn_topstories/~3/b-gJezqWSTM/index.html",
            "summary": "Nearly 30 US states are reporting downward trends in...",
            "media_content": [
                {
                    "url": "https://cdn.cnn.com/cnnnext/dam/assets/200911014935-us-coronavirus-friday-0906-restricted-super-169.jpg"
                }
            ],
        }

        # Act
        results = convert_rss_data_to_md(rss_entry, "first_headline")

        # Assert
        expected = """---
title: "The warning isn't new. Experts have long cautioned the months ahead will be challenging. Here's why."
date: 
thumbnail: https://cdn.cnn.com/cnnnext/dam/assets/200911014935-us-coronavirus-friday-0906-restricted-super-169.jpg
target_link: http://rss.cnn.com/~r/rss/cnn_topstories/~3/b-gJezqWSTM/index.html
type: first_headline
categories:
    - first_headline
---
Nearly 30 US states are reporting downward trends in..."""
        print(results)
        self.assertEqual(results, expected)

    def test_convert_rss_data_to_md__given_rss_data_without_thumbnail__correct_md_text_returned(
        self,
    ):
        # Arrange
        rss_entry = {
            "title": "The warning isn't new. Experts have long cautioned the months ahead will be challenging. Here's why.",
            "link": "http://rss.cnn.com/~r/rss/cnn_topstories/~3/b-gJezqWSTM/index.html",
            "summary": "Nearly 30 US states are reporting downward trends in...",
        }

        # Act
        results = convert_rss_data_to_md(rss_entry, "first_headline")

        # Assert
        expected = """---
title: "The warning isn't new. Experts have long cautioned the months ahead will be challenging. Here's why."
date: 

target_link: http://rss.cnn.com/~r/rss/cnn_topstories/~3/b-gJezqWSTM/index.html
type: first_headline
categories:
    - first_headline
---
Nearly 30 US states are reporting downward trends in..."""
        print(results)
        self.assertEqual(results, expected)

    def test_convert_rss_data_to_md__given_rss_data_with_publish_date__correct_md_text_returned(
        self,
    ):
        # Arrange
        rss_entry = {
            "title": "The warning isn't new. Experts have long cautioned the months ahead will be challenging. Here's why.",
            "link": "http://rss.cnn.com/~r/rss/cnn_topstories/~3/b-gJezqWSTM/index.html",
            "summary": "Nearly 30 US states are reporting downward trends in...",
            "published": "1/1/00",
        }

        # Act
        results = convert_rss_data_to_md(rss_entry, "first_headline")

        # Assert
        expected = """---
title: "The warning isn't new. Experts have long cautioned the months ahead will be challenging. Here's why."
date: 1/1/00

target_link: http://rss.cnn.com/~r/rss/cnn_topstories/~3/b-gJezqWSTM/index.html
type: first_headline
categories:
    - first_headline
---
Nearly 30 US states are reporting downward trends in..."""
        print(results)
        self.assertEqual(results, expected)

    def test_get_about_md__given_normal_use__then_about_md_returned(self):
        # Arrange
        now = datetime(2020, 1, 1, 13, 4, 5)

        # Act
        results = get_about_file_md(now)
        print(results)

        # Assert
        expected = """---
title: "About"
date: 2020-01-01T13:04:05
draft: false
---
## Collection of top headlines for news site RSS feeds.

This site is auto-generated from a mixed collection of RSS feeds from different newsites to provide a mixture of view points. 
It grabs the [first](/first_headline) and [second](/second_headline) RSS entry from each feed. It also grabs some headlines from more [fringe](/fringe) websites.

Generated: 2020-01-01T13:04:05"""
        self.assertEqual(results, expected)


if __name__ == "__main__":
    unittest.main()
