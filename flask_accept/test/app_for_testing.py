from flask import Flask, jsonify
from flask_restful import Resource, Api
from flask_restplus import Resource as PlusResource
from flask_restplus import Api as PlusApi

from flask_accept import accept, accept_fallback

app = Flask(__name__)
app.debug = True
# flask_restful api
api = Api(app)

# flask_restplus api
plus_api = PlusApi(app)


@app.route('/with-fallback')
@accept_fallback
def index_with_fallback():
    return jsonify(version='v0')


@index_with_fallback.support('application/vnd.vendor.v1+json')
def index_with_fallback_v1():
    return jsonify(version='v1')


@index_with_fallback.support(
    'application/json',
    'application/vnd.vendor+json',
    'application/vnd.vendor.v2+json')
def index_with_fallback_v2():
    return jsonify(version='v2')


@app.route('/without-fallback')
@accept('application/vnd.vendor.v1+json')
def index_without_fallback():
    return jsonify(version='v1')


@index_without_fallback.support(
    'application/json',
    'application/vnd.vendor+json',
    'application/vnd.vendor.v2+json')
def index_without_fallback_v2():
    return jsonify(version='v2')


@app.route('/with-wildcard')
@accept('application/*')
def index_with_wildcard():
    return jsonify(rh='application/*')


@index_with_wildcard.support('text/*')
def index_with_wildcard_text():
    return jsonify(rh='text/*')


@app.route('/with-double-wildcard')
@accept('*/*')
def index_with_double_wildcard():
    return jsonify(rh='*/*')


# Routes set up with flask_restful
class IndexResourceWithoutFallback(Resource):
    @accept('application/vnd.vendor.v1+json')
    def get(self):
        return jsonify(version='v1')

    @get.support(
        'application/json',
        'application/vnd.vendor+json',
        'application/vnd.vendor.v2+json')
    def get_v2(self):
        return jsonify(version='v2')


class IndexResourceWithFallback(Resource):
    @accept_fallback
    def get(self):
        return jsonify(version='v0')

    @get.support('application/vnd.vendor.v1+json')
    def get_v1(self):
        return jsonify(version='v1')

    @get.support(
        'application/json',
        'application/vnd.vendor+json',
        'application/vnd.vendor.v2+json')
    def get_v2(self):
        return jsonify(version='v2')


api.add_resource(IndexResourceWithoutFallback, '/resource/without-fallback')
api.add_resource(IndexResourceWithFallback, '/resource/with-fallback')


# Routes set up with flask_restplus
class PlusIndexResourceWithoutFallback(PlusResource):
    @accept('application/vnd.vendor.v1+json')
    def get(self):
        """
            The doc string of GET /plus/without-fallback
        """
        return jsonify(version='v1')

    @get.support(
        'application/json',
        'application/vnd.vendor+json',
        'application/vnd.vendor.v2+json')
    def get_v2(self):
        return jsonify(version='v2')


class PlusIndexResourceWithFallback(PlusResource):
    @accept_fallback
    def get(self):
        """
            The doc string of GET /plus/with-fallback
        """
        return jsonify(version='v0')

    @get.support('application/vnd.vendor.v1+json')
    def get_v1(self):
        return jsonify(version='v1')

    @get.support(
        'application/json',
        'application/vnd.vendor+json',
        'application/vnd.vendor.v2+json')
    def get_v2(self):
        return jsonify(version='v2')


plus_api.add_resource(PlusIndexResourceWithoutFallback, '/plus/without-fallback')
plus_api.add_resource(PlusIndexResourceWithFallback, '/plus/with-fallback')
