import multiprocessing
import os

from dotenv import load_dotenv
from flask import Flask, abort, request
import flatty

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
        print(os.environ["FLASK_API_KEY"])
        if (
            "api_key" in content.keys()
            and content["api_key"] == os.environ["FLASK_API_KEY"]
        ):
            city = content.get('city')
            if city:
                print(city)
                get_offers_work = multiprocessing.Process(target=flatty.get_offers_for_city,
                                                    args=(city,))
                get_offers_work.start()
                return "Processing request...", 201
            return abort(400, "No city specified")
        else:
            abort(401, "Not Authenticated!")
    abort(400, "Content-Type not supported!")
