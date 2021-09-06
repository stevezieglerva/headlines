import functools
import heapq
import json
import re
from dataclasses import dataclass
from typing import List

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
    "s",
    "says",
    "can",
    "us",
    "day",
    "man",
    "woman",
    "charge",
    "cnn",
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december",
    "by",
]

REPLACEMENT_WORDS = {
    "U.S.": "USA",
    "D.C.": "DC",
    "Related Article:": "",
    "View »": "",
    '"': "",
    "Year's": "Years",
    "Political cartoon of the day": "",
    "White House": "",
    "Today's mortgage refinance": "",
    "Social media": "",
}


@dataclass(frozen=True)
class GramFrequency:
    gram: str
    frequency: float

    @classmethod
    def create_from_tuple(cls, gram_tuple: tuple):
        return cls(gram_tuple[1], gram_tuple[0])


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


class LeadHeadlines:
    def __init__(
        self, headlines: List[str], percentage_threshold: float = 0.01
    ) -> None:
        self.prep_to_raw_mapping = self.__prep_data(headlines)
        prepped_headlines = [h for h in self.prep_to_raw_mapping.keys()]

        self.__top_gram1_raw = self.__get_top_grams_for_headlines(prepped_headlines, 1)
        self.__top_gram2_raw = self.__get_top_grams_for_headlines(prepped_headlines, 2)
        self.__top_gram3_raw = self.__get_top_grams_for_headlines(prepped_headlines, 3)

        gram_1_percentages = [
            (
                self.__get_percentage_of_headlines_with_gram(prepped_headlines, g[1]),
                g[1],
            )
            for g in self.__top_gram1_raw.values
        ]
        self.gram1_sorted = sorted(gram_1_percentages, reverse=True)

        gram_2_percentages = [
            (
                self.__get_percentage_of_headlines_with_gram(prepped_headlines, g[1]),
                g[1],
            )
            for g in self.__top_gram2_raw.values
        ]
        self.gram2_sorted = sorted(gram_2_percentages, reverse=True)

        gram_3_percentages = [
            (
                self.__get_percentage_of_headlines_with_gram(prepped_headlines, g[1]),
                g[1],
            )
            for g in self.__top_gram3_raw.values
        ]
        self.gram3_sorted = sorted(gram_3_percentages, reverse=True)

        grams = self.gram2_sorted.copy()
        grams.extend(self.gram3_sorted)
        self.grams_sorted = sorted(grams, reverse=True)
        best_frequency = GramFrequency.create_from_tuple(self.grams_sorted[0])
        self.best_keywords = ""
        self.lead_headlines = []
        self.headline_percentage = 0
        if best_frequency.frequency > percentage_threshold:
            self.best_keywords = best_frequency.gram
            self.headline_percentage = best_frequency.frequency
            self.lead_headlines = self.__get_lead_headlines(self.best_keywords)

    def __get_percentage_of_headlines_with_gram(self, prepped_headlines, gram):
        # print(f"\ngram: '{gram}'")
        headlines_with_gram = [h for h in prepped_headlines if gram in h]
        headlines_with_gram = {}

        words = gram.split(" ")
        for headline in prepped_headlines:
            if gram in headline:
                headlines_with_gram[headline] = headlines_with_gram.get(headline, 0) + 1
                # print(f"\tfound '{gram}'' in '{headline}'")
            else:
                words = gram.split(" ")
                if len(words) == 3:
                    left = " ".join(words[0:2])
                    right = " ".join(words[1:3])
                    if left in headline or right in headline:
                        headlines_with_gram[headline] = (
                            headlines_with_gram.get(headline, 0) + 1
                        )
                        # print(f"\tfound partial '{gram}'' in '{headline}'")

        found_count = len(headlines_with_gram.keys())
        total_count = len(prepped_headlines)
        # print(f"\t\t{found_count} / {total_count}")
        return round(float(found_count / total_count), 2)

    def __str__(self):
        best_gram1 = GramFrequency.create_from_tuple(self.gram1_sorted[0])
        return f"best_keywords: '{self.best_keywords:<50}' {self.headline_percentage:.0%} headlines ('{best_gram1.gram}' is {best_gram1.frequency:.0%}')"

    def __repr__(self):
        return f"""best_keywords: {self.best_keywords} ({self.headline_percentage:.0%})

lead_headlines: {self.lead_headlines[0:3]} ...
headline count: {len(self.prep_to_raw_mapping)}

top 1-grams: {self.gram1_sorted}
top 2-grams: {self.gram2_sorted}
top 3-grams: {self.gram3_sorted}
"""

    def __prep_data(self, raw_headlines: List[str]) -> dict:
        prep_to_raw_mapping = {}
        for raw_headline in raw_headlines:
            for w in REPLACEMENT_WORDS:
                raw_headline = raw_headline.replace(w, REPLACEMENT_WORDS[w])
            input_list = raw_headline.split(" ")
            input_list_lower = [w.lower().strip() for w in input_list]
            # if "year" in input_list_lower:
            #    print(input_list_lower)
            input_remove_words = input_list_lower
            # for w in input_list_lower:
            #     if w in REPLACEMENT_WORDS:
            #         print(f"{w} -> {REPLACEMENT_WORDS[w]}")
            #         input_remove_words.append(REPLACEMENT_WORDS[w])
            #     else:
            #         input_remove_words.append(w)
            input_no_stop_words = [w for w in input_remove_words if w not in STOP_WORDS]
            # input_no_possessives = [w.replace("'s", "s") for w in input_no_stop_words]
            input_no_punc = [
                re.sub(r"[^a-zA-Z0-9 -']", "", w) for w in input_no_stop_words
            ]
            input_no_numbers = [
                w for w in input_no_punc if not re.match(r"^ *[0-9]+ *$", w)
            ]
            input_trim = [w.strip() for w in input_no_numbers]
            input_no_empty = [w for w in input_trim if w != ""]
            input_line = " ".join(input_no_empty)
            prep_to_raw_mapping[input_line] = raw_headline
        return prep_to_raw_mapping

    def __ngrams(self, input, n) -> List[str]:
        input_to_process = input.split(" ")
        input_to_process_without_blanks = [
            w for w in input_to_process if w.strip() != ""
        ]
        output = []
        for i in range(len(input_to_process_without_blanks) - n + 1):
            output.append(input_to_process[i : i + n])

        output_no_blanks = [x for x in output if " ".join(x).strip() != ""]
        if n == 1:
            return [x[0] for x in output_no_blanks]
        return [" ".join(x).strip() for x in output_no_blanks]

    def __get_top_grams_for_headlines(self, headlines, gram_length):
        top_gram = TopX(3)
        counts_gram = {}
        for i in headlines:
            results = self.__ngrams(i, gram_length)
            for gram in results:
                counts_gram[gram] = counts_gram.get(gram, 0) + 1
        for k, v in counts_gram.items():
            item = (v, k)
            top_gram.add(item)
        return top_gram

    def __get_top_gram(self, headlines: list, gram_length: int) -> GramFrequency:

        top_gram = self.__get_top_grams_for_headlines(headlines, gram_length)
        best_gram = top_gram.values[0]
        # top_frequency = top_gram.values[0][0]
        # ties = [gram for gram in top_gram.values if gram[0] == top_frequency]
        # if len(ties) > 1:
        #     ties.sort(key=lambda x: x[1])
        #     best_gram = ties[0]

        gram_frequency = GramFrequency.create_from_tuple(best_gram)
        return gram_frequency

    def __get_best_keywords(self, headlines: list):

        top_gram1 = self.__get_top_gram(headlines, 1)
        top_gram2 = self.__get_top_gram(headlines, 2)
        top_gram3 = self.__get_top_gram(headlines, 3)

        # one max hit not enough for a lead
        if top_gram2.frequency == 1 and top_gram3.frequency == 1:
            self.reason = "No clear winner"
            return ""

        # 3-gram better than 2-gram
        if top_gram3.frequency >= top_gram2.frequency:
            self.reason = "Clear 3-gram winner"
            return top_gram3.gram

        # if 2-gram in a good 3-gram return 3-gram for more context
        if top_gram2.gram in top_gram3.gram and top_gram3.frequency > 1:
            self.reason = "Use 3-gram with best 2-gram for improved context"
            return top_gram3.gram
        self.reason = "Best available 2-gram"
        return top_gram2.gram

    def __get_lead_headlines(self, best_gram: str):
        return [
            raw
            for prepped, raw in self.prep_to_raw_mapping.items()
            if best_gram in prepped
        ]
