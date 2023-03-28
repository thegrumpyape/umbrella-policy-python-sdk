import os

import pytest
from dotenv import load_dotenv

from umbrella_policy_python_sdk import Umbrella

if os.path.exists('.env'):
    load_dotenv('.env')


@pytest.fixture(scope='session')
def umbrella_client():
    client_id = str(os.environ.get("UMBRELLA_CLIENT_ID"))
    client_secret = str(os.environ.get("UMBRELLA_CLIENT_SECRET"))
    umbrella = Umbrella(client_id, client_secret)
    yield umbrella


@pytest.fixture(scope='session')
def test_create_destination_list(umbrella_client):
    name = "Test Destination List"
    access = "block"
    destination_list = umbrella_client.create_destination_list(name, access)
    destination_list_id = destination_list["id"]
    assert isinstance(destination_list, dict)
    assert isinstance(destination_list_id, int)
    assert destination_list["name"] == name
    assert destination_list["access"] == access

    yield destination_list_id


@pytest.fixture(scope='session')
def test_destinations(umbrella_client, test_create_destination_list):
    destination_list_id = test_create_destination_list
    result = umbrella_client.destinations(destination_list_id)
    assert isinstance(result, list)

    destination_ids = [destination["id"] for destination in result]

    yield destination_ids


def test_add_destinations(umbrella_client, test_create_destination_list):
    destination_list_id = test_create_destination_list
    destinations = ["foo.bar.test", "bar.foo.test"]
    result = umbrella_client.add_destinations(destination_list_id, destinations)
    print(result)
    assert isinstance(result, dict)
    assert result["id"] == destination_list_id
    assert result["meta"]["destinationCount"] == 2


def test_destination_list(umbrella_client, test_create_destination_list):
    destination_list_id = test_create_destination_list
    result = umbrella_client.destination_list(destination_list_id)
    assert isinstance(result, dict)
    assert result["id"] == destination_list_id


def test_update_destination_list(umbrella_client, test_create_destination_list):
    destination_list_id = test_create_destination_list
    new_name = "New Test Destination List"
    result = umbrella_client.update_destination_list(destination_list_id, new_name)
    assert isinstance(result, dict)
    assert result["id"] == destination_list_id
    assert result["name"] == new_name


def test_destinations_list(umbrella_client, test_create_destination_list):
    destination_list_id = test_create_destination_list
    result = umbrella_client.destinations(destination_list_id)
    assert isinstance(result, list)


def test_delete_destinations(
    umbrella_client,
    test_create_destination_list,
    test_destinations,
):
    destination_list_id = test_create_destination_list
    destination_ids = test_destinations
    result = umbrella_client.delete_destinations(destination_list_id, destination_ids)
    assert isinstance(result, dict)
    assert result["id"] == destination_list_id
    assert result["meta"]["destinationCount"] == 0


def test_delete_destination_list(umbrella_client, test_create_destination_list):
    destination_list_id = test_create_destination_list
    result = umbrella_client.delete_destination_list(destination_list_id)
    assert isinstance(result, dict)
    assert result["code"] == 200
    assert result["text"] == "OK"
