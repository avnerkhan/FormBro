from flask import Flask, request
from enum import Enum
from util import read_and_load, write_to_file
from DatabaseAPI import DatabaseAPI as DB
import urllib.request as request_url

app = Flask(__name__)


class APIFields(Enum):
    URL = "URL"
    CLASS = "CLASS"


json_urls = read_and_load("urls.json")
db = DB("PULLUPS", "pullups")


@app.route('/get_unclassified_image_url', methods=["GET"])
def get_unclassified_image_url() -> str:
    if not json_urls:
        return "No more unclassified URLS to read from."
    return json_urls.pop()


@app.route("/persist_json", methods=["POST"])
def persist_json() -> bool:
    try:
        write_to_file("urls.json", json_urls)
        return True
    except:
        print("Error occured when trying to persist JSON")
        return False


@app.route("/save_picture_with_class", methods=["POST"])
def save_picture_with_class() -> bool:
    try:
        json_request = request.get_json()
        url = json_request[APIFields.URL]
        class_type = json_request[APIFields.CLASS]
        remote_picture = request_url.Request(url)
        temp_f = request_url.urlopen(remote_picture)
        db.insert_into_table(url, int(class_type), temp_f.read())
        return True
    except:
        print("Error in saving picture")
        return False


if __name__ == '__main__':
    json_urls = read_and_load("urls.json")
    app.run()
