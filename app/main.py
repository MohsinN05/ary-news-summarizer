from flask import Flask, request, jsonify

from app.scraper import search_news, NEWS_SOURCE
from app.summarizer import summarize_article

app = Flask(__name__)

REGISTRATION = "FA23-BDS-021"


@app.route("/", methods=["GET"])
def home():
    return f"""
    <html>
        <head>
            <title>News Summarizer API</title>
        </head>
        <body>
            <h1>News Summarizer API</h1>
            <h2>Registration Number: {REGISTRATION}</h2>
            <p>News Source: {NEWS_SOURCE}</p>
            <p>API Endpoint: /get?keyword=your_keyword</p>
        </body>
    </html>
    """


@app.route("/get", methods=["GET"])
def get_news():
    keyword = request.args.get("keyword", "").strip()

    if not keyword:
        return jsonify({
            "error": "Please provide a keyword"
        }), 400

    try:
        article = search_news(keyword)

        summary = summarize_article(
            article["content"],
            sentence_count=5
        )

        return jsonify({
            "registration": REGISTRATION,
            "newssource": NEWS_SOURCE,
            "keyword": keyword,
            "url": article["url"],
            "summary": summary
        })

    except Exception as error:
        app.logger.exception("News processing failed")

        return jsonify({
            "error": "Unable to process the requested news article",
            "details": str(error)
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=7000,
        debug=False
    )
