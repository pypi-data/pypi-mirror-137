import asyncio
from typing import Any


async def async_wait_until(var: Any, val: Any = True) -> None:

    """
    Waits until a variable is a specific value.

    Parameters
    ----------
    `var` : Any
        The variable to constantly check.
    `val` : Any
        The value to wait for. Defaults to True. (i.e., wait for said `var` to be `True`)
    """

    while var is not val:
        await asyncio.sleep(0.0001)


def clean_string(s: str, lowercase: bool = True) -> str:
    if not lowercase:
        return s.strip()
    return s.strip().lower()
