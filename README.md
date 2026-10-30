# ARY News Summarizer API

A Docker-based news scraping and summarization application developed
for CSC418 - DevOps for Cloud Computing.

## Student Information

- Name: Mohsin Nadeem
- Registration Number: FA23-BDS-021
- News Source: ARY News Pakistan

## Technologies

- Python
- Flask
- Selenium
- Chromium
- BeautifulSoup
- Sumy (LexRank)
- Docker

## Features

- Searches ARY News using a keyword.
- Extracts the first matching news article.
- Retrieves the article content.
- Generates an automatic summary.
- Provides results through a REST API.

## API

### Homepage

GET /

Displays the project information and registration number.

### Search and Summarize

GET /get?keyword=Pakistan

Example response:

```json
{
  "registration": "FA23-BDS-021",
  "newssource": "ARY News Pakistan",
  "keyword": "Pakistan",
  "url": "ARTICLE_URL",
  "summary": "Generated article summary."
}
