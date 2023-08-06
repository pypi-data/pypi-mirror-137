import time
from typing import Any, Tuple


class defaults:
    TIME_ROUND = 2


def timeit(func, *args, **kwargs) -> Tuple[str, Any]:
    """
    Times a function and returns it's (execution_time, func_result).

    Notes
    -----
    - This function does not return the execution time as an integer. Look at the formatting provided below for more information. This was done merely for printing purpose.
    - execution_time will be "{execution_time}ms" if it is < 1.0 else "{execution_time} seconds"

    Parameters
    ----------
    `func` : Callable
        The function to time.
    *args, **kwargs :
        Parameters to be passed to the function.

    Returns
    -------
    A tuple with the first value being the execution time and the second being the return value of `func`.
    """

    st = time.perf_counter()
    r = func(*args, **kwargs)
    et = time.perf_counter() - st
    et = round(et, defaults.TIME_ROUND)
    ind = " second(s)"
    if et < 1.0:
        et = et * 1000
        ind = "ms"
    return (f"{et}{ind}", r)


async def async_timeit(func, *args, **kwargs) -> Tuple[str, Any]:
    """Asyncio version of timeit()."""

    st = time.perf_counter()
    r = await func(*args, **kwargs)
    et = time.perf_counter() - st
    et = round(et, defaults.TIME_ROUND)
    ind = " second(s)"
    if et < 1.0:
        et = et * 1000
        ind = "ms"
    return (f"{et}{ind}", r)
