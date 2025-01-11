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

@app.route("/log_x_post", methods=["POST"])
def webhook():
    # Get data from Twilio's webhook
    print(request.form)

    # # Verify the message is from your number
    # if sender == MY_PHONE_NUMBER:
    #     # Forward the message to the API
    #     response = requests.post(
    #         FORWARDING_API_URL,
    #         json={"message": message_body},
    #         headers={"Authorization": f"Bearer {FORWARDING_API_KEY}"}
    #     )
    #     if response.status_code == 200:
    #         return jsonify({"status": "success"}), 200
    #     else:
    #         return jsonify({"status": "error", "details": response.text}), 500

    # # Ignore messages from other numbers
    # return jsonify({"status": "ignored"}), 403
    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    # Run the Flask application
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))