Flask-Accept
============

.. image:: https://travis-ci.org/di/flask-accept.svg?branch=master
    :target: https://travis-ci.org/di/flask-accept

Description
-----------

Custom ``Accept`` header routing support for Flask.

Features
--------

**Respond differently based on the MIME type accepted**
  Extend any given endpoint to support any additional media type.

**Use custom media types to version your API**
  Never put a ``/v1/`` in your URI ever again.

**Dead-simple API**
  Yet Another Flask Decorator.

Documentation
-------------

Installation
~~~~~~~~~~~~

Installing:

::

    $ pip install flask-accept

Quickstart
~~~~~~~~~~

Below is an example Flask app that only accepts the ``text/html`` media type:

.. code:: python

    from flask import Flask
    from flask_accept import accept
    app = Flask(__name__)

    @app.route('/')
    @accept('text/html')
    def hello_world():
        return 'Hello World!'

    if __name__ == '__main__':
        app.run()

When one tries to access the endpoint without a valid ``Accept`` header:

.. code:: console

    $ curl localhost:5000 -I
    HTTP/1.0 406 NOT ACCEPTABLE

With the valid header:

.. code:: console

    $ curl localhost:5000 -I -H "Accept: text/html"
    HTTP/1.0 200 OK
    Content-Type: text/html; charset=utf-8

Adding Support for an Existing Endpoint
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Given our example from before, we can add support for a different response to
an additonal media type as follows:

.. code:: python

    from flask import Flask, jsonify
    from flask_accept import accept
    app = Flask(__name__)

    @app.route('/')
    @accept('text/html')
    def hello_world():
        return 'Hello World!'

    @hello_world.support('application/json')
    def hello_world_json():
        return jsonify(result="Hello World!")

    if __name__ == '__main__':
        app.run()

Now our ``hello_world`` endpoint supports JSON:

.. code:: console

    $ curl localhost:5000 -I -H "Accept: application/json"
    HTTP/1.0 200 OK
    Content-Type: application/json

Falling Back on a Default Endpoint
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If we want to support a specific media type, but have every other request
fall back to a default endpoint, we can use ``accept_fallback`` as follows:

.. code:: python

    from flask import Flask, jsonify
    from flask_accept import accept, accept_fallback
    app = Flask(__name__)

    @app.route('/')
    @accept_fallback
    def hello_world():
        return 'Hello World!'

    @hello_world.support('application/json')
    def hello_world_json():
        return jsonify(result="Hello World!")

    if __name__ == '__main__':
        app.run()

Our ``hello_world`` endpoint still supports JSON, but for any other media type
(or if none is specified) it will fall back:

.. code:: console

   $ curl localhost:5000 -I
   HTTP/1.0 200 OK
   Content-Type: text/html

   $ curl localhost:5000 -I -H "Accept: madeup/mediatype"
   HTTP/1.0 200 OK
   Content-Type: text/html

Use Cases
~~~~~~~~~

Some possible use cases for Flask-Accept.

Versioning your API
^^^^^^^^^^^^^^^^^^^

Flask-Accept let you accept any possible media type, including `custom vendored
media types <https://en.wikipedia.org/wiki/Media_type#Vendor_tree>`_. This is
ideal for versioning an API using ``Accept`` headers only:

.. code:: python

    from flask import Flask, jsonify
    from flask_accept import accept
    app = Flask(__name__)

    @app.route('/')
    @accept('application/vnd.your_vendor.v1', 'application/vnd.your_vendor.v2')
    def hello_world():
        return 'Hello World!'

    @hello_world.support('application/vnd.your_vendor.v3')
    def hello_world_v2():
        return 'Goodbye cruel world.'

    if __name__ == '__main__':
        app.run()

.. code:: console

    $ curl localhost:5000 -H "Accept: application/vnd.your_vendor.v1"
    Hello World!

    $ curl localhost:5000 -H "Accept: application/vnd.your_vendor.v2"
    Hello World!

    $ curl localhost:5000 -H "Accept: application/vnd.your_vendor.v3"
    Goodbye cruel world.

Works with Flask-RESTful Resources
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The same functionality can be applied to APIs built with Flask-RESTful

.. code:: python

    from flask import Flask, jsonify
    from flask_accept import accept
    from flask_restful import Resource, Api
    app = Flask(__name__)
    api = Api(app)


    class HelloWorldResource(Resource):
        @accept('application/vnd.your_vendor.v1', 'application/vnd.your_vendor.v2')
        def get():
            return 'Hello World!'

        @get.support('application/vnd.your_vendor.v3')
        def get_v2():
            return 'Goodbye cruel world.'


    api.add_resource(HelloWorldResource, '/')

    if __name__ == '__main__':
        app.run()

.. code:: console

    $ curl localhost:5000 -H "Accept: application/vnd.your_vendor.v1"
    Hello World!

    $ curl localhost:5000 -H "Accept: application/vnd.your_vendor.v2"
    Hello World!

    $ curl localhost:5000 -H "Accept: application/vnd.your_vendor.v3"
    Goodbye cruel world.


Testing
~~~~~~~

To run the tests

::

    python setup.py test

Authors
-------

-  `Dustin Ingram <https://github.com/di>`_
-  `Patrick Smith <https://github.com/patricksmith>`_

License
-------

Open source MIT license.
