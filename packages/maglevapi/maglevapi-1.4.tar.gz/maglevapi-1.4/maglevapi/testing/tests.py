import asyncio
import gc
import inspect
import traceback
import os
from ..os_interface import utils
from ..profiling import async_timeit
from termcolor import colored
from pathlib import Path


class Testing:

    """
    Testing module.

    Parameters
    ----------
    `save_path` : str
        Path to save test results. Defaults to None which is to just print out the results.
    `spacing` : int
        How many seconds to wait before running the next test. Defaults to 0.5
    `gc_collect` : bool
        Whether to run the garbage collection before performing the next test. Defaults to False. I'm not so sure how useful this is but it's here anyways.
    `stop_on_exception` : bool  
        Whether to stop the all the other tests once a exception is raised. Defaults to False.
    `format` : Tuple[str]
        Two values indicating the format of (success, fail). Defaults to ("'{test_name}' ran successfully in '{t}'.", "'{test_name}' failed with the following traceback\n{tb}")

    Notes
    -----
    - Just like the builtin unittest module. Each test should be prefixed with a "test_"
    - Each test must be a coroutine (i.e, defined with `async def`)
    """

    def __init__(self, **params) -> None:
        self.save_path, \
        self.spacing, \
        self.gc_collect, \
        self.stop_on_exception, \
        self.format = utils.quick_kwargs(
            "save_path",
            ("spacing", 0.5),
            ("gc_collect", False),
            ("stop_on_exception", False),
            ("format", (
                "'{test_name}' ran successfully in '{t}'.",
                "'{test_name}' failed with the following traceback\n{tb}"
            )),
            kwargs=params
        )

        if self.save_path:
            Path(os.path.dirname(self.save_path)).mkdir(exist_ok=True, parents=True)

    def format_fail(self, test_name: str, tb: str) -> str:
        return self.format[1].replace("{test_name}", test_name) \
            .replace("{tb}", tb)

    def format_success(self, test_name: str, t: str) -> str:
        return self.format[0].replace("{test_name}", test_name) \
            .replace("{t}", t)

    async def run(self) -> None:
        """
        Run all the tests.
        """

        # Counter
        s = 0
        f = 0

        to_save = []
        for item in dir(self):
            if item.startswith("test_"):
                attr = getattr(self, item)
                if inspect.iscoroutinefunction(attr):

                    try:
                        print(colored(f"Running test '{item}'...", "yellow"), end="\r")
                        t, _ = await async_timeit(attr)
                        s += 1
                        to_save.append(f"OK! '{item}' - '{t}'")
                        print(colored(self.format_success(item, t), "green"))
                    except Exception as e:
                        f += 1
                        to_save.append(f"FAIL! '{item}' - '{str(e)}'")

                        if self.stop_on_exception:
                            raise e

                        tb = traceback.format_exc()
                        print(colored(self.format_fail(item, tb), "red"))

                    if self.gc_collect:
                        gc.collect()
                    await asyncio.sleep(self.spacing)

        print(colored(f"{s} successfull tests and {f} failed.", "cyan"))
        to_save.append(f"{s} - OK!\n{f} - FAIL!")

        if self.save_path and to_save:
            to_save = "\n".join(to_save)
            with open(self.save_path, "w") as f:
                f.write(to_save)
