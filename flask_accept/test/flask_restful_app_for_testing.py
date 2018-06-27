from flask import Flask, jsonify
from flask_restful import Resource, Api

from flask_accept import accept, accept_fallback

app = Flask(__name__)
app.debug = True
api = Api(app)


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
