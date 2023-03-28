"""A simple API wrapper for the Cisco Umbrella Policies v2 API."""
from typing import Dict, List

from .client import Client


class Umbrella:
    """A simple API wrapper for the Cisco Umbrella Policies v2 API.

    **Attributes:**

    - BASE_URL (str): The base URL for the Umbrella API.
    - TOKEN_URL (str): The URL for retrieving an access token for the Umbrella API.

    **Args:**

    - client_id (str): The client ID for the Umbrella API.
    - client_secret (str): The client secret for the Umbrella API.

    **Methods:**

    - `destination_lists(params: dict | None = None) -> List[Dict]`: Retrieves a list of destination lists from the Umbrella API.
    - `create_destination_list(name: str, access: str, is_global: bool = False, params: dict | None = None) -> Dict`: Creates a new destination list on the Umbrella API.
    - `update_destination_list(destination_list_id: int, name: str) -> Dict`: Updates an existing destination list on the Umbrella API.
    - `delete_destination_list(destination_list_id: int) -> str`: Deletes a destination list from the Umbrella API.
    - `destination_list(destination_list_id: int, params: dict | None = None) -> Dict`: Retrieves a single destination list from the Umbrella API.
    - `destinations(destination_list_id: int, params: dict | None = None) -> List[Dict]`: Retrieves a list of destinations for a destination list from the Umbrella API.
    - `add_destinations(destination_list_id: int, destinations: List[str]) -> Dict`: Adds a list of destinations to a destination list on the Umbrella API.
    - `delete_destinations(destination_list_id: int, destination_ids: List[str]) -> Dict`: Removes a list of destinations from a destination list on the Umbrella API.
    """  # noqa

    BASE_URL = "https://api.umbrella.com/policies/v2"
    TOKEN_URL = "https://api.umbrella.com/auth/v2/token"

    def __init__(self, client_id: str, client_secret: str) -> None:
        """Initializes a new Umbrella client.

        :param client_id: The client ID for the Umbrella API.
        :type client_id: str
        :param client_secret: The client secret for the Umbrella API.
        :type client_secret: str
        """  # noqa
        self.client = Client(self.BASE_URL, self.TOKEN_URL, client_id, client_secret)

    def destination_lists(self, params: dict | None = None):
        """Retrieves a list of destination lists from the Umbrella API.

        :param params: Additional parameters to include in the request to the Umbrella API. Defaults to None.
        :type params: dict, optional

        :returns: A list of destination lists from the Umbrella API.
        :rtype: List[Dict]
        """  # noqa
        result = self._get_all("/destinationlists", params=params)
        return result

    def create_destination_list(
        self,
        name: str,
        access: str,
        is_global: bool = False,
        params: dict | None = None,
    ):
        """Creates a new destination list on the Umbrella API.

        :param name: The name of the new destination list.
        :type name: str
        :param access: The access level for the new destination list.
        :type access: str
        :param is_global: Whether the new destination list is global. Defaults to False.
        :type is_global: bool, optional
        :param params: Additional parameters to include in the request to the Umbrella API. Defaults to None.
        :type params: dict, optional

        :returns: The response from the Umbrella API for creating a new destination list.
        :rtype: dict
        """  # noqa
        payload = {"name": name, "isGlobal": is_global, "access": access}
        result = self.client.create("/destinationlists", payload=payload, params=params)
        return result

    def update_destination_list(self, destination_list_id: int, name: str):
        """Updates an existing destination list on the Umbrella API.

        :param destination_list_id: The ID of the destination list to update.
        :type destination_list_id: int
        :param name: The new name for the destination list.
        :type name: str

        :returns: The updated destination list from the Umbrella API.
        :rtype: dict
        """  # noqa
        payload = {"name": name}
        result = self.client.update(
            f"/destinationlists/{destination_list_id}", payload=payload
        )
        return result["data"]

    def delete_destination_list(self, destination_list_id: int):
        """Deletes a destination list from the Umbrella API.

        :param destination_list_id: The ID of the destination list to delete.
        :type destination_list_id: int

        :returns: The status message from the Umbrella API for deleting a destination list.
        :rtype: str
        """  # noqa
        result = self.client.delete(f"/destinationlists/{destination_list_id}")
        return result["status"]

    def destination_list(self, destination_list_id: int, params: dict | None = None):
        """Retrieves a single destination list from the Umbrella API.

        :param destination_list_id: The ID of the destination list to retrieve.
        :type destination_list_id: int
        :param params: Additional parameters to include in the request to the Umbrella API.
        :type params: dict | None

        :returns: The destination list from the Umbrella API.
        :rtype: dict
        """  # noqa
        result = self.client.get(
            f"/destinationlists/{destination_list_id}", params=params
        )
        return result["data"]

    def destinations(self, destination_list_id: int, params: dict | None = None):
        """Retrieves a list of destinations for a destination list from the Umbrella API.

        :param destination_list_id: The ID of the destination list to retrieve destinations for.
        :type destination_list_id: int
        :param params: Additional parameters to include in the request to the Umbrella API.
        :type params: dict | None

        :returns: A list of destinations for the specified destination list from the Umbrella API.
        :rtype: list[dict]
        """  # noqa
        result = self._get_all(
            f"/destinationlists/{destination_list_id}/destinations", params=params
        )
        return result

    def add_destinations(self, destination_list_id: int, destinations: List[str]):
        """Adds a list of destinations to a destination list on the Umbrella
        API.

        Args:
            destination_list_id (int): The ID of the destination list to add destinations to.
            destinations (List[str]): A list of destination URLs or IP addresses to add to the destination list.

        Returns:
            Dict: The response from the Umbrella API for adding destinations to a destination list.
        """  # noqa
        dest_dict = [{"destination": entry} for entry in destinations]

        batches = self._make_batches(dest_dict, 100)

        result = None
        for batch in batches:
            result = self.client.create(
                f"/destinationlists/{destination_list_id}/destinations", payload=batch
            )
        return result["data"] if result is not None else None

    def delete_destinations(self, destination_list_id: int, destination_ids: List[str]):
        """Removes a list of destinations from a destination list on the Umbrella API.

        :param destination_list_id: The ID of the destination list to remove destinations from.
        :type destination_list_id: int
        :param destination_ids: A list of destination IDs to remove from the destination list.
        :type destination_ids: list[str]

        :returns: The response from the Umbrella API for removing destinations from a destination list.
        :rtype: dict
        """  # noqa
        batches = self._make_batches(destination_ids, 100)
        result = None
        for batch in batches:
            result = self.client.delete(
                f"/destinationlists/{destination_list_id}/destinations/remove",
                payload=batch,
            )
        return result["data"] if result is not None else None

    def _get_all(self, endpoint: str, params: dict | None = None):
        """Retrieves all results from a paginated endpoint on the Umbrella API.

        :param endpoint: The endpoint to retrieve results from.
        :type endpoint: str
        :param params: Additional parameters to include in the request to the Umbrella API.
        :type params: dict | None

        :returns: A list of all results from the paginated endpoint.
        :rtype: list[dict]
        """  # noqa
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
            response = self.client.get(endpoint, params=params)
            results: List[Dict] = response.get("data", [])
            all_results.extend(results)

            # break the loop if all results have been retrieved
            if len(results) < page_size:
                break

            # update the page for the next request
            page += 1

        return all_results

    def _make_batches(self, entries: List, size: int) -> List[List]:
        """Splits a list of entries into batches of a specified size.

        :param entries: The list of entries to split into batches.
        :type entries: list
        :param size: The size of each batch.
        :type size: int

        :returns: A list of batches, with each batch containing `size` entries or fewer.
        :rtype: list[list]

        """  # noqa
        return [entries[i: i + size] for i in range(0, len(entries), size)]
