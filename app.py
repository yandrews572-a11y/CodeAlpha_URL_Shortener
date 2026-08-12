from datetime import datetime, timezone

from flask import Flask, jsonify, redirect, render_template, request
import shortuuid
import validators

from models import create_url, get_url, increment_click


app = Flask(__name__)


# Home
@app.route("/")
def home():
    return render_template("index.html")


# Create Short URL
@app.route("/shorten", methods=["POST"])
def shorten():

    data = request.get_json()

    # Check URL field
    if not data or "url" not in data:
        return jsonify({
            "error": "URL is required"
        }), 400

    long_url = data["url"]

    # URL validation
    if not validators.url(long_url):
        return jsonify({
            "error": "Invalid URL"
        }), 400

    # Custom alias or random code
    custom_alias = data.get("custom_alias")

    if custom_alias:

        # Check whether alias already exists
        existing = get_url(custom_alias)

        if existing:
            return jsonify({
                "error": "Custom alias already exists"
            }), 409

        short_code = custom_alias

    else:

        short_code = shortuuid.uuid()[:6]

    # URL expiry
    expires_in_days = data.get("expires_in_days")

    # Validate expiry value
    if expires_in_days is not None:

        try:
            expires_in_days = int(expires_in_days)

            if expires_in_days <= 0:
                return jsonify({
                    "error": "expires_in_days must be greater than 0"
                }), 400

        except (ValueError, TypeError):

            return jsonify({
                "error": "expires_in_days must be a number"
            }), 400

    # Save URL
    saved = create_url(
        long_url,
        short_code,
        expires_in_days
    )

    return jsonify({
        "short_url": f"http://127.0.0.1:5000/{saved['short_code']}"
    }), 201


# Redirect Short URL
@app.route("/<short_code>")
def redirect_url(short_code):

    print("SHORT CODE RECEIVED:", short_code)

    url = get_url(short_code)

    print("DATABASE RESULT:", url)

    # Short URL doesn't exist
    if not url:
        return "URL Not Found", 404

    # Check URL expiry
    expires_at = url.get("expires_at")

    if expires_at:

        # Make sure datetime is timezone-aware
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)

        if expires_at <= datetime.now(timezone.utc):

            return jsonify({
                "error": "This short URL has expired"
            }), 410

    # Increase click count
    increment_click(short_code)

    # Redirect to original URL
    return redirect(url["long_url"])


# URL Statistics
@app.route("/stats/<short_code>")
def stats(short_code):

    url = get_url(short_code)

    if not url:
        return jsonify({
            "error": "Short URL not found"
        }), 404

    expires_at = url.get("expires_at")

    return jsonify({
        "short_code": url["short_code"],
        "long_url": url["long_url"],
        "clicks": url["clicks"],
        "created_at": url["created_at"].isoformat(),
        "expires_at": expires_at.isoformat() if expires_at else None
    })


# Start Flask Server
if __name__ == "__main__":
    app.run(debug=False)