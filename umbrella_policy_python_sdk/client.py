"""A simple client for sending requests to the Cisco Umbrella v2 API."""

from typing import Dict, List

import requests
from oauthlib.oauth2 import BackendApplicationClient, TokenExpiredError
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session


class Client:
    """A client for interacting with the Cisco Umbrella v2 API.

    :param token_url: The URL of the token endpoint for the API.
    :param client_id: The client ID for the API.
    :param client_secret: The client secret for the API.
    :param timeout: The timeout in seconds for API requests (default 5 seconds).
    """

    def __init__(
        self,
        base_url: str,
        token_url: str,
        client_id: str,
        client_secret: str,
        timeout: int = 5,
    ):
        self.base_url = base_url
        self.token_url = token_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = self.get_token()
        self.timeout = timeout

    def get_token(self):
        """Fetches an access token from the API using the OAuth2 client
        credentials flow.

        :return: A dictionary containing the access token and related information.
        """
        auth = HTTPBasicAuth(self.client_id, self.client_secret)
        client = BackendApplicationClient(client_id=self.client_id)
        oauth = OAuth2Session(client=client)
        self.token = oauth.fetch_token(token_url=self.token_url, auth=auth)
        return self.token

    def get_all(self, endpoint: str, params: Dict = None) -> List[Dict]:
        """Sends multiple GET requests to the specified API endpoint to
        retrieve all results.

        :param endpoint: The endpoint to call.
        :param params: Query parameters to include in the request (optional).
        :return: A list of dictionaries containing the JSON responses from the API.
        """
        all_results = []
        page = 1
        page_size = 100
        while True:
            # set the page and page_size parameters in the request
            page_param = {"page": page}
            if params is None:
                params = page_param
            else:
                params.update(page_param)
            params.update({"limit": page_size})

            # send the request and add the results to the list
            response = self.get(endpoint, params=params)
            results: List[Dict] = response.get("data", [])
            all_results.extend(results)

            # break the loop if all results have been retrieved
            if len(results) < page_size:
                break

            # update the page for the next request
            page += 1

        return all_results

    def get(self, endpoint: str, params: Dict = None) -> Dict:
        """Sends a GET request to the specified API endpoint.

        :param endpoint: The endpoint to call.
        :param params: Query parameters to include in the request (optional).
        :return: A dictionary containing the JSON response from the API.
        """
        return self.manual("GET", endpoint, params=params)

    def create(
        self,
        endpoint: str,
        payload: Dict,
        params: Dict = None,
    ) -> Dict:
        """Sends a POST request to the specified API endpoint.

        :param endpoint: The endpoint to call.
        :param params: Query parameters to include in the request (optional).
        :param payload: JSON payload to include in the request (optional).
        :return: A dictionary containing the JSON response from the API.
        """
        return self.manual("POST", endpoint, params=params, payload=payload)

    def update(self, endpoint: str, payload: Dict, params: Dict = None) -> Dict:
        """Sends a PATCH request to the specified API endpoint.

        :param endpoint: The endpoint to call.
        :param params: Query parameters to include in the request (optional).
        :param payload: JSON payload to include in the request (optional).
        :return: A dictionary containing the JSON response from the API.
        """
        return self.manual("PATCH", endpoint, params=params, payload=payload)

    def delete(
        self,
        endpoint: str,
        params: Dict = None,
        payload: Dict = None,
    ) -> Dict:
        """Sends a DELETE request to the specified API endpoint.

        :param endpoint: The endpoint to call.
        :param params: Query parameters to include in the request (optional).
        :return: A dictionary containing the JSON response from the API.
        """
        return self.manual("DELETE", endpoint, params=params, payload=payload)

    def manual(
        self,
        method: str,
        endpoint: str,
        params: Dict = None,
        payload: Dict = None,
    ) -> Dict:
        """Sends a manual request to the specified API endpoint.

        :param method: The HTTP method to use for the request (e.g. GET, POST, etc.).
        :param endpoint: The endpoint to call.
        :param params: Query parameters to include in the request (optional).
        :param payload: JSON payload to include in the request (optional).
        :return: A dictionary containing the JSON response from the API.
        """
        success = False
        response = None
        if self.token is None:
            self.get_token()
        while not success:
            try:
                api_headers = {"Authorization": f"Bearer {self.token['access_token']}"}
                url = self.base_url + endpoint
                response = requests.request(
                    method,
                    url,
                    headers=api_headers,
                    params=params,
                    json=payload,
                    timeout=self.timeout,
                )
                response.raise_for_status()
                success = True
            except TokenExpiredError:
                self.token = self.get_token()
        return response.json() if response is not None else {}
