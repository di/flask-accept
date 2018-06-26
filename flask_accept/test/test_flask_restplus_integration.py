import json

import pytest

from app_for_testing import app


@pytest.mark.parametrize('uri,doc', [
    ('/plus/with-doc', 'The doc string of GET /plus/with-doc'),
    ('/plus/without-doc', None)
])
def test_flask_restplus_swagger_document(uri, doc):
    with app.test_client() as c:
        rv = c.get('/swagger.json')
        swagger = json.loads(rv.data.decode())
        assert swagger['paths'][uri]['get'].get('summary') == doc
