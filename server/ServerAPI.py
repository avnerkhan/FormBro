import urllib.request as request_url
import sys
import os
sys.path.append(os.getcwd() + "/..")
from util import read_and_load, write_to_file
from DatabaseAPI import DatabaseAPI as DB
from enum import Enum
from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


class APIFields(Enum):
    URL = "url"
    CLASS = "class"
    USER_EMAIL = "userEmail"


json_urls = read_and_load("urls.json")
db = DB("PULLUPS", "pullups")
classified_urls = db.get_all_from_table()


@app.route("/get_classified_image_url", methods=["GET"])
def get_classified_image_url() -> any:
    if not classified_urls:
        return "No more classified URLS"
    return jsonify(classified_urls.pop())


# Our json_urls contains unclassified data
@app.route('/get_unclassified_image_url', methods=["GET"])
def get_unclassified_image_url() -> any:
    if not json_urls:
        return "No more unclassified URLS to read from."
    return jsonify(json_urls.pop())

# Rewrite our updated json_urls to the urls.json file


@app.route("/persist_json", methods=["GET"])
def persist_json() -> str:
    try:
        write_to_file("urls.json", json_urls)
        return "True"
    except:
        print("Error occured when trying to persist JSON")
        return "False"

# Save to our sqllite db


@app.route("/save_picture_with_class", methods=["POST"])
def save_picture_with_class() -> str:
    try:
        json_request = request.get_json()
        url = json_request[APIFields.URL.value]
        class_type = json_request[APIFields.CLASS.value]
        user_email = json_request[APIFields.USER_EMAIL.value]
        db.insert_into_table(user_email, url, int(class_type))
        return "True"
    except Exception as e:
        print(e)
        print("Error in saving picture")
        return "False"


if __name__ == '__main__':
    app.run()
