import json
import random

import pytest

from app_for_testing import app


@pytest.mark.parametrize("headers,expected", [
    (['text/plain;format=flowed', 'text/plain', 'text/*', '*/*'], 'text/plain;format=flowed'),
    (['text/plain', 'text/*', '*/*'], 'text/plain'),
    (['text/*', '*/*'], 'text/*'),
    (['*/*'], '*/*'),
])
def test_precedence(headers, expected):
    with app.test_client() as c:
        random.shuffle(headers)
        header_string = ", ".join(headers)
        resp = c.get('/precedence', headers={'accept': header_string})
    assert resp.headers['Content-Type'] == expected
