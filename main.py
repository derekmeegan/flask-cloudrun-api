import os
import asyncio
from crawl4ai import AsyncWebCrawler
from flask import Flask, request, jsonify

app = Flask(__name__)

# Define the asynchronous crawling logic
async def crawl_crypto_news():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://crypto.news",
        )
        return result.markdown

# Flask route for the HTTP request
@app.route("/crawl", methods=["GET"])
def crawl():
    # Run the asynchronous function and return the response
    result = asyncio.run(crawl_crypto_news())
    return jsonify({"data": result})

@app.route("/test", methods=["GET"])
def test():
    return jsonify({"result": 'hello'})

if __name__ == "__main__":
    # Run the Flask application
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

    

