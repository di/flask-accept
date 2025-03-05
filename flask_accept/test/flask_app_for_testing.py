from flask import Flask, jsonify

from flask_accept import accept, accept_fallback

app = Flask(__name__)
app.debug = True


@app.route("/with-fallback")
@accept_fallback
def index_with_fallback():
    return jsonify(version="v0")


@index_with_fallback.support("application/vnd.vendor.v1+json")
def index_with_fallback_v1():
    return jsonify(version="v1")


@index_with_fallback.support(
    "application/json", "application/vnd.vendor+json", "application/vnd.vendor.v2+json"
)
def index_with_fallback_v2():
    return jsonify(version="v2")


@app.route("/without-fallback")
@accept("application/vnd.vendor.v1+json")
def index_without_fallback():
    return jsonify(version="v1")


@index_without_fallback.support(
    "application/json", "application/vnd.vendor+json", "application/vnd.vendor.v2+json"
)
def index_without_fallback_v2():
    return jsonify(version="v2")


@app.route("/with-wildcard")
@accept("application/*")
def index_with_wildcard():
    return jsonify(rh="application/*")


@index_with_wildcard.support("text/*")
def index_with_wildcard_text():
    return jsonify(rh="text/*")


@app.route("/with-double-wildcard")
@accept("*/*")
def index_with_double_wildcard():
    return jsonify(rh="*/*")
