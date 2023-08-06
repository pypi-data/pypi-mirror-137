import datetime
import json
import random
import string
import time
from typing import Any, Tuple

import bcrypt
from flask import Flask, request

from .codes import *

DICTIONARY = string.hexdigits + string.digits + ".-,;" + string.ascii_lowercase
SALT_ROUNDS = 10
MAX_REQUESTS_BUFFER = 256


def generate_id() -> str:
    r = "".join(random.choices(string.digits, k=10)) + \
        "".join(random.choices("123456789CUMBALLS", k=10)) + \
        str(int(time.time()))[-4:]
    return r


def generate_credentials(length: int) -> Tuple[str, str]:
    """Generates credentials. Returns a tuple. (api_key, api_id) """

    key = "".join(random.choices(DICTIONARY, k=length))
    return key, generate_id()


def create_hash(k: str) -> bytes:
    return bcrypt.hashpw(k.encode(), bcrypt.gensalt(SALT_ROUNDS))


def compare_hash(k: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(k.encode(), hashed)


class RouteSecurity:
    """
    Class that deals with securing routes using API keys.

    Notes
    -----
    - This uses the json data that comes with the request. Obviously if no json was passed, authentication would also fail.

    Parameters
    ----------
    `app` : Union[Flask, Blueprint]
        The flask app to secure or a blueprint of the flask app.
    `db` : Database
        Pymongo or pymongo-like database to use for storing credentials.
    `redis` : Redis
        Redis instance, used for caching.
    `key_holder` : str
        The name of the key in the json content that contains the API key. Defaults to "api_key".
    `id_holder` : str
        Similar to key_holder but for ids. Defaults to "api_id".
    `pop_credentials` : bool
        Whether to pop the key and id upon checking. Defaults to True.
    `log_requests` : bool    
        Whether to log every single request. Defaults to True.
    `max_request_logs` : int
        Maximum amount of request logs. Defaults to 200.
    `logging` : Logger
        Logger object from py-prettylog. If provided, all logs coming from this class will be in the group "route-security"
    """

    LOGGING_GROUP = "route-security"

    def __init__(self, app: Flask, db: Any, redis: Any, key_holder: str = "api_key", id_holder: str = "api_id", **kwargs) -> None:
        self.app = app
        self.db = db
        self.redis = redis
        self.key_holder = key_holder
        self.id_holder = id_holder
        self.pop_credentials = kwargs.get("pop_credentials", True)
        self.log_requests = kwargs.get("log_requests", True)
        self.max_requests_logs = kwargs.get("max_requests_logs", 200)
        self.logging = kwargs.get("logging")

    def patch(self) -> None:
        """Patch flask's before_request. Must be called in order for the security to take effect."""
        @self.app.before_request
        async def before_request():
            data = request.json
            if data:
                func = {
                    True: data.pop,
                    False: data.get
                }

                key = func[self.pop_credentials](self.key_holder, None)
                id_ = func[self.pop_credentials](self.id_holder, None)
                if key and id_:
                    valid = await self.validate_credentials(key, id_)
                    if valid:
                        if self.log_requests:
                            await self.log_request(id_, 4)
                        return

            return CODE_403

    async def log_request(self, id_: str, buffer: int) -> None:
        """
        Store the request in redis then update the requests list in db.user after the buffer has been reached.

        Notes
        -----
        - Validation is not performed here, therefore you mus not call this manually. This is all called after validation occurs.

        Parameters
        ----------
        `id_` : str
            API Id.
        """

        query_string = f"requests:{id_}"

        if not self.redis.exists(query_string):
            self.redis.set(query_string, json.dumps([]))

        # Create the log details
        data = {
            "ip": request.remote_addr,
            "created": datetime.datetime.now().isoformat(),
            "url": request.url,
            "user_agent": request.headers.get("User-Agent")
        }

        stored = json.loads(self.redis.get(query_string).decode("utf-8"))
        stored.append(data)
        self.redis.set(query_string, json.dumps(stored))

        if len(stored) > buffer:

            account_data = self.db.api_accounts.find_one({"id": id_})
            if account_data:
                if len(account_data["requests"]) > self.max_requests_logs:
                    del account_data["requests"][:len(stored)]
                account_data["requests"].extend(stored)

                self.db.api_accounts.update_one(
                    {"id": id_}, {"$set": account_data})

            self.redis.set(query_string, json.dumps([]))

    async def validate_credentials(self, key: str, id_: str) -> bool:
        """
        Validate API credentials.

        Parameters
        ----------
        `key` : str
            The key to validate against the hashes stored in the database.
        `id_` : str
            The id registered with that api key.

        Returns
        -------
        `bool` : 
            Indicating whether the key is valid or not.
        """

        cache_string = f"cached_credentials:{id_}#{key}"
        cache_time = 8600

        # Check if the provided credentials is in the cache
        # 1 - Valid credentials
        # 0 - Invalid
        if self.redis.exists(cache_string):
            if int(self.redis.get(cache_string).decode("utf-8")):

                if self.logging:
                    self.logging.debug(
                        f"ID: {id_} & Key: {key} is in the cache and is valid.", group="route-security")

                return True
            else:

                if self.logging:
                    self.logging.debug(
                        f"ID: {id_} & Key: {key} is in the cache and is invalid.", group="route-security")

                return False

        data = self.db.api_accounts.find_one({"id": id_})
        validated = False
        if data:
            hashed = data["api_key"]
            if compare_hash(key, hashed):
                validated = True

        self.redis.setex(cache_string, cache_time, int(validated))
        if self.logging:
            self.logging.debug(
                f"Credentials cached in the key of '{cache_string}' with a value of {int(validated)}", group="route-security")
        return validated
