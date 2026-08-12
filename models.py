from datetime import datetime, timedelta, timezone

from config import urls_collection


def create_url(long_url, short_code, expires_in_days=None):

    expires_at = None

    if expires_in_days:
        expires_at = datetime.now(timezone.utc) + timedelta(
            days=expires_in_days
        )

    data = {
        "long_url": long_url,
        "short_code": short_code,
        "clicks": 0,
        "created_at": datetime.now(timezone.utc),
        "expires_at": expires_at
    }

    urls_collection.insert_one(data)

    return data


def get_url(short_code):

    return urls_collection.find_one({
        "short_code": short_code
    })


def increment_click(short_code):

    urls_collection.update_one(
        {
            "short_code": short_code
        },
        {
            "$inc": {
                "clicks": 1
            }
        }
    )