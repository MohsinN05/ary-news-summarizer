
import time
from urllib.parse import quote_plus, urlparse

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


NEWS_SOURCE = "ARY News Pakistan"
BASE_URL = "https://arynews.tv"


def create_driver():
    options = Options()
    options.binary_location = "/usr/bin/chromium"
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    return webdriver.Chrome(options=options)


def search_news(keyword):
    driver = create_driver()

    try:
        search_url = (
            f"{BASE_URL}/?s={quote_plus(keyword)}"
        )

        driver.get(search_url)

        WebDriverWait(driver, 20).until(
            lambda d: d.execute_script(
                "return document.readyState"
            ) == "complete"
        )

        time.sleep(3)

        soup = BeautifulSoup(
            driver.page_source, "lxml"
        )

        article = None

        for link in soup.select("a[href]"):
            href = link.get("href", "")
            title = link.get_text(" ", strip=True)

            if not href or not title:
                continue

            parsed = urlparse(href)

            if (
                parsed.hostname
                and parsed.hostname.endswith("arynews.tv")
                and parsed.path not in ("", "/")
                and not any(
                    x in parsed.path.lower()
                    for x in [
                        "/category/",
                        "/tag/",
                        "/author/",
                        "/wp-content/"
                    ]
                )
            ):
                article = {
                    "title": title,
                    "url": href
                }
                break

        if not article:
            raise Exception(
                "No article found for this keyword"
            )

        driver.get(article["url"])

        WebDriverWait(driver, 20).until(
            lambda d: d.execute_script(
                "return document.readyState"
            ) == "complete"
        )

        time.sleep(2)

        article_soup = BeautifulSoup(
            driver.page_source, "lxml"
        )

        title_tag = article_soup.find("h1")
        title = (
            title_tag.get_text(" ", strip=True)
            if title_tag else article["title"]
        )

        content = article_soup.select_one(
            "article"
        )

        if not content:
            content = article_soup.body

        paragraphs = []

        if content:
            for paragraph in content.find_all("p"):
                text = paragraph.get_text(
                    " ", strip=True
                )

                if len(text) > 40:
                    paragraphs.append(text)

        article_text = "\n".join(paragraphs)

        if not article_text:
            raise Exception(
                "Could not extract article content"
            )

        return {
            "title": title,
            "url": article["url"],
            "content": article_text
        }

    finally:
        driver.quit()
