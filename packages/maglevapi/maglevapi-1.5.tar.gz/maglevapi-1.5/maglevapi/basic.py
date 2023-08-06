import asyncio
from typing import Any, Tuple


def quick_kwargs(*keys, kwargs: dict, default: Any = None) -> Tuple[Any]:
    """
    Instead of doing...
    >>> value_1 = kwargs.get("value_1")
    >>> value_2 = kwargs.get("value_2", "foo")
    >>> value_3 = kwargs.get("value_3")

    This compacts that so you can do...
    >>> value_1, value_2, value_3 = quick_kwargs("value_1", ("value_2", "foo"), "value_3")

    You could also make certain parameters required by doing so...
    >>> value_1 = quick_kwargs(("value_1", "__required__"))
    - If value_1 does not exist, a TypeError with a message of "missing required parameter 'value_1'" will be raised.
    """

    return_values = []
    for k in keys:
        if isinstance(k, tuple):
            default = k[1]
            if default == "__required__":
                if kwargs.get(k[0]) is None:
                    raise TypeError(f"missing required parameter '{k[0]}'")
                else:
                    return_values.append(kwargs.get(k[0]))
            else:
                return_values.append(kwargs.get(k[0], default))
            continue
        return_values.append(kwargs.get(k, default))

    if len(return_values) > 1:
        return tuple(return_values)
    return return_values[0]


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
