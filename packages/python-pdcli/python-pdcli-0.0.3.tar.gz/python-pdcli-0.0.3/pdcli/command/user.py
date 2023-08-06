"""Implement pd user command."""
import json

from ..api.user import get_user, ls_user


def user(user_id: str = None) -> str:
    """Get user.

    :param user_id: user id. "me" for current user.
        list all user if unspecified.
    """
    result = get_user(user_id=user_id) if user_id else ls_user()

    return json.dumps(result)
