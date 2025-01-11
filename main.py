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

@app.route("/message_creator", methods=['POST', 'GET'])
def message_creator():
    # Check for 'message' in query string
    message = request.args.get('message')
    
    # If not found in query string, check in the request body
    if not message:
        if request.is_json:  # Check if the request body is JSON
            data = request.get_json()
            message = data.get('message') if data else None
    
    if message:
        # Print the message to the console
        print(f"Message received: {message}")
        return "Your messaged was received by your creator."
    else:
        print('No message was provided by caller')

@app.route("/test", methods=["GET"])
def test():
    return jsonify({"result": 'hello'})

if __name__ == "__main__":
    # Run the Flask application
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))