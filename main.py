import re
import os
import asyncio
from crawl4ai import AsyncWebCrawler
from flask import Flask, request, jsonify
from google.cloud import pubsub_v1

def parse_x_url(url):
    pattern = r"https:\/\/x\.com\/(?P<username>[\w]+)\/status\/(?P<id>\d+)"
    match = re.search(pattern, url)
    if match:
        username = match.group("username")
        id = match.group("id")
        return username, id
    return None, None

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
        print(f"Message received: {message}")
        return "Your messaged was received by your creator.", 200

    return 'No message was provided in query string.', 400

@app.route("/test", methods=["GET"])
def test():
    return jsonify({"result": 'hello'})

@app.route("/log_x_post", methods=["POST"])
def twilio_webhook():
    data = request.form
    sender = data.get('From')
    content = data.get('Body').strip()

    # # Verify the message is from your number
    if sender == '+16615930925':
        username, post_id = parse_x_url(content)
        print(username)
        print(post_id)
        if username and post_id:
            publisher = pubsub_v1.PublisherClient()
            topic_path = publisher.topic_path('hallowed-ridge-447322-d1', 'x-post-lookup')
            
            message = {
                "username": username,
                "post_id": post_id,
            }
            publisher.publish(topic_path, data=str(message).encode('utf-8'))
            return f"Post from {username} with ID {post_id} logged.", 200
    return "Invalid sender or content.", 400

if __name__ == "__main__":
    # Run the Flask application
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))