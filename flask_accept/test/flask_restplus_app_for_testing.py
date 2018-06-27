from flask import Flask, jsonify
from flask_restplus import Resource
from flask_restplus import Api

from flask_accept import accept, accept_fallback

app = Flask(__name__)
app.debug = True
api = Api(app)


class PlusResourceWithoutDoc(Resource):
    @accept('application/vnd.vendor.v1+json')
    def get(self):
        return jsonify(version='v1')

    @get.support(
        'application/json',
        'application/vnd.vendor+json',
        'application/vnd.vendor.v2+json')
    def get_v2(self):
        return jsonify(version='v2')


class PlusResourceWithDoc(Resource):
    @accept('application/vnd.vendor.v1+json')
    def get(self):
        """
            The doc string of GET /plus/with-doc
        """
        return jsonify(version='v1')

    @get.support(
        'application/json',
        'application/vnd.vendor+json',
        'application/vnd.vendor.v2+json')
    def get_v2(self):
        return jsonify(version='v2')


class PlusResourceWithoutFallback(Resource):
    @accept('application/vnd.vendor.v1+json')
    def get(self):
        return jsonify(version='v1')

    @get.support(
        'application/json',
        'application/vnd.vendor+json',
        'application/vnd.vendor.v2+json')
    def get_v2(self):
        return jsonify(version='v2')


class PlusResourceWithFallback(Resource):
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


api.add_resource(PlusResourceWithoutFallback, '/plus/without-fallback')
api.add_resource(PlusResourceWithFallback, '/plus/with-fallback')
api.add_resource(PlusResourceWithoutDoc, '/plus/without-doc')
api.add_resource(PlusResourceWithDoc, '/plus/with-doc')
