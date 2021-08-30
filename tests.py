import unittest
from datetime import datetime
from unittest.mock import MagicMock, Mock, PropertyMock, patch

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

    def test_ngrams__given_headline__then_ngrams_returned_without_stop_words_and_punctuation(
        self,
    ):
        # Arrange
        input = "Hurricane Ida has really strong winds!"

        # Act
        results = ngrams(input, 3)
        print(results)

        # Assert
        self.assertEqual(
            results,
            ["hurricane ida really", "ida really strong", "really strong winds"],
        )

    def test_get_best_keywords__given_headlines__then_best_returned(self):
        # Arrange
        input = [
            "Families forced to queue for hours at Heathrow border control",
            "Canada election: Will declining consumer confidence hurt Trudeau?",
            "Texas ‘freedom defender’ who rallied against COVID-19 measures dies",
            "Ida now a tropical storm as more than 1 million Louisiana utility customers are left without power",
            "As The Lake Tahoe Wildfire Spreads, Everyone On The California Side Is Told To Leave",
            "Haiti Quake Turned Baptism Celebration Into Tragedy",
            "In New Orleans and beyond, evacuations are underway.",
            "Live: 'Covid's C.1.2 variant may be more infectious, evade vaccine protection'",
            "Authorities conduct search-and-rescue efforts in Ida's aftermath. 'The worst-case scenario seems to have happened' in Jefferson Parish, an official says.",
            "Raging California wildfire threatens Lake Tahoe, prompts evacuations",
            "Ida now a tropical storm",
            "Ida now a tropical storm",
        ]

        # Act
        results = get_best_keywords(input)

        # Assert
        self.assertEqual(results, "now tropical storm")

    def test_get_best_keywords__given_other_headlines__then_best_returned(self):
        # Arrange
        input = [
            "Families forced to queue for hours at Heathrow border control",
            "Canada election: Will declining consumer confidence hurt Trudeau?",
            "Texas ‘freedom defender’ who rallied against COVID-19 measures dies",
            "Ida now a tropical storm as more than 1 million Louisiana utility customers are left without power",
            "As The Lake Tahoe Wildfire Spreads, Everyone On The California Side Is Told To Leave",
            "Haiti Quake Turned Baptism Celebration Into Tragedy",
            "In New Orleans and beyond, evacuations are underway.",
            "Live: 'Covid's C.1.2 variant may be more infectious, evade vaccine protection'",
            "Authorities conduct search-and-rescue efforts in Ida's aftermath. 'The worst-case scenario seems to have happened' in Jefferson Parish, an official says.",
            "Raging California wildfire threatens Lake Tahoe, prompts evacuations",
            "At Least One Person Is Dead As Ida Leaves A Million People Without Power In Louisiana",
            "Pace of US evacuation flights from Afghanistan slowing one day before Biden's deadline: officials",
        ]

        # Act
        results = get_best_keywords(input)

        # Assert
        self.assertEqual(results, "without power")

    def test_get_lead_headlines__given_other_headlines__then_best_returned(self):
        # Arrange
        input = [
            "Families forced to queue for hours at Heathrow border control",
            "Canada election: Will declining consumer confidence hurt Trudeau?",
            "Texas ‘freedom defender’ who rallied against COVID-19 measures dies",
            "Ida now a tropical storm as more than 1 million Louisiana utility customers are left without power",
            "As The Lake Tahoe Wildfire Spreads, Everyone On The California Side Is Told To Leave",
            "Haiti Quake Turned Baptism Celebration Into Tragedy",
            "In New Orleans and beyond, evacuations are underway.",
            "Live: 'Covid's C.1.2 variant may be more infectious, evade vaccine protection'",
            "Authorities conduct search-and-rescue efforts in Ida's aftermath. 'The worst-case scenario seems to have happened' in Jefferson Parish, an official says.",
            "Raging California wildfire threatens Lake Tahoe, prompts evacuations",
            "At Least One Person Is Dead As Ida Leaves A Million People Without Power In Louisiana",
            "Pace of US evacuation flights from Afghanistan slowing one day before Biden's deadline: officials",
        ]

        # Act
        results = get_lead_headlines(input)
        print(results)

        # Assert
        self.assertEqual(
            results,
            [
                "Ida now a tropical storm as more than 1 million Louisiana utility customers are left without power",
                "At Least One Person Is Dead As Ida Leaves A Million People Without Power In Louisiana",
            ],
        )

    def test_get_lead_headlines_md__given_headlines__then_md_is_correct(self):
        # Arrange

        # Act
        results = get_lead_headlines_md(
            datetime.now(),
            "hurricane ida",
            ["Hurricante Ida is really bad", "Who is impacted by Hurricane Ida."],
        )
        print(f"test results: {results}")

        # Assert
        self.assertTrue('title: "Lead Headlines"' in results)


if __name__ == "__main__":
    unittest.main()
