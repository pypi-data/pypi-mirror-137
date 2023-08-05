""" Use the Apptrail Application Events SDK for Python to send audit logs to Apptrail from your Python applications.
"""

from ._client import ApptrailError, ApptrailEventsClient

__all__ = [
    "ApptrailEventsClient",
    "ApptrailError",
]
