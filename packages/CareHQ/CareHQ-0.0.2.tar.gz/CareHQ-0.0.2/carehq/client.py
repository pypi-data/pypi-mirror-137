import hashlib
import json
import io
import time

import requests
from werkzeug.datastructures import MultiDict

from . import exceptions

__all__ = ['Client']


class APIClient:
    """
    A client for the CareHQ API.
    """

    def __init__(self,
        account_id,
        api_key,
        api_secret,
        api_base_url='https://api.carehq.co.uk',
        timeout=None
    ):

        # The Id of the CareHQ account the API key relates to
        self._account_id = account_id

        # A key used to authenticate API calls to an account
        self._api_key = api_key

        # A secret used to generate a signature for each API request
        self._api_secret = api_secret

        # The base URL to use when calling the API
        self._api_base_url = api_base_url

        # The period of time before requests to the API should timeout
        self._timeout = timeout

        # NOTE: Rate limiting information is only available after a request
        # has been made.

        # The maximum number of requests per second that can be made with the
        # given API key.
        self._rate_limit = None

        # The time (seconds since epoch) when the current rate limit will
        # reset.
        self._rate_limit_reset = None

        # The number of requests remaining within the current limit before the
        # next reset.
        self._rate_limit_remaining = None

    @property
    def rate_limit(self):
        return self._rate_limit

    @property
    def rate_limit_reset(self):
        return self._rate_limit_reset

    @property
    def rate_limit_remaining(self):
        return self._rate_limit_remaining

    def __call__(
        self,
        method,
        path,
        params=None,
        data=None,
    ):
        """Call the API"""

        # Filter out params/data set to `None` and ensure all arguments are
        # converted to strings.

        if params:
            params = {k: str(v) for k, v in params.items() if v is not None}

        if data:
            data = {k: str(v) for k, v in data.items() if v is not None}

        # Build the signature
        signature_body = json.dumps(
            MultiDict(
                params if method.lower() == 'get' else data
            ).to_dict(False)
        )

        timestamp = str(time.time())
        signature = hashlib.sha1()
        signature.update(
            ''.join([
                timestamp,
                signature_body,
                self._api_secret
            ]).encode('utf8')
        )
        signature = signature.hexdigest()

        # Build headers
        headers = {
            'Accept': 'application/json',
            'X-CareHQ-AccountId': self._account_id,
            'X-CareHQ-APIKey': self._api_key,
            'X-CareHQ-Signature': signature,
            'X-CareHQ-Timestamp': timestamp
        }

        # Make the request
        r = getattr(requests, method.lower())(
            f'{self._api_base_url}/v1/{path}',
            headers=headers,
            params=params,
            data=data,
            timeout=self._timeout
        )

        # Update the rate limit
        if 'X-CareHQ-RateLimit-Limit' in r.headers:
            self._rate_limit = int(r.headers['X-CareHQ-RateLimit-Limit'])
            self._rate_limit_reset \
                    = float(r.headers['X-CareHQ-RateLimit-Reset'])
            self._rate_limit_remaining \
                    = int(r.headers['X-CareHQ-RateLimit-Remaining'])

        # Handle a successful response
        if r.status_code in [200, 204]:
            return r.json()

        # Raise an error related to the response
        try:
            error = r.json()

        except ValueError:
            error = {}

        error_cls = exceptions.APIException.get_class_by_status_code(
            r.status_code
        )

        raise error_cls(
            r.status_code,
            error.get('hint'),
            error.get('arg_errors')
        )


