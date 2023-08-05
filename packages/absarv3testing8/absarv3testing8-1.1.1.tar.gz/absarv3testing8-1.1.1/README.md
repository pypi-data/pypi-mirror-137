
# Getting Started with RESTAPI SDK

## Install the Package

The package is compatible with Python versions `2 >=2.7.9` and `3 >=3.4`.
Install the package from PyPi using the following pip command:

```python
pip install absarv3testing8==1.1.1
```

You can also view the package at:
https://pypi.python.org/pypi/absarv3testing8

## Test the SDK

You can test the generated SDK and the server with test cases. `unittest` is used as the testing framework and `nose` is used as the test runner. You can run the tests as follows:

Navigate to the root directory of the SDK and run the following commands

```
pip install -r test-requirements.txt
nosetests
```

## Initialize the API Client

**_Note:_** Documentation for the client can be found [here.](/doc/client.md)

The following parameters are configurable for the API Client:

| Parameter | Type | Description |
|  --- | --- | --- |
| `content_type` | `string` | body content type for post request<br>*Default*: `'application/json'` |
| `accept_language` | `string` | response format<br>*Default*: `'application/json'` |
| `base_url` | `string` | *Default*: `'https://localhost:443'` |
| `environment` | Environment | The API environment. <br> **Default: `Environment.PRODUCTION`** |
| `http_client_instance` | `HttpClient` | The Http Client passed from the sdk user for making requests |
| `override_http_client_configuration` | `bool` | The value which determines to override properties of the passed Http Client from the sdk user |
| `timeout` | `float` | The value to use for connection timeout. <br> **Default: 60** |
| `max_retries` | `int` | The number of times to retry an endpoint call if it fails. <br> **Default: 0** |
| `backoff_factor` | `float` | A backoff factor to apply between attempts after the second try. <br> **Default: 2** |
| `retry_statuses` | `Array of int` | The http statuses on which retry is to be done. <br> **Default: [408, 413, 429, 500, 502, 503, 504, 521, 522, 524]** |
| `retry_methods` | `Array of string` | The http methods on which retry is to be done. <br> **Default: ['GET', 'PUT']** |

The API client can be initialized as follows:

```python
from restapisdk.restapisdk_client import RestapisdkClient
from restapisdk.configuration import Environment

client = RestapisdkClient(
    content_type='application/json',
    accept_language='application/json',
    environment=Environment.PRODUCTION,
    base_url = 'https://localhost:443',)
```

## Authorization

This API uses `OAuth 2 Bearer token`.

## List of APIs

* [API](/doc/controllers/api.md)
* [Session](/doc/controllers/session.md)
* [User](/doc/controllers/user.md)
* [Group](/doc/controllers/group.md)
* [Metadata](/doc/controllers/metadata.md)
* [Database](/doc/controllers/database.md)
* [Connection](/doc/controllers/connection.md)

## Classes Documentation

* [Utility Classes](/doc/utility-classes.md)
* [HttpResponse](/doc/http-response.md)
* [HttpRequest](/doc/http-request.md)

