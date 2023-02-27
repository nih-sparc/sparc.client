import json
import os

import pytest
from pennsieve2 import Pennsieve


@pytest.fixture(scope="session")
def test_dir():
    return os.path.dirname(__file__)


@pytest.fixture(scope="session")
def test_resources_dir(test_dir):
    return os.path.join(test_dir, "resources")


@pytest.fixture(scope="session")
def config_file(test_resources_dir):
    return os.path.join(test_resources_dir, "config.ini")


@pytest.fixture
def mock_user():
    class MockPennsieveUser:
        profile_name = None

        def __init__(self):
            self.profile_name = "user"

        def get_user(self):
            return self.profile_name

        def set_user(self, profile_name):
            self.profile_name = profile_name

    return MockPennsieveUser()


@pytest.fixture
def mock_pennsieve():
    class MockPennsieve(Pennsieve):
        default_headers = "headers"
        profile_name = None
        manifest = None

        def __init__(self, config=None, connect=True) -> None:
            if config is not None:
                self.profile_name = config.get("pennsieve_profile_name")
            if connect:
                self.connect()

        def connect(self, profile_name=None):
            return "connected"

        def agent_version(self) -> str:
            return "test version"

        def get_user(self):
            return self.profile_name

        def get_profile(self) -> str:
            return self.user.whoami()

        def switch(self, profile_name):
            class Manifest:
                manifest = "manifest"

                def __init__(self):
                    pass

            self.profile_name = profile_name
            self.manifest = Manifest()
            return self.profile_name

        def close(self):
            return "closed"

        def get(self, url, **kwargs):
            return "get"

        def post(self, url, json, **kwargs):
            return "post"

        def put(self, url, json, **kwargs):
            return "put"

        def delete(self, url, **kwargs):
            return "delete"

        def list_datasets(self, url=None, headers=None, params=None):
            return json.loads(
                """{"limit":1,"offset":0,"totalCount":1,"datasets":[{"id":2,"sourceDatasetId":3,"name":"dataset",
                    "description":"description","ownerId":4,"ownerFirstName":"John","ownerLastName":"Smith",
                    "ownerOrcid":"0000-0000-0000-0000","organizationName":"organization","organizationId":1,
                    "license":"license","tags":["tag1","tag2"],"version":5,"revision":null,"size":6,
                    "modelCount":[{"modelName":"model","count":0}],
                    "fileCount":1,"recordCount":1,"uri":"s3://pennsieve/1/1/",
                    "arn":"arn:aws:s3:::pennsieve/1/1/","status":"PUBLISH_SUCCEEDED",
                    "doi":"10.00000/abc123","banner":"https://pennsieve/banner","readme":"https://pennsieve/dataset-assets/1/1/readme.md",
                    "contributors":[{"firstName":"John","middleInitial":null,"lastName":"Smith","degree":null,
                    "orcid":"0000-0000-0000-0000"}],"collections":[{"id":1,"name":"name"}],
                    "externalPublications":[{"doi":"10.0000/protocols.xx","relationshipType":"IsSupplementedBy"}],
                    "sponsorship":{"title":"title","imageUrl":"https://imageurl","markup":"markup"},
                    "pennsieveSchemaVersion":"4.0","createdAt":"2000-12-12","updatedAt":"2000-12-12",
                    "firstPublishedAt":"2000-12-12","versionPublishedAt":"2000-12-12",
                    "revisedAt":null,"embargo":false,"embargoReleaseDate":null,"embargoAccess":null}]}"""
            )

        def list_files(self, url=None, headers=None, params=None):
            return json.loads(
                """{
                "limit": 1,
                "offset": 0,
                "totalCount": 10000,
                "files": [
                    {
                      "name": "This is the filename.txt",
                      "datasetId": 1,
                      "datasetVersion": 1,
                      "size": 1,
                      "fileType": "TXT",
                      "packageType": "package",
                      "icon": "Icon",
                      "uri": "s3://pennsieve/a/b/a.txt",
                      "createdAt": null,
                      "sourcePackageId": "N:package:aaaaaa"
                    }]
                }"""
            )

        def list_records(self, url=None, headers=None, params=None):
            return json.loads(
                """{
                  "limit": 10,
                  "offset": 0,
                  "totalCount": 10000,
                  "records": [
                    {
                      "datasetId": 1,
                      "version": 3,
                      "model": "researcher",
                      "properties": {
                        "hasORCIDId": "https://orcid.org/0000-0000-0000-0000",
                        "hasAffiliation": "UPenn",
                        "middleName": "A",
                        "hasRole": "",
                        "lastName": "Smith",
                        "firstName": "John",
                        "id": "aaaaaaa-aaaa-aaaa-aaaaaa"
                          }
                }]}"""
            )

        def download_file(self, file_list=None, output_name=None):
            return "downloaded"

    return MockPennsieve()
