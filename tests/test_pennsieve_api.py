import json

import pytest
import requests
import responses
from requests.exceptions import HTTPError

from sparc.client.services import PennsieveService


@responses.activate
def test_register_responses():

    responses.add(
        method=responses.GET,
        url="http://api.pennsieve.io/datasets/",
        content_type="application/json",
        json={"key": "value"},
        status=200,
    )

    responses.add(
        method=responses.POST,
        url="http://api.pennsieve.io/datasets/1/versions/1/files/download-manifest",
        content_type="application/json",
        json={"key2": "value2"},
        status=200,
    )

    responses.add(
        method=responses.PUT,
        url="http://api.pennsieve.io/whatever",
        content_type="application/json",
        json={"key3": "value3"},
        status=200,
    )

    responses.add(
        method=responses.DELETE,
        url="http://api.pennsieve.io/whatever",
        content_type="application/json",
        json={"key4": "value4"},
        status=200,
    )

    p = PennsieveService(config={"pennsieve_profile_name": "test"}, connect=False)
    resp = p.get("http://api.pennsieve.io/datasets/")
    assert resp == {"key": "value"}

    resp = p.post(
        "http://api.pennsieve.io/datasets/1/versions/1/files/download-manifest",
        json=json.dumps({"datasetId": 1}),
    )
    assert resp == {"key2": "value2"}

    resp = p.put("http://api.pennsieve.io/whatever", json=json.dumps({"datasetId": 0}))
    assert resp == {"key3": "value3"}

    resp = p.delete("http://api.pennsieve.io/whatever", json=json.dumps({"datasetId": 0}))
    assert resp == {"key4": "value4"}
