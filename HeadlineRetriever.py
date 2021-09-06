from dataclasses import dataclass
from datetime import date, timedelta
from typing import List

import requests
import wayback
from bs4 import BeautifulSoup
from retry import retry


@dataclass(frozen=True)
class Headline:
    date: date
    url: str
    headline: str


class HeadlineRetriever:
    def __init__(self, urls: List[str] = []):
        self.NEWS_URLS = [
            "https://www.npr.org/sections/news",
            "https://www.washingtontimes.com",
            "https://www.cnn.com",
            "https://www.foxnews.com",
            "https://www.msn.com",
            "https://news.google.com",
        ]
        self.urls = self.NEWS_URLS
        if urls:
            self.urls = urls
        self.client = wayback.WaybackClient()
        pass

    @retry(tries=3, backoff=1)
    def __download_page(self, url):
        print(f"\t{url}")
        res = requests.get(url)
        return res

    def get_headlines(self, **kwargs) -> List[Headline]:
        today = date.today()
        start_date = kwargs.get("start_date", today)
        day_after_start = start_date + timedelta(days=1)
        end_date = kwargs.get("end_date", day_after_start)
        print(f"{start_date} -> {end_date}")

        days_between = (end_date - start_date).days
        for day in range(0, days_between):
            from_date = start_date + timedelta(days=day)
            daily_headlines = []
            for url in self.urls:
                url_to_download = url
                if start_date != today:
                    results = self.client.search(
                        url=url,
                        from_date=from_date,
                        to_date=from_date + timedelta(days=day + 1),
                    )
                    try:
                        record = next(results)
                        url_to_download = record.raw_url
                    except StopIteration as e:
                        continue
                res = self.__download_page(url_to_download)
                html = res.text
                soup = BeautifulSoup(html, features="html.parser")
                links = soup.find_all("a")
                cleaned_links = [l for l in links if "Read the transcript" not in l]
                for l in cleaned_links:
                    link_text = l.text.replace("\n", "").replace("\t", "")
                    link_text = link_text.strip()
                    try:
                        link_url = l["href"]
                    except KeyError:
                        continue
                    if self.include_headline(link_text, link_url):
                        if link_url.startswith("./"):
                            link_url = link_url[2:]
                            link_url = f"{url_to_download}/{link_url}"
                        headline = Headline(from_date, link_url, link_text)
                        daily_headlines.append(headline)

        return daily_headlines

    def include_headline(self, link_text, link_url) -> bool:
        if len(link_text.split(" ")) <= 5:
            return False
        if "video.foxnews" in link_url:
            return False
        return True
