import json
import os

from sparc.client import SparcClient

import pytest


test_dir = os.path.dirname(__file__)
config_dir = os.path.join(test_dir, "resources")
config_file = os.path.join(config_dir, "config.ini")


client = SparcClient(connect=False, config_file = config_file)


# Test connect and initialization
def test_metadata_connect():
    response = client.metadata.connect()

    assert response == "https://api.scicrunch.io/elastic/v1"


# Test getting info
def test_metadata_info():
    response = client.metadata.info()

    assert response == "https://api.scicrunch.io/elastic/v1"


# Test list datasets with no API key
def test_metadata_list_datasets_nokey():
    response = {}

    response = client.metadata.list_datasets()

    if bool(response):
        assert 0
    else:
        assert 1


# Test list datasets utilizing alternate non-api key endpoint
def test_metadata_list_datasets():
    response = {}

    client.metadata.algolia_api = "https://api.pennsieve.io/discover/datasets"
    response = client.metadata.list_datasets()

    assert response['totalCount'] > 0 


# Test search with query string with no API key
def test_metadata_search_string_nokey():
    query_string = "{\"query\": {\"terms\": {\"_id\": [ \"136\", \"95\" ] } } }"
    response = {}

    response = client.metadata.search_datasets(query_string)
    
    if bool(response):
        assert 0
    else:
        assert 1


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

# Test list datasets utilizing alternate non-api key endpoint
def test_metadata_list_datasets_badurl():
    response = {}

    client.metadata.algolia_api = "https://api.scicrunch.io/elastic/v0"
    response = client.metadata.list_datasets()

    if bool(response):
        assert 0
    else:
        assert 1


# Test config operations for API key
def test_metadata_api_key():
    set_result = client.metadata.set_profile(api_key = "Test Key")
    assert set_result == "Test Key"
        
    get_result = client.metadata.get_profile()
    assert get_result == "Test Key"


# Test close
def test_metadata_close():
    close_result = client.metadata.close()
    assert close_result == "https://api.scicrunch.io/elastic/v1"

# Test get URL with no headers
def test_metadata_get_noheader():
    get_result = client.metadata.getURL("https://api.scicrunch.io/elastic/v1/SPARC_Algolia_pr/_search", headers="NONE")

    if bool(get_result):
        assert 0
    else:
        assert 1

# Test post URL with no headers
def test_metadata_post_noheader():
    body = "{\"query\": {\"terms\": {\"_id\": [ \"136\", \"95\" ] } } }"
    body_json = json.loads(body)

    post_result = client.metadata.postURL("https://api.scicrunch.io/elastic/v1/SPARC_Algolia_pr/_search", body_json, headers="NONE")

    if bool(post_result):
        assert 0
    else:
        assert 1