import time

import requests
from flask import Flask, render_template, request
import json
import config

times = []
app = Flask(__name__)
app.backend = 'http://localhost:5000'


@app.route('/', methods=["GET"])
def search_gui():
    model = config.model
    return render_template('search.html', search_url="/search/term", stats_url="/stats", model=model)


@app.route('/search_admin', methods=["GET"])
def search_gui_admin():
    return render_template('search_admin.html', search_url="/search/term", stats_url="/stats")


@app.route("/search/term", methods=["POST"])
def search():
    body = json.loads(request.get_data())
    data = {
       "term": body['term'],
       "dataset": body['dataset'],
       "model": config.model,
       "size": body['size']
    }
    search_url = app.backend + "/search"
    tic = time.perf_counter()
    r = requests.request(url=search_url, json=data, method="POST")
    toc = time.perf_counter()
    times.append(float(f"{toc - tic:0.4f}"))
    print(times)
    if r.status_code > 300:
        return r.text

    return r.json(), 200


@app.route("/stats", methods=["POST"])
def stats():
    body = json.loads(request.get_data())

    data = {
        "term": body['term'],
        "dataset": "data_books",
        "model": config.model,
        "size": body['size'],
        "id": body['id'],
        "rating": body['rating']
    }

    stats_url = app.backend + "/stats"

    r = requests.request(url=stats_url, json=data, method="POST")

    if r.status_code > 300:
        return r.text

    return r.json(), 200


@app.route("/details", methods=["GET"])
def render_stats():
    return render_template('stats.html', search_url="/details/get")


@app.route("/details/get", methods=["GET"])
def analyse():
    # ToDo: build auto analyser (maybe in Backend)
    return "nothing here yet"


@app.route("/get_counter", methods=["GET"])
def get_counter():
    print("HERE")
    stats_url = app.backend + "/get_counter"
    print(stats_url)
    r = requests.request(url=stats_url, method="GET")
    print(r.text)
    if r.status_code > 300:
        return r.text

    return r.json(), 200
