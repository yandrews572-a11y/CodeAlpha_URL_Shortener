import os
import shortuuid
import validators

from flask import Flask, jsonify, request, redirect, render_template
from dotenv import load_dotenv

from models import create_url, get_url, increment_click


# Load environment variables
load_dotenv()


# Create Flask app
app = Flask(__name__)


# -----------------------------------
# HOME / FRONTEND
# -----------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------------
# CREATE SHORT URL
# -----------------------------------

@app.route("/shorten", methods=["POST"])
def shorten():

    data = request.get_json()

    # Check request body
    if not data or "url" not in data:
        return jsonify({
            "error": "URL is required"
        }), 400

    long_url = data["url"]

    # Validate URL
    if not validators.url(long_url):
        return jsonify({
            "error": "Invalid URL"
        }), 400

    # -----------------------------------
    # CUSTOM ALIAS
    # -----------------------------------

    custom_alias = data.get("custom_alias")

    if custom_alias:

        # Remove unwanted spaces
        custom_alias = custom_alias.strip()

        # Check alias already exists
        existing = get_url(custom_alias)

        if existing:
            return jsonify({
                "error": "Custom alias already exists"
            }), 409

        short_code = custom_alias

    else:

        # Generate random short code
        short_code = shortuuid.uuid()[:6]


    # -----------------------------------
    # EXPIRY
    # -----------------------------------

    expires_in_days = data.get("expires_in_days")

    if expires_in_days:

        try:
            expires_in_days = int(expires_in_days)

        except (ValueError, TypeError):

            return jsonify({
                "error": "expires_in_days must be a number"
            }), 400

        if expires_in_days <= 0:

            return jsonify({
                "error": "expires_in_days must be greater than 0"
            }), 400

    else:
        expires_in_days = None


    # -----------------------------------
    # SAVE TO DATABASE
    # -----------------------------------

    saved = create_url(
        long_url,
        short_code,
        expires_in_days
    )


    # -----------------------------------
    # CREATE LIVE SHORT URL
    # -----------------------------------

    base_url = os.getenv(
        "BASE_URL",
        "http://127.0.0.1:5000"
    )

    short_url = f"{base_url}/{saved['short_code']}"


    # -----------------------------------
    # RESPONSE
    # -----------------------------------

    response = {
        "short_url": short_url,
        "short_code": saved["short_code"]
    }

    # Include expiry if available
    if saved.get("expires_at"):
        response["expires_at"] = saved["expires_at"]

    return jsonify(response), 200


# -----------------------------------
# REDIRECT SHORT URL
# -----------------------------------

@app.route("/<short_code>")
def redirect_url(short_code):

    print("SHORT CODE RECEIVED:", short_code)

    # Find URL in MongoDB
    url = get_url(short_code)

    print("DATABASE RESULT:", url)

    # URL doesn't exist
    if not url:
        return "URL Not Found", 404

    # -----------------------------------
    # CHECK EXPIRY
    # -----------------------------------

    if url.get("expires_at"):

        from datetime import datetime

        expires_at = url["expires_at"]

        if datetime.utcnow() > expires_at:

            return jsonify({
                "error": "This short URL has expired"
            }), 410


    # -----------------------------------
    # INCREMENT CLICKS
    # -----------------------------------

    increment_click(short_code)


    # -----------------------------------
    # REDIRECT
    # -----------------------------------

    return redirect(url["long_url"])


# -----------------------------------
# RUN APPLICATION
# -----------------------------------

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )