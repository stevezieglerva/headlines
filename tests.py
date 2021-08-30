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

    def test_get_lead_headlines__given_no_tie__then_highest_returned(self):
        # Arrange
        input = [
            "hurricane ida slams lousiana",
            "hurricane ida",
            "covid surge hitting the south",
        ]

        # Act
        subject = LeadHeadlines(input)

        # Assert
        self.assertEqual(subject.best_keywords, "hurricane ida")
        self.assertEqual(
            subject.lead_headlines, ["hurricane ida slams lousiana", "hurricane ida"]
        )

    def test_get_lead_headlines__given_no_tie__then_highest_returned(self):
        # Arrange
        input = [
            "hurricane ida slams lousiana",
            "hurricane ida",
            "covid surge hitting the south",
            "covid surge",
        ]

        # Act
        subject = LeadHeadlines(input)

        # Assert
        self.assertEqual(subject.best_keywords, "covid surge")
        self.assertEqual(
            subject.lead_headlines,
            [
                "covid surge hitting the south",
                "covid surge",
            ],
        )

    # def test_get_top_gram__given_tie__then_highest_returned(self):
    #     # Arrange
    #     input = [
    #         "hurricane ida slams lousiana",
    #         "hurricane ida",
    #         "covid surge",
    #         "covid surge hitting the south",
    #     ]

    #     # Act
    #     results = get_top_gram(input, 2)

    #     # Assert
    #     self.assertEqual(results, (2, "covid surge"))

    # def test_ngrams__given_headline__then_ngrams_returned_without_stop_words_and_punctuation(
    #     self,
    # ):
    #     # Arrange
    #     input = "Hurricane Ida has really strong winds!"

    #     # Act
    #     results = ngrams(input, 3)
    #     print(results)

    #     # Assert
    #     self.assertEqual(
    #         results,
    #         ["hurricane ida really", "ida really strong", "really strong winds"],
    #     )

    # def test_get_best_keywords__given_headlines__then_best_returned(self):
    #     # Arrange
    #     input = [
    #         "Families forced to queue for hours at Heathrow border control",
    #         "Canada election: Will declining consumer confidence hurt Trudeau?",
    #         "Texas ‘freedom defender’ who rallied against COVID-19 measures dies",
    #         "Ida now a tropical storm as more than 1 million Louisiana utility customers are left without power",
    #         "As The Lake Tahoe Wildfire Spreads, Everyone On The California Side Is Told To Leave",
    #         "Haiti Quake Turned Baptism Celebration Into Tragedy",
    #         "In New Orleans and beyond, evacuations are underway.",
    #         "Live: 'Covid's C.1.2 variant may be more infectious, evade vaccine protection'",
    #         "Authorities conduct search-and-rescue efforts in Ida's aftermath. 'The worst-case scenario seems to have happened' in Jefferson Parish, an official says.",
    #         "Raging California wildfire threatens Lake Tahoe, prompts evacuations",
    #         "Ida now a tropical storm",
    #         "Ida now a tropical storm",
    #     ]

    #     # Act
    #     results = get_best_keywords(input)

    #     # Assert
    #     self.assertEqual(results, "ida now tropical")

    # def test_get_best_keywords__given_other_headlines__then_best_returned(self):
    #     # Arrange
    #     input = [
    #         "Families forced to queue for hours at Heathrow border control",
    #         "Canada election: Will declining consumer confidence hurt Trudeau?",
    #         "Texas ‘freedom defender’ who rallied against COVID-19 measures dies",
    #         "Ida now a tropical storm as more than 1 million Louisiana utility customers are left without power",
    #         "As The Lake Tahoe Wildfire Spreads, Everyone On The California Side Is Told To Leave",
    #         "Haiti Quake Turned Baptism Celebration Into Tragedy",
    #         "In New Orleans and beyond, evacuations are underway.",
    #         "Live: 'Covid's C.1.2 variant may be more infectious, evade vaccine protection'",
    #         "Authorities conduct search-and-rescue efforts in Ida's aftermath. 'The worst-case scenario seems to have happened' in Jefferson Parish, an official says.",
    #         "Raging California wildfire threatens Lake Tahoe, prompts evacuations",
    #         "At Least One Person Is Dead As Ida Leaves A Million People Without Power In Louisiana",
    #         "Pace of US evacuation flights from Afghanistan slowing one day before Biden's deadline: officials",
    #     ]

    #     # Act
    #     results = get_best_keywords(input)

    #     # Assert
    #     self.assertEqual(results, "lake tahoe")

    # def test_get_best_keywords__given_tie_in_headlines__then_lowest_alpha_returned(
    #     self,
    # ):
    #     # Arrange
    #     input = [
    #         "hurricane ida slams lousiana",
    #         "hurricane ida",
    #         "covid surge",
    #         "covid surge hitting the south",
    #     ]

    #     # Act
    #     results = get_best_keywords(input)

    #     # Assert
    #     self.assertEqual(results, "covid surge")

    # def test_get_lead_headlines__given_other_headlines__then_best_returned(self):
    #     # Arrange
    #     input = [
    #         "Families forced to queue for hours at Heathrow border control",
    #         "Canada election: Will declining consumer confidence hurt Trudeau?",
    #         "Texas ‘freedom defender’ who rallied against COVID-19 measures dies",
    #         "Ida now a tropical storm as more than 1 million Louisiana utility customers are left without power",
    #         "As The Lake Tahoe Wildfire Spreads, Everyone On The California Side Is Told To Leave",
    #         "Haiti Quake Turned Baptism Celebration Into Tragedy",
    #         "In New Orleans and beyond, evacuations are underway.",
    #         "Live: 'Covid's C.1.2 variant may be more infectious, evade vaccine protection'",
    #         "Authorities conduct search-and-rescue efforts in Ida's aftermath. 'The worst-case scenario seems to have happened' in Jefferson Parish, an official says.",
    #         "Raging California wildfire threatens Lake Tahoe, prompts evacuations",
    #         "At Least One Person Is Dead As Ida Leaves A Million People Without Power In Louisiana",
    #         "Pace of US evacuation flights from Afghanistan slowing one day before Biden's deadline: officials",
    #     ]

    #     # Act
    #     results = get_lead_headlines(input)
    #     print(results)

    #     # Assert
    #     self.assertEqual(
    #         results,
    #         [
    #             "As The Lake Tahoe Wildfire Spreads, Everyone On The California Side Is Told To Leave",
    #             "Raging California wildfire threatens Lake Tahoe, prompts evacuations",
    #         ],
    #     )

    # def test_get_lead_headlines__given_google_headlines__then_best_returned(self):
    #     # Arrange
    #     input = [
    #         "At Least One Person Is Dead As Ida Leaves A Million People Without Power In Louisiana",
    #         "Ida pummels Louisiana: Live updates",
    #         "New Orleans Without Power As Ida Moves North",
    #         "WATCH LIVE: Non-stop coverage of Ida’s aftermath in Louisiana",
    #         "Ida: At least 1 dead, more than a million customers without power in Louisiana",
    #         "US intercepts rockets targeting Kabul airport as key diplomats fly out",
    #         "As many as 5 rockets were fired on Kabul airport, says US official",
    #         "Unvaccinated U.S. Visitors Could Face New Restrictions on Travel to Europe",
    #         "EU to recommend reinstating Covid-related travel restrictions on US, reports say",
    #         "Hospital patients are being evacuated as the rapidly growing Caldor Fire edges closer to California's Lake Tahoe region",
    #         "South Lake Tahoe Wildfire: California Side's Residents Warned To Leave",
    #         "Taliban offered Kabul to U.S., but Americans said no: report",
    #         "The Tale of California’s Recall Election",
    #         "Why Aren’t Democrats Talking About the Worst Possible Outcome of the California Recall?",
    #         "New COVID variant detected in South Africa, most mutated variant so far",
    #         "New South African COVID-19 strain is the most mutated one yet: report",
    #         "Ed Asner, Emmy-Winning Star of ‘Lou Grant’ and ‘Up,’ Dies at 91",
    #         "Ed Asner, acclaimed 'Mary Tyler Moore Show' actor, dies at 91",
    #         "Vaccine Refusers Don't Get to Dictate Terms Anymore",
    #         "Hurricane Ida Reversed the Course of the Mississippi River",
    #         "Hurricane Ida knocks out power in all of New Orleans | DW News",
    #         "Sirhan Sirhan: Robert Kennedy’s oldest son condemns killer’s possible parole",
    #         "Chad Daybell's children defend their father, say he was 'framed'",
    #         "Sneak peek: The Secrets of Chad Daybell's Backyard",
    #         "Critics slam WaPo column for blaming crisis in Afghanistan on American people",
    #         "McConnell: ‘Why we went’ to Afghanistan has been lost",
    #         "Israel doubles down on booster shots as daily Covid cases set new record",
    #         "This is how to prevent another 100,000 Covid deaths by December, Fauci says",
    #         "After death threats from a far-right group, Russian restaurant pulls ad featuring Black man",
    #         "Border policeman dies from Gaza riot shooting injury",
    #         "Coronavirus booster shots 'not a luxury', WHO Europe head says",
    #         "The Taliban's education minister says it will allow Afghan women to attend university, but mixed gender classes will be banned",
    #         "Afghanistan: UK sceptical of Taliban safe passage pledge, says minister",
    #         "NC Coronavirus update August 30: Wake County Public School System updates COVID 19 protocols as cases increase in NC",
    #         "Durham mayor says city is ready to welcome Afghan refugees",
    #         "What is Theranos founder Elizabeth Holmes on trial for?",
    #         "Treasury yields fall slightly as investors await key jobs report",
    #         "Boeing 777s, which had engine blow apart after takeoff, grounded until 2022",
    #         "Gas prices dodge Hurricane Ida catastrophe",
    #         "Ida closes Colonial Pipeline, gas prices expected to rise",
    #         "Galaxy S10, Galaxy S20, Galaxy Note 10, and Galaxy Note 20 get One UI 3.1.1 updates",
    #         "One UI 4 allegedly draws near with the sighting of a Galaxy S21 Ultra on new software",
    #         "Notebookcheck.net",
    #         "Steve Cohen weighs in on Mets’ ‘thumbs-down’ gestures",
    #         "Mets fans booed their team during its freefall, and now the players are returning the favor",
    #     ]

    #     # Act
    #     results = get_lead_headlines(input)
    #     print(results)

    #     # Assert
    #     self.assertEqual(
    #         results,
    #         [
    #             "Hurricane Ida Reversed the Course of the Mississippi River",
    #             "Hurricane Ida knocks out power in all of New Orleans | DW News",
    #             "Gas prices dodge Hurricane Ida catastrophe",
    #         ],
    #     )

    # def test_get_lead_headlines_md__given_headlines__then_md_is_correct(self):
    #     # Arrange

    #     # Act
    #     results = get_lead_headlines_md(
    #         datetime.now(),
    #         "hurricane ida",
    #         ["Hurricante Ida is really bad", "Who is impacted by Hurricane Ida."],
    #     )
    #     print(f"test results: {results}")

    #     # Assert
    #     self.assertTrue("Lead headlines for 'hurricane ida'" in results)


if __name__ == "__main__":
    unittest.main()
