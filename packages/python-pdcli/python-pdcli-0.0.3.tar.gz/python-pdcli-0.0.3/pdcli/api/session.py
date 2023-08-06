"""Session interfaces."""
import os

from pdpyras import APISession  # type: ignore


#: PD API key
API_KEY = os.environ.get("PD_ACCOUNT_TOKEN")

#: API session
_API_SESSION = None


def get_api_session():
    """Get api session."""
    global _API_SESSION  # pylint: disable=global-statement

    if not _API_SESSION:
        _API_SESSION = APISession(API_KEY)

    return _API_SESSION
