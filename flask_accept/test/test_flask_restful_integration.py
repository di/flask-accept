import json

import pytest

from flask_restful_app_for_testing import app


@pytest.mark.parametrize(
    "headers,status_code,version",
    [
        ("text/html", 200, "v0"),
        ("*/*", 200, "v0"),
        ("application/vnd.vendor.v1+json", 200, "v1"),
        ("application/json", 200, "v2"),
        ("application/json, text/html", 200, "v2"),
        ("application/vnd.vendor+json", 200, "v2"),
        ("application/vnd.vendor.v2+json", 200, "v2"),
    ],
)
def test_flask_restful_resource_with_fallback(headers, status_code, version):
    with app.test_client() as c:
        rv = c.get("/resource/with-fallback", headers={"accept": headers})
        assert rv.status_code == status_code
        if rv.status_code < 300:
            assert version == json.loads(rv.data.decode())["version"]


@pytest.mark.parametrize(
    "headers,status_code,version",
    [
        ("text/html", 406, None),
        ("*/*", 406, None),
        ("application/vnd.vendor.v1+json", 200, "v1"),
        ("application/json", 200, "v2"),
        ("application/json, text/html", 200, "v2"),
        ("application/vnd.vendor+json", 200, "v2"),
        ("application/vnd.vendor.v2+json", 200, "v2"),
    ],
)
def test_flask_restful_resource_without_fallback(headers, status_code, version):
    with app.test_client() as c:
        rv = c.get("/resource/without-fallback", headers={"accept": headers})
        assert rv.status_code == status_code
        if rv.status_code < 300:
            assert version == json.loads(rv.data.decode())["version"]
        else:
            for accepted_type in (
                "application/json",
                "application/vnd.vendor.v1+json",
                "application/vnd.vendor+json",
                "application/vnd.vendor.v2+json",
            ):
                assert accepted_type in rv.data.decode()
