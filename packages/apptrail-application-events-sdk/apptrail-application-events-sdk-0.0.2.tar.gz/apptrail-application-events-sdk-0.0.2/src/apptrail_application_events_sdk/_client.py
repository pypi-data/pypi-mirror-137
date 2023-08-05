import os
import json
import base64
import logging

import backoff
import requests
import jsonlines
import jsonschema

from io import BytesIO
from uuid import uuid4


def _make_logger():
    logger = logging.getLogger("apptrail")
    logger.setLevel(logging.INFO)
    return logger


def _get_application_id_from_api_key(api_key: str):
    try:
        return base64.b64decode(api_key + "==").decode().split(",")[0]
    except Exception:
        raise ValueError("Invalid API Key") from None


def _post_policy_giveup_check(e):
    status_code = e.response.status_code
    if not status_code:
        return False
    if status_code >= 500:
        return False
    elif status_code == 429:
        return False
    else:
        return True


def _upload_giveup_check(e):
    status_code = e.response.status_code
    if not status_code:
        return False
    if status_code >= 500:
        return False
    elif status_code == 429:
        return False
    else:
        return True


class ApptrailError(Exception):
    pass


class _PolicyExpiredException(Exception):
    pass


_EVENT_SCHEMA = json.load(open(os.path.join(os.path.dirname(__file__), "raw-event-schema.json")))
_VALIDATOR = jsonschema.Draft7Validator(_EVENT_SCHEMA, format_checker=jsonschema.FormatChecker())


class ApptrailEventsClient:
    """The Apptrail Events Client allows you to send audit logs to Apptrail.

    See:
        [Working with events](https://apptrail.com/docs/applications/guide/working-with-events/overview)
        [Sending events](https://apptrail.com/docs/applications/guide/working-with-events/sending-events)

    """

    logger = _make_logger()

    def __init__(
        self,
        *,
        region: str,
        api_key: str,
    ):
        """Create a new Apptrail Events Client.

        Keyword Args:
            region (str): The Apptrail region (e.g. `us-west-2`) to send events to. Construct separate instances per region.
                For more on Apptrail regions, see [Apptrail Regions](https://apptrail.com/docs/applications/guide/regions).
            api_key (str): Your API Key secret. For more on API keys, see [API Keys](https://apptrail.com/docs/applications/guide/dashboard/managing-api-keys).
        """
        self._application_id = _get_application_id_from_api_key(api_key)
        self.region = region
        self._base_api_url = "https://events.{}.apptrail.com/applications/session".format(region)
        self._api_key = api_key

        self._upload_url = None
        self._form = None

    def __repr__(self) -> str:
        return "ApptrailEventsClient[region={}]".format(self.region)

    def _make_s3_key(self):
        return os.path.join(self.application_id, f"{str(uuid4())}.jsonl")

    @backoff.on_exception(
        backoff.expo,
        requests.exceptions.RequestException,
        max_time=2,
        jitter=backoff.full_jitter,
        giveup=_post_policy_giveup_check,
    )
    def _refresh_post_policy(self):
        res = requests.get(self._base_api_url, headers={"Authorization": f"Bearer {self._api_key}"})
        if res.status_code >= 400 and res.status_code != 429:
            raise ApptrailError("Bad request. Status: {}".format(res.status_code))
        res.raise_for_status()
        res_body = res.json()
        self._form = res_body["form"]
        self._upload_url = res_body["uploadUrl"]

    @backoff.on_exception(
        backoff.expo,
        requests.exceptions.RequestException,
        max_time=2,
        jitter=backoff.full_jitter,
        giveup=_upload_giveup_check,
    )
    @backoff.on_exception(
        backoff.expo,
        _PolicyExpiredException,
        max_tries=2,
        jitter=None,
    )
    def _put_events_inner(self, events: list):
        if not self._form or not self._upload_url:
            self._refresh_post_policy()

        for event in events:
            try:
                _VALIDATOR.validate(event)
            except jsonschema.ValidationError as e:
                raise ApptrailError("Invalid event provided: {}".format(e.message)) from None

        content_bio = BytesIO()
        with jsonlines.Writer(content_bio, compact=True) as writer:
            writer.write_all(events)

        filename = str(uuid4()) + ".jsonl"
        key = os.path.join(self._application_id, filename)
        content = content_bio.getvalue().decode("utf-8")
        mp_form_data = {**self._form, "key": key, "file": (filename, content)}

        res = requests.post(self._upload_url, files=mp_form_data)

        if res.status_code == 403:
            if "Policy expired" in res.text:
                self._refresh_post_policy()
                raise _PolicyExpiredException()

        res.raise_for_status()

    def put_events(self, events: list):
        """Send a list of up to 1000 audit events to log to Apptrail.

        Args:
            events (List[dict]): A list of Apptrail events as a list of dictionaries. For details
                on the Apptrail event format, see [Event Format](https://apptrail.com/applications/guide/event-format)

        Raises:
            ApptrailError: If an error occurs during sending events, e.g in the case of server errors or client side issues.
                The SDK includes automatic retries with exponential backoff but you should handle errors and sideline audit logs,
                especially for critical audit data.
        """
        if not events:
            raise ValueError("Must provide at least one event.")
        if len(events) > 1000:
            raise ValueError("Cannot send more than 1000 events. Please make multiple calls.")
        msg = "Failed to put Events. Encountered exception."
        try:
            self._put_events_inner(events)
        except ApptrailError as ae:
            raise ApptrailError(msg) from ae
        except Exception:
            raise ApptrailError(msg) from None
        self.logger.info("Successfully sent {} Apptrail events.".format(len(events)))

    def put_event(self, event: dict):
        """Send a single audit event to log to Apptrail.

        Args:
            events (dict): The event to log as a dictionary. For details on the Apptrail event format,
                see [Event Format](https://apptrail.com/applications/guide/event-format)

        Raises:
            ApptrailError: If an error occurs during sending events, e.g in the case of server errors or client side issues.
                The SDK includes automatic retries with exponential backoff but you should handle errors and sideline audit logs,
                especially for critical audit data.
        """
        self.put_events([event])
