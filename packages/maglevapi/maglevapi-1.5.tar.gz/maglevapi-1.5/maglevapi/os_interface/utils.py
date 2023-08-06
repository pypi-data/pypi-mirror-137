import json
import os
from typing import Union


def join_path(*path: str, cwd: Union[str, bool] = None) -> str:
    """
    Shortcut for performing a os.path.join(os.getcwd())

    Parameters
    ----------
    `*path` : str
        Either a path like "my/path/here.py" or a comma separated arguments path "my", "path", "here.py"
    `cwd` : Union[str, bool]
        The current working directory to use. Defaults to None which is to use os.getcwd(). You can pass False here to indicate that we should not use any cwd.

    Returns
    -------
    `str` :
        The joined path.
    """

    path = list(path)
    if len(path) < 2:
        path = path[0].split("/")

    if (cwd is None) or (cwd is True):
        cwd = os.getcwd()

    if cwd is not False:
        path.insert(0, cwd)

    return os.path.join(*path)


def load_json(path: str) -> dict:
    """
    Shortcut for loading json files.

    Parameters
    ----------
    `path` : str
        The path to the json file.

    Returns
    -------
    `dict`
    """

    with open(path) as f:
        return json.load(f)


def dump_json(path: str, data: Union[dict, list], indent: int = 4) -> str:
    """
    Shortcut for dumping data to a json file.

    Parameters
    ----------
    `path` : str
        The path to the json file.
    `data` : Union[dict, list]
        The json serializable object to dump.
    `indent` int
        Indentation. Defaults to 4.

    Returns
    -------
    `str` :
        The path where the json was dumped.
    """

    with open(path, "w+") as f:
        json.dump(data, f, indent=indent)
    
    return path
