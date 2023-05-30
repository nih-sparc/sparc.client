import logging
import os

import requests
from pennsieve2 import Pennsieve
from configparser import SectionProxy
from typing import List, Optional, Union
from ._default import ServiceBase


class PennsieveService(ServiceBase):
    """A wrapper for the Pennsieve2 library

    Parameters:
    -----------
    config : dict
        A configuration with defined profile name (pennsieve_profile_name).
    connect : bool
        Determines if Sparc Client should initiate connection with Pennsieve Agent.

    Attributes:
    -----------
    default_headers : dict
        A dictionary with headers to make HTTP requests.
    host_api : str
        A default HTTP address of the Pennsieve.
    Pennsieve : object
        A class holding st.


    Methods:
    --------
    connect()
        Establishes connection with Pennsieve Agent.
    info() -> str
        Returns the version of Pennsieve Agent.
    get_profile() -> str
        Returns the currently used profile.
    set_profile() -> str
        Changes the profile to the specified name.
    close() : None
        Closes Pennsieve Agent.
    list_datasets(...) : dict
        Returns a dictionary with datasets matching search criteria.
    list_files(...) : dict
        Returns a dictionary with datasets matching search criteria.
    list_filenames(...) : list
        Returns a dictionary with filenames stored at AWS matching search criteria.
    list_records(...) : dict
        Returns a dictionary with records matching search criteria.

    """

    default_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json; charset=utf-8",
    }

    host_api = "https://api.pennsieve.io"
    Pennsieve: Pennsieve = None
    profile_name: str = None

    def __init__(
        self, config: Optional[Union[dict, SectionProxy]] = None, connect: bool = False
    ) -> None:
        logging.info("Initializing Pennsieve...")
        logging.debug(str(config))

        self.Pennsieve = Pennsieve(connect=False)
        if config is not None:
            self.profile_name = config.get("pennsieve_profile_name")
            logging.info("Profile: " + self.profile_name)
        else:
            logging.info("Profile: none")
        if connect:
            self.connect()  # profile_name=self.profile_name)

    def connect(self) -> Pennsieve:
        """Establishes connection with Pennsieve Agent."""
        logging.info("Connecting to Pennsieve...")

        if self.profile_name is not None:
            self.Pennsieve.connect(profile_name=self.profile_name)
        else:
            self.Pennsieve.connect()
        return self.Pennsieve

    def info(self) -> str:
        """Returns the version of Pennsieve Agent."""
        return self.Pennsieve.agent_version()

    def get_profile(self) -> str:
        """Returns currently used profile.

        Returns:
        --------
        A string with username.
        """
        return self.Pennsieve.get_user()

    def set_profile(self, profile_name: str) -> str:
        """Changes the profile to the specified name.

        Parameters:
        -----------
        profile_name : str
            The name of the profile to change into.

        Returns:
        --------
        A string with confirmation of profile switch.
        """
        return self.Pennsieve.switch(profile_name)

    def close(self) -> None:
        """Closes the Pennsieve Agent."""
        return self.Pennsieve.stop()

    def list_datasets(
        self,
        limit: int = 10,
        offset: int = 0,
        query: str = None,
        organization: str = None,
        organization_id: int = None,
        tags: List[str] = None,
        embargo: bool = None,
        order_by: str = None,
        order_direction: str = None,
    ) -> list:
        """Gets datasets matching specified criteria.

        Parameters:
        -----------
        limit : int
            Max number of datasets returned.
        offset : int
            Offset used for pagination of results.
        query : str
            Fuzzy text search terms (refer to elasticsearch).
        organization : str
            Publishing organization.
        organization_id : int
            Publishing organization id.
        tags : list(str)
            Match dataset tags.
        embargo : bool
            Include embargoed datasets.
        order_by : str
            Field to order by:
                name - dataset name
                date - date published
                size - size of dataset
                relevance - order determined by elasticsearch
        order_direction : str
            Sort order:
                asc - Ascending, from A to Z
                desc - Descending, from Z to A

        Returns:
        --------
        A json with the results.

        """
        return self.Pennsieve.get(
            self.host_api + "/discover/search/datasets",
            headers=self.default_headers,
            params={
                "limit": limit,
                "offset": offset,
                "query": query,
                "organization": organization,
                "organizationId": organization_id,
                "tags": tags,
                "embargo": embargo,
                "orderBy": order_by,
                "orderDirection": order_direction,
            },
        )

    def list_files(
        self,
        limit: int = 10,
        offset: int = 0,
        file_type: str = None,
        query: str = None,
        organization: str = None,
        organization_id: int = None,
        dataset_id: int = None,
    ) -> list:
        """
        Parameters:
        -----------
        limit : int
            Max number of datasets returned.
        offset : int
            Offset used for pagination of results.
        file_type : str
            Type of file.
        query : str
            Fuzzy text search terms (refer to elasticsearch).
        model : str
            Only return records of this model.
        organization : str
            Publishing organization.
        organization_id : int
            Publishing organization id.
        dataset_id : int
            Files within this dataset.

        Returns:
        --------
        List of files stored at AWS with their parameters.
        """

        return self.Pennsieve.get(
            self.host_api + "/discover/search/files",
            headers=self.default_headers,
            params={
                "limit": limit,
                "offset": offset,
                "fileType": file_type,
                "query": query,
                "organization": organization,
                "organizationId": organization_id,
                "datasetId": dataset_id,
            },
        )["files"]

    def list_filenames(
        self,
        limit: int = 10,
        offset: int = 0,
        file_type: str = None,
        query: str = None,
        organization: str = None,
        organization_id: int = None,
        dataset_id: int = None,
    ) -> list:
        """Calls list_files() and extracts the names of the files.
        See also
        --------
        list_files()
        """
        response = self.list_files(
            limit=limit,
            offset=offset,
            file_type=file_type,
            query=query,
            organization=organization,
            organization_id=organization_id,
            dataset_id=dataset_id,
        )

        return list(map(lambda x: "/".join(x["uri"].split("/")[5:]), response))

    def list_records(
        self,
        limit: int = 10,
        offset: int = 0,
        model: str = None,
        organization: str = None,
        dataset_id: int = None,
    ) -> list:
        """
        Parameters:
        -----------
        limit : int
            Max number of datasets returned.
        offset : int
            Offset used for pagination of results.
        model : str
            Only return records of this model.
        organization : str
            Publishing organization.
        dataset_id : int
            Files within this dataset.
        """

        return self.Pennsieve.get(
            self.host_api + "/discover/search/records",
            headers=self.default_headers,
            params={
                "limit": limit,
                "offset": offset,
                "model": model,
                "organization": organization,
                "datasetId": dataset_id,
            },
        )

    def download_file(self, file_list: list[dict] | dict, output_name: str = None):
        """Downloads files into a local storage.

        Parameters:
        -----------
        file_list : list[dict] or dict
            Names of the file(s) to download with their parameters.
            The files need to come from a single database.
        output_name : str
            The name of the output file.

        Returns:
        --------
        A response from the server.
        """

        # make sure we are passing a list
        file_list = [file_list] if type(file_list) is dict else file_list

        # create a tuple with datasetId and version of the dataset
        properties = set([(x["datasetId"], x["datasetVersion"]) for x in file_list])

        # extract all the files
        paths = [
            x if x.get("uri") is None else "/".join(x.get("uri").split("/")[5:]) for x in file_list
        ]
        assert (
            len(properties) == 1
        ), "Downloading files from multiple datasets or dataset versions is not supported."

        # initialize parameters for the request
        json = {
            "data": {
                "paths": paths,
                "datasetId": next(iter(properties))[0],
                "version": next(iter(properties))[1],
            }
        }

        # download the files with zipit service
        url = "https://api.pennsieve.io/zipit/discover"
        headers = {"content-type": "application/json"}
        response = requests.post(url, json=json, headers=headers)

        # replace extension of the file with '.gz' if downloading more than 1 file
        if output_name is None:
            output_name = file_list[0]["name"] if len(paths) == 1 else "download.gz"

        with open(output_name, mode="wb+") as f:
            f.write(response.content)
        return response

    def get(self, url: str, **kwargs):
        """Invokes GET endpoint on a server. Passing server name in url is optional.

        Parameters:
        -----------
        url : str
            The address of the server endpoint to be called (e.g. api.pennsieve.io/datasets).
            The name of the server can be ommitted.
        kwargs : dict
            A dictionary storing additional information.

        Returns:
        --------
        String in JSON format with response from the server.

        Example:
        --------
        p=Pennsieve()
        p.get('https://api.pennsieve.io/discover/datasets', params={'limit':20})

        """
        return self.Pennsieve.get(url, **kwargs)

    def post(self, url: str, json: dict, **kwargs):
        """Invokes POST endpoint on a server. Passing server name in url is optional.

        Parameters:
        -----------
        url : str
            The address of the server endpoint to be called (e.g. api.pennsieve.io/datasets).
            The name of the server can be omitted.
        json : dict
            A request payload with parameters defined by a given endpoint.
        kwargs : dict
            Additional information.

        Returns:
        --------
        String in JSON format with response from the server.
        """
        return self.Pennsieve.post(url, json=json, **kwargs)

    def put(self, url: str, json: dict, **kwargs):
        """Invokes PUT endpoint on a server. Passing server name in url is optional.

        Parameters:
        -----------
        url : str
            The address of the server endpoint to be called (e.g. api.pennsieve.io/datasets).
            The name of the server can be omitted.
        json : dict
            A request payload with parameters defined by a given endpoint.
        kwargs : dict
            Additional information.

        Returns:
        --------
        String in JSON format with response from the server.
        """
        return self.Pennsieve.put(url, json=json, **kwargs)

    def delete(self, url: str, **kwargs):
        """Invokes DELETE endpoint on a server. Passing server name in url is optional.

        Parameters:
        -----------
        url : str
            The address of the server endpoint to be called. The name of the server can be omitted.
        kwargs : dict
            Additional information.

        Returns:
        --------
        String in JSON format with response from the server.
        """
        return self.Pennsieve.delete(url, **kwargs)
