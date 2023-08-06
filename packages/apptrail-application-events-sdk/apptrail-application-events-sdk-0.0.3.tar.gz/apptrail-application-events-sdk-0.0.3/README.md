# Apptrail Application Events SDK for Python

You can use the Apptrail Application Events SDK for Python to send audit logs from your
Python applications to your customers.

## Learn more

- [Working with events](https://apptrail.com/docs/applications/guide/working-with-events/overview)
- [Full SDK Reference](https://apptrail.com/docs/applications/guide/working-with-events/using-the-events-sdk/application-events-sdk-python)
- [Developer Guide](https://apptrail.com/docs/applications/guide)
- [Apptrail](https://apptrail.com)

## Notes and tips

- Requires Python >= 3.6
- Instantiate the client once at the top of your application and reuse it to prevent unnecessary recreation.

## Installing

The Events SDK is [published to PyPI](https://pypi.org/project/apptrail-application-events-sdk).

```bash
pip install apptrail-application-events-sdk
```

## Instantiating client

```python
from apptrail_application_events_sdk import ApptrailEventsClient

my_api_key = load_secret_api_Key()
my_region = "us-west-2";

events_client = ApptrailEventsClient(
  region=my_region,
  api_key=my_api_key,
)
```

## Sending an event

```python

event = {
  "tenantId": "cust_MGY4MmYzNDMtZjEwOC00OWI",
  "eventName": "CreateRepository",
  "eventTime": "2022-01-26T06:01:00Z",
  "actor": {
    "id": "acct_MmRlODllZDctM2I0Yi0",
    "details": {
      "type": "account",
      "name": "API Access",
    },
  },
  "resources": [
    {
      "id": "repo_YWI5NjkzY2UtNzI1Ny00N",
      "details": {
        "repositoryType": "V2",
      },
    },
  ],
  "context": {
    "sourceIpAddress": "103.6.179.245",
    "userAgent": "Apache-HttpClient/4.5.3 (Java/11.0.11)",
  }
  "tags": {
    "severity": "LOW",
  },
  "eventDetails": {
    "request": {
      "repositoryName": "my-repository",
    },
  },
};

events_client.put_event(event)
```

## Sending multiple events

```
events = [...]

events_client.put_events(events)
```

## Handling errors

As a best practice, you should handle errors while sending events, especially if you are sending critical logs. The Events client includes automatic retries with backoff, but errors can happen due to rare server issues or client side issues.

You can choose what to do with failing events. For example, you may sideline them to disk, or a dead letter queue for retry or remediation.

```python
from apptrail_application_events_sdk import ApptrailError

try:
  events_client.put_event(event)
except ApptrailError as e:
  # handle error
except Exception as e:
  # handle
```

## Logging

You can enable logging from the Apptrail Events SDK, from your application using the Python `logging` library. The Apptrail Events SDK uses a standard logger named `apptrail` that you can configure.

```python
import logging
from apptrail_application_events import ApptrailEventsClient

apptrail_logger = logging.getLogger('apptrail')
apptrail_logger.addHandler(logging.StreamHandler())
apptrail_logger.setLevel(logging.DEBUG)

# use SDK
```
