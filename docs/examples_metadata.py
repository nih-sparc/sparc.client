# Set of example call to the metadata services within the SPARC client
# Make sure to get an API key and add to your config/config.ini file
# Add key to the scicrunch_api_key attribute
# Instructions for getting an API key can be found at: https://fdilab.gitbook.io/api-handbook/sparc-k-core-api-overview/getting-started-with-sparc-apis

import json
from sparc.client import SparcClient

client = SparcClient(connect=False, config_file='../config/config.ini')

# Connect
response = client.metadata.connect()

if response == "https://scicrunch.org/api/1/elastic":
    test_pass = True
else:
    test_pass = False

print( str(test_pass) )

# Get Info
response = client.metadata.info()

if response == "https://scicrunch.org/api/1/elastic":
    test_pass = True
else:
    test_pass = False

print( str(test_pass) )

# ES list datasets
response = {}
response = client.metadata.list_datasets()

check_response = response['hits']['total']
if check_response > 200:
    test_pass = True
else:
    test_pass = False

print( str(test_pass) )

# ES search via default
response = {}
response = client.metadata.search_datasets()

check_response = response['hits']['total']
if check_response > 200:
    test_pass = True
else:
    test_pass = False

print( str(test_pass) )

# ES search via JSON string
response = {}
response = client.metadata.search_datasets("{\"query\": {\"terms\": {\"_id\": [ \"136\", \"95\" ] } } }")

check_response = response['hits']['total']
if check_response == 2:
    test_pass = True
else:
    test_pass = False

print( str(test_pass) )

# ES search via JSON object
response = {}
body = "{\"query\": {\"terms\": {\"_id\": [ \"136\", \"95\" ] } } }"
body_json = json.loads(body)

response = client.metadata.search_datasets(body_json)

check_response = response['hits']['total']
if check_response == 2:
    test_pass = True
else:
    test_pass = False

print( str(test_pass) )
