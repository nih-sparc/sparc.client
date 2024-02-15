import json

from sparc.client import SparcClient

import pytest

client = SparcClient(connect=False, config_file='../config/config.ini')

# Test connect and initialization
def test_metadata_connect():
    response = client.metadata.connect()

    assert response == "https://api.scicrunch.io/elastic/v1"


# Test getting info
def test_metadata_info():
    response = client.metadata.info()

    assert response == "https://api.scicrunch.io/elastic/v1"


# Test list datasets utilizing alternate non-api key endpoint
def test_metadata_list_datasets():
    response = {}

    client.metadata.algolia_api = "https://api.pennsieve.io/discover/datasets"
    response = client.metadata.list_datasets()

    assert response['totalCount'] > 0 


# Test search with query string utilizing alternate non-api key endpoint
def test_metadata_search_string():
    query_string = "{ \"paths\": [\"banner.jpg\"] }"
    response = {}

    client.metadata.algolia_api = "https://api.pennsieve.io/discover/datasets/307/versions/1/files/download-manifest"
    response = client.metadata.search_datasets(query_string)

    assert response['header']['count'] > 0


# Test search with JSON body utilizing alternate non-api key endpoint
def test_metadata_search_body():
    body = "{ \"paths\": [\"banner.jpg\"] }"
    body_json = json.loads(body)
    response = {}

    client.metadata.algolia_api = "https://api.pennsieve.io/discover/datasets/307/versions/1/files/download-manifest"
    response = client.metadata.search_datasets(body_json)

    assert response['header']['count'] > 0
