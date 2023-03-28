# Umbrella Policy Python SDK

## Description

I could not find a SDK for the Cisco Umbrella Policy v2 API so I decided to write my own for other projects I am working on.

## Getting Started


### Installing
You can install the package using pip:
```
$ pip install https://github.com/thegrumpyape/umbrella-policy-python-sdk.git@main
```

### Usage

NOTE: While I hardcoded the client id and client secret in the example. I recommend you store them outside of the script (i.e. environment variables)

Here's a simple example of how to retrieve a list of all destination lists:

```python
from umbrella_policy_python_sdk import Umbrella

API_KEY = "<YOUR_CLIENT_ID>"
API_SECRET = "<YOUR_CLIENT_SECRET>"

api = Umbrella(API_KEY, API_SECRET)

destination_lists = api.destination_lists()

for destination_list in destination_lists:
    print(destination_list['name'])
```

## Version History

* 0.1
    * Initial Release