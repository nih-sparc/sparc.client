import json
from pennsieve2 import Pennsieve

from sparc.client.services.pennsieve import PennsieveService


def test_connect_no_profile(mocker):
    expected = None
    mocker.patch("pennsieve2.Pennsieve.connect")
    p = PennsieveService(connect=False)
    pennsieve = p.connect()
    actual = pennsieve.get_user()
    assert actual == expected


def test_connect_false_with_profile(mocker, mock_user, mock_pennsieve):
    expected = "profile"
    mocker.patch("pennsieve2.Pennsieve.connect")
    mocker.patch("pennsieve2.Pennsieve.get_user", mock_user.get_user)
    mock_user.set_user("profile")
    p = PennsieveService(connect=False, config={"pennsieve_profile_name": "profile"})
    pennsieve = p.connect()
    actual = pennsieve.get_user()
    assert actual == expected


def test_connect_true_with_profile(mocker, mock_user, mock_pennsieve):
    expected = "test version"
    mocker.patch("pennsieve2.Pennsieve.connect", mock_pennsieve.connect)
    mocker.patch("pennsieve2.Pennsieve.agent_version", mock_pennsieve.agent_version)
    mocker.patch("pennsieve2.Pennsieve.get_user", mock_user.get_user)
    mock_user.set_user("profile")
    p = PennsieveService(connect=True, config={"pennsieve_profile_name": "profile"})
    pennsieve = p.connect()
    assert pennsieve is not None
    assert pennsieve.get_user() == "profile"
    assert pennsieve.agent_version() == expected


def test_get_profile(mocker, mock_pennsieve, mock_user):
    expected = "user"
    mocker.patch("pennsieve2.Pennsieve.get_user", mock_user.get_user)
    mock_user.set_user("user")

    p = PennsieveService(connect=False)
    actual = p.get_profile()
    assert actual == expected


def test_set_profile(mocker, mock_pennsieve):
    expected = "new user"
    mocker.patch("pennsieve2.Pennsieve.switch", mock_pennsieve.switch)

    class Manifest:
        manifest = "manifest"

        def __init__(self):
            pass

    p = PennsieveService(connect=False)
    p.manifest = Manifest()
    actual = p.set_profile("new user")
    assert expected == actual


def test_info(mocker, mock_pennsieve):
    expected = "test version"
    mocker.patch("pennsieve2.Pennsieve.agent_version", mock_pennsieve.agent_version)
    p = PennsieveService(connect=False)
    actual = p.info()
    assert expected == actual


def test_closed(mocker, mock_pennsieve):
    expected = "closed"
    mocker.patch("pennsieve2.Pennsieve.stop", mock_pennsieve.close)
    p = PennsieveService(connect=False)
    actual = p.close()
    assert expected == actual


def test_list_datasets(mocker, mock_pennsieve):
    expected = {
        "limit": 1,
        "offset": 0,
        "totalCount": 1,
        "datasets": [
            {
                "id": 2,
                "sourceDatasetId": 3,
                "name": "dataset",
                "description": "description",
                "ownerId": 4,
                "ownerFirstName": "John",
                "ownerLastName": "Smith",
                "ownerOrcid": "0000-0000-0000-0000",
                "organizationName": "organization",
                "organizationId": 1,
                "license": "license",
                "tags": ["tag1", "tag2"],
                "version": 5,
                "revision": None,
                "size": 6,
                "modelCount": [{"modelName": "model", "count": 0}],
                "fileCount": 1,
                "recordCount": 1,
                "uri": "s3://pennsieve/1/1/",
                "arn": "arn:aws:s3:::pennsieve/1/1/",
                "status": "PUBLISH_SUCCEEDED",
                "doi": "10.00000/abc123",
                "banner": "https://pennsieve/banner",
                "readme": "https://pennsieve/dataset-assets/1/1/readme.md",
                "contributors": [
                    {
                        "firstName": "John",
                        "middleInitial": None,
                        "lastName": "Smith",
                        "degree": None,
                        "orcid": "0000-0000-0000-0000",
                    }
                ],
                "collections": [{"id": 1, "name": "name"}],
                "externalPublications": [
                    {"doi": "10.0000/protocols.xx", "relationshipType": "IsSupplementedBy"}
                ],
                "sponsorship": {
                    "title": "title",
                    "imageUrl": "https://imageurl",
                    "markup": "markup",
                },
                "pennsieveSchemaVersion": "4.0",
                "createdAt": "2000-12-12",
                "updatedAt": "2000-12-12",
                "firstPublishedAt": "2000-12-12",
                "versionPublishedAt": "2000-12-12",
                "revisedAt": None,
                "embargo": False,
                "embargoReleaseDate": None,
                "embargoAccess": None,
            }
        ],
    }
    mocker.patch("pennsieve2.Pennsieve.get", mock_pennsieve.list_datasets)
    p = PennsieveService(connect=False)
    actual = p.list_datasets()
    assert expected == actual


def test_list_files(mocker, mock_pennsieve):
    expected = [
        {
            "name": "This is the filename.txt",
            "datasetId": 1,
            "datasetVersion": 1,
            "size": 1,
            "fileType": "TXT",
            "packageType": "package",
            "icon": "Icon",
            "uri": "s3://pennsieve/a/b/a.txt",
            "createdAt": None,
            "sourcePackageId": "N:package:aaaaaa",
        }
    ]
    mocker.patch("pennsieve2.Pennsieve.get", mock_pennsieve.list_files)
    p = PennsieveService(connect=False)
    actual = p.list_files()
    assert expected == actual


def test_list_filenames(mocker, mock_pennsieve):
    expected = ["a.txt"]
    mocker.patch("pennsieve2.Pennsieve.get", mock_pennsieve.list_files)
    p = PennsieveService(connect=False)
    actual = p.list_filenames({"uri": "http://pennsieve.io/dataset/file"})
    assert expected == actual


def test_list_records(mocker, mock_pennsieve):
    expected = {
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
                    "id": "aaaaaaa-aaaa-aaaa-aaaaaa",
                },
            }
        ],
    }

    mocker.patch("pennsieve2.Pennsieve.get", mock_pennsieve.list_records)
    p = PennsieveService(connect=False)
    actual = p.list_records()
    assert expected == actual


def test_download(mocker, mock_pennsieve):
    file_list = [
        {
            "name": "manifest.json",
            "datasetId": 1,
            "datasetVersion": 1,
            "size": 10000,
            "fileType": "Json",
            "packageType": "Unsupported",
            "icon": "JSON",
            "uri": "s3://pennsieve/1/2/manifest.json",
            "createdAt": None,
            "sourcePackageId": None,
        }
    ]

    class PennsieveResponse:
        status_code = 200
        content = b'{"content" : "content}'

    def response(url=None, json=None, headers=None):
        return PennsieveResponse()

    mocker.patch("requests.post", response)
    mocker.patch("os.open")
    mocker.patch("os.write")

    p = PennsieveService(connect=False)
    response = p.download_file(file_list=file_list)
    assert response.status_code == 200

    response = p.download_file(file_list=file_list, output_name="test")
    assert response.status_code == 200


def test_download_multiple(mocker, mock_pennsieve):
    file_list = [
        {
            "name": "manifest.json",
            "datasetId": 1,
            "datasetVersion": 1,
            "size": 10000,
            "fileType": "Json",
            "packageType": "Unsupported",
            "icon": "JSON",
            "uri": "s3://pennsieve/1/2/manifest.json",
            "createdAt": None,
            "sourcePackageId": None,
        },
        {
            "name": "manifest2.json",
            "datasetId": 1,
            "datasetVersion": 1,
            "size": 20000,
            "fileType": "Json",
            "packageType": "Unsupported",
            "icon": "JSON",
            "uri": "s3://pennsieve/1/2/manifest2.json",
            "createdAt": None,
            "sourcePackageId": None,
        },
    ]

    class PennsieveResponse:
        status_code = 200
        content = b'{"content" : "content}'

    def response(url=None, json=None, headers=None):
        return PennsieveResponse()

    mocker.patch("requests.post", response)
    mocker.patch("os.open")
    mocker.patch("os.write")

    p = PennsieveService(connect=False)
    response = p.download_file(file_list=file_list)
    assert response.status_code == 200

    response = p.download_file(file_list=file_list, output_name="test")
    assert response.status_code == 200
