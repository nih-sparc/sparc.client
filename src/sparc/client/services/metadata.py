import json

import requests
from requests.adapters import HTTPAdapter, Retry

from configparser import SectionProxy
from typing import List, Optional, Union
from ._default import ServiceBase


class MetadataService(ServiceBase):
    """A wrapper for the Elasticsearch Metadata library

    Parameters:
    -----------
    config : dict
        A configuration containing necessary API key (scicrunch_api_key).
    connect : bool
        Not needed with REST metadata services.

    Attributes:
    -----------
    default_headers : dict
        A dictionary with headers to make HTTP requests.
    host_api : str
        A default HTTP address of the SciCrunch Elasticsearch API endpoint.

    Methods:
    --------
    get_profile() -> str
        Returns the currently used API Key.
    set_profile() -> str
        Changes the API Key.
    close() : None
        Not needed with REST metadata services.
    getURL(...) : dict
        Supporting function to retrieve data from REST endpoint via GET
        This support Elasticsearch URL based queries
    postURL(...) : dict
        Supporting function to retrieve data from REST endpoint
        This supports Elasticsearch JSON queries
    list_datasets(...) : dict
        Returns a dictionary with datasets metadata.
    search_datasets(...) : dict
        Returns a dictionary with datasets matching search criteria.

    """

    default_headers = {
        "Content-Type": "application/json",
        "Accept": "application/json; charset=utf-8",
    }

    host_api = "https://scicrunch.org/api/1/elastic"

    scicrunch_api_key: str = None
    profile_name: str = None

    def __init__(
        self, config: Optional[Union[dict, SectionProxy]] = None, connect: bool = False
    ) -> None:
        logging.info("Initializing SPARC K-Core Elasticsearch services...")
        logging.debug(str(config))

        if config is not None:
            self.scicrunch_api_key = config.get("scicrunch_api_key")
            logging.info("SciCrunch API Key: Found")
            self.profile_name = config.get("pennsieve_profile_name")
            logging.info("Profile: " + self.profile_name)
        else:
            logging.warning("SciCrunch API Key: Not Found")
            logging.info("Profile: none")
        if connect:
            self.connect()

    def connect(self) -> str:
        """Not needed as metadata services are REST service calls"""
        logging.info("Metadata REST services available...")

        self.host_api = "https://scicrunch.org/api/1/elastic"
        return self.host_api

    def info(self) -> str:
        """Returns information about the metadata search services."""

        self.host_api = "https://scicrunch.org/api/1/elastic"
        return self.host_api

    def get_profile(self) -> str:
        """Returns currently used API key.

        Returns:
        --------
        A string with API Key.
        """
        return self.scicrunch_api_key

    def set_profile(self, api_key: str) -> str:
        """Changes the API key to the specified name.

        Parameters:
        -----------
        api_key : str
            The API key to use.

        Returns:
        --------
        A string with confirmation of API key switch.
        """
        self.scicrunch_api_key = api_key
        return self.scicrunch_api_key

    def close(self) -> None:
        """Not needed as metadata services are REST service calls"""
        return self.host_api

    #####################################################################
    # Supporting Functions

    #####################################################################
    # Function to GET content from URL with retries
    def getURL(self, url, headers="NONE"):
        result = "[ERROR]"
        url_session = requests.Session()

        retries = Retry(total=6,
                        backoff_factor=1,
                        status_forcelist=[403, 404, 413, 429, 500, 502, 503, 504])

        url_session.mount('https://', HTTPAdapter(max_retries=retries))

        success = 1

        try:
            if headers == "NONE":
                url_result = url_session.get(url)
            else:
                url_result = url_session.get(url, headers=headers)

            if url_result.status_code == 410:
                logging.warning("Retrieval Status 410 - URL Unpublished:" + url)
            else:
                url_result.raise_for_status()

        except requests.exceptions.HTTPError as errh:
            logging.error("Retrieving URL - HTTP Error:", errh)
            success = 0
        except requests.exceptions.ConnectionError as errc:
            logging.error("Retrieving URL - Error Connecting:", errc)
            success = 0
        except requests.exceptions.Timeout as errt:
            logging.error("Retrieving URL - Timeout Error:", errt)
            success = 0
        except requests.exceptions.RequestException as err:
            logging.error("Retrieving URL - Something Else", err)
            success = 0

        url_session.close()

        if success == 1:
            result = url_result
        else:
            result = {}

        return result.json()


#####################################################################
# Function to retrieve content via POST from URL with retries
    def postURL(self, url, body, headers="NONE"):

        result = "[ERROR]"
        url_session = requests.Session()

        retries = Retry(total=6,
                        backoff_factor=1,
                        status_forcelist=[403, 404, 413, 429, 500, 502, 503, 504])

        url_session.mount('https://', HTTPAdapter(max_retries=retries))

        try:
            if type(body) is dict:
                body_json = body
            else:
                body_json = json.loads(body)
        except:
                logging.error("Elasticsearch query body can not be read")
                              
        success = 1

        try:
            if headers == "NONE":
                url_result = url_session.post(url, json = body_json)
            else:
                url_result = url_session.post(url, json = body_json, headers=headers)

            if url_result.status_code == 410:
                logging.warning("Retrieval Status 410 - URL Unpublished:" + url)
            else:
                url_result.raise_for_status()

        except requests.exceptions.HTTPError as errh:
            logging.error("Retrieving URL - HTTP Error:", errh)
            success = 0
        except requests.exceptions.ConnectionError as errc:
            logging.error("Retrieving URL - Error Connecting:", errc)
            success = 0
        except requests.exceptions.Timeout as errt:
            logging.error("Retrieving URL - Timeout Error:", errt)
            success = 0
        except requests.exceptions.RequestException as err:
            logging.error("Retrieving URL - Something Else", err)
            success = 0

        url_session.close()

        if success == 1:
            result = url_result
        else:
            result = {}

        return result.json()
    

#####################################################################
# Metadata Search Functions

    def list_datasets(
        self,
        limit: int = 10,
        offset: int = 0
    ) -> list:
        """Lists datasets and associated metadata.

        Parameters:
        -----------
        limit : int
            Max number of datasets returned.
        offset : int
            Offset used for pagination of results.

        Returns:
        --------
        A json with the results.

        """
        self.host_api = "https://scicrunch.org/api/1/elastic/SPARC_Algolia_pr/_search"

        list_url = self.host_api + "?" + "from=" + str(offset) + "&size=" + str(limit) + "&key=" + self.scicrunch_api_key

        list_results = self.getURL(list_url, headers=self.default_headers)
        return list_results

    def search_datasets(self, query: str = '{"query": { "match_all": {}}}') -> list:
        """Gets datasets matching specified query.

        This function provides

        Parameters:
        -----------
        query : str
            Elasticsearch JSON query.

        Returns:
        --------
        A json with the results.

        """

        self.host_api = "https://scicrunch.org/api/1/elastic/SPARC_Algolia_pr/_search"

        list_url = self.host_api + "?" + "key=" + self.scicrunch_api_key

        list_results = self.postURL(list_url, body=query, headers=self.default_headers)
        return list_results
