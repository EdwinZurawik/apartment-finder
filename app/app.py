import multiprocessing
import os

import flatty
from dotenv import load_dotenv
from flask import (
    Flask,
    abort,
    request,
)

load_dotenv()

app = Flask(__name__)


@app.route("/")
def index():
    return "Hello World!"


@app.route("/get_offers", methods=["POST"])
def get_offers():
    content_type = request.headers.get("Content-Type")
    if content_type == "application/json":
        content = request.get_json()
        if (
            "api_key" in content.keys()
            and content["api_key"] == os.environ["FLASK_API_KEY"]
        ):
            city = content.get("city")
            if city:
                multiprocessing.Process(
                    target=scrape_and_save_offers, args=(city,)
                ).start()
                return "Processing request...", 201
            return abort(400, "No city specified")
        else:
            abort(401, "Not Authenticated!")
    abort(400, "Content-Type not supported!")


def scrape_and_save_offers(city: str) -> None:
    offers_list = flatty.get_offers_for_city(city)
    flatty.update_offers(offers_list)
