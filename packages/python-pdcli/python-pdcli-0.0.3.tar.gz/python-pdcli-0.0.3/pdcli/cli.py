"""Callables of cli."""
import fire  # type: ignore

from . import pd as pd_


def pd():  # pylint: disable=invalid-name
    """Cli interface to pd service."""
    fire.Fire(pd_)
