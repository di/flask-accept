import json

import pytest

from app_for_testing import app, index_without_fallback


@pytest.mark.parametrize('headers,status_code,version', [
    ('text/html', 200, 'v0'),
    ('*/*', 200, 'v0'),
    ('application/vnd.vendor.v1+json', 200, 'v1'),
    ('application/json', 200, 'v2'),
    ('application/json, text/html', 200, 'v2'),
    ('application/vnd.vendor+json', 200, 'v2'),
    ('application/vnd.vendor.v2+json', 200, 'v2'),
])
def test_with_fallback(headers, status_code, version):
    with app.test_client() as c:
        rv = c.get('/with-fallback', headers={'accept': headers})
        assert rv.status_code == status_code
        if rv.status_code < 300:
            assert version == json.loads(rv.data.decode())['version']


@pytest.mark.parametrize('headers,status_code,version', [
    ('text/html', 406, None),
    ('*/*', 406, None),
    ('application/vnd.vendor.v1+json', 200, 'v1'),
    ('application/json', 200, 'v2'),
    ('application/json, text/html', 200, 'v2'),
    ('application/vnd.vendor+json', 200, 'v2'),
    ('application/vnd.vendor.v2+json', 200, 'v2'),
])
def test_without_fallback(headers, status_code, version):
    with app.test_client() as c:
        rv = c.get('/without-fallback', headers={'accept': headers})
        assert rv.status_code == status_code
        if rv.status_code < 300:
            assert version == json.loads(rv.data.decode())['version']
        else:
            for accepted_type in index_without_fallback.accept_handlers:
                assert accepted_type in rv.data.decode()


@pytest.mark.parametrize('headers,status_code,rh', [
    ('*/*', 406, None),
    ('text/html', 200, 'text/*'),
    ('text/*', 200, 'text/*'),
    ('application/*', 200, 'application/*'),
    ('application/json', 200, 'application/*'),
])
def test_with_wildcard(headers, status_code, rh):
    with app.test_client() as c:
        rv = c.get('/with-wildcard', headers={'accept': headers})
        if rv.status_code < 300:
            assert rh == json.loads(rv.data.decode())['rh']


@pytest.mark.parametrize('headers,status_code,rh', [
    ('*/*', 200, '*/*'),
    ('text/html', 200, '*/*'),
    ('text/*', 200, '*/*'),
    ('application/*', 200, '*/*'),
    ('application/json', 200, '*/*'),
])
def test_with_double_wildcard(headers, status_code, rh):
    with app.test_client() as c:
        rv = c.get('/with-double-wildcard', headers={'accept': headers})
        if rv.status_code < 300:
            assert rh == json.loads(rv.data.decode())['rh']


@pytest.mark.parametrize('headers,status_code,version', [
    ('text/html', 200, 'v0'),
    ('*/*', 200, 'v0'),
    ('application/vnd.vendor.v1+json', 200, 'v1'),
    ('application/json', 200, 'v2'),
    ('application/json, text/html', 200, 'v2'),
    ('application/vnd.vendor+json', 200, 'v2'),
    ('application/vnd.vendor.v2+json', 200, 'v2'),
])
def test_flask_restful_resource_with_fallback(headers, status_code, version):
    with app.test_client() as c:
        rv = c.get('/resource/with-fallback', headers={'accept': headers})
        assert rv.status_code == status_code
        if rv.status_code < 300:
            assert version == json.loads(rv.data.decode())['version']


@pytest.mark.parametrize('headers,status_code,version', [
    ('text/html', 406, None),
    ('*/*', 406, None),
    ('application/vnd.vendor.v1+json', 200, 'v1'),
    ('application/json', 200, 'v2'),
    ('application/json, text/html', 200, 'v2'),
    ('application/vnd.vendor+json', 200, 'v2'),
    ('application/vnd.vendor.v2+json', 200, 'v2'),
])
def test_flask_restful_resource_without_fallback(headers,
                                                 status_code,
                                                 version):
    with app.test_client() as c:
        rv = c.get('/resource/without-fallback', headers={'accept': headers})
        assert rv.status_code == status_code
        if rv.status_code < 300:
            assert version == json.loads(rv.data.decode())['version']
        else:
            for accepted_type in index_without_fallback.accept_handlers:
                assert accepted_type in rv.data.decode()


@pytest.mark.parametrize('headers,status_code,version', [
    ('text/html', 200, 'v0'),
    ('*/*', 200, 'v0'),
    ('application/vnd.vendor.v1+json', 200, 'v1'),
    ('application/json', 200, 'v2'),
    ('application/json, text/html', 200, 'v2'),
    ('application/vnd.vendor+json', 200, 'v2'),
    ('application/vnd.vendor.v2+json', 200, 'v2'),
])
def test_flask_restplus_resource_with_fallback(headers, status_code, version):
    with app.test_client() as c:
        rv = c.get('/plus/with-fallback', headers={'accept': headers})
        assert rv.status_code == status_code
        if rv.status_code < 300:
            assert version == json.loads(rv.data.decode())['version']


@pytest.mark.parametrize('headers,status_code,version', [
    ('text/html', 406, None),
    ('*/*', 406, None),
    ('application/vnd.vendor.v1+json', 200, 'v1'),
    ('application/json', 200, 'v2'),
    ('application/json, text/html', 200, 'v2'),
    ('application/vnd.vendor+json', 200, 'v2'),
    ('application/vnd.vendor.v2+json', 200, 'v2'),
])
def test_flask_restplus_resource_without_fallback(headers,
                                                  status_code,
                                                  version):
    with app.test_client() as c:
        rv = c.get('/plus/without-fallback', headers={'accept': headers})
        assert rv.status_code == status_code
        if rv.status_code < 300:
            assert version == json.loads(rv.data.decode())['version']
        else:
            for accepted_type in index_without_fallback.accept_handlers:
                assert accepted_type in rv.data.decode()


@pytest.mark.parametrize('uri,doc', [
    ('/plus/with-fallback', 'The doc string of GET /plus/with-fallback'),
    ('/plus/without-fallback', 'The doc string of GET /plus/without-fallback')
])
def test_flask_restplus_swagger_document(uri, doc):
    with app.test_client() as c:
        rv = c.get('/swagger.json')
        swagger = json.loads(rv.data.decode())
        assert swagger['paths'][uri]['get']['summary'] == doc
