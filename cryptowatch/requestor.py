import sys
import traceback
import json
from urllib.parse import urlencode
from urllib3.util.retry import Retry


import cryptowatch
from cryptowatch.utils import log


try:
    import requests
except ImportError:
    print(
        'Warning: The Cryptowatch Python SDK requires the "requests" library.'
        "This library is used to send HTTP requests to the Cryptowatch API."
        "You can install it by running: "
        "pip install -U requests",
        file=sys.stderr,
    )
else:
    try:
        # Require version 0.8.8 or newer as we want to enforce the
        # SSL certificate verification
        version = requests.__version__
        major, minor, patch = [int(i) for i in version.split(".")]
    except Exception:
        pass
    else:
        if (major, minor, patch) < (0, 8, 8):
            print(
                "Warning: The Cryptowatch SDK requires that your Python "
                '"requests" library be newer than version 0.8.8, but your '
                '"requests" library is version {}.'
                "We request this version to be able to verify the SSL "
                "certificate. Without this a 3rd party on your network could "
                "pretend to be Cryptowatch server."
                'We recommend upgrading your "requests" library.'
                "You can do so by running: "
                "pip install -U requests".format(version),
                file=sys.stderr,
            )


class Requestor:
    def __init__(self, rest_endpoint, user_agent, opts={}):
        # Must have options
        self.user_agent = user_agent
        self.rest_endpoint = rest_endpoint
        if not rest_endpoint.startswith("https"):
            log('Warning: API endpoint must start with "https".', is_error=True)
        if not user_agent:
            log("Warning: User-Agent header must be set.", is_error=True)
        # Options with defaults, overridden by kwargs
        self.verify_ssl = opts.get("verify_ssl", True)
        self.connect_timeout = opts.get("connect_timeout", 5)
        self.read_timeout = opts.get("read_timeout", 20)
        self.max_retries = opts.get("max_retries", 5)
        # Make all API calls share the same session
        self.api_client = requests.Session()
        # Apply a backoff for failing requests, up to self.max_retries
        # 1st waiting will be 0.1s, then 0.2s, 0.4s, etc, following this formula:
        # {backoff factor} * (2 ** ({number of retries so far} - 1))
        retries = Retry(
            total=self.max_retries,
            backoff_factor=0.1,
            status_forcelist=[500, 502, 503, 504],
        )
        a = requests.adapters.HTTPAdapter(max_retries=retries)
        self.api_client.mount("https://", a)

    def get_resource(self, resource, query=None):
        try:
            headers = {"User-Agent": self.user_agent, "Accept": "application/json"}
            if cryptowatch.api_key:
                headers["X-CW-API-Key"] = cryptowatch.api_key

            url = f"{self.rest_endpoint}{resource}"

            if query:
                querystring = urlencode(query)
                url = f"{url}?{querystring}"

            log("HTTP GET {}\n\twith headers: {}".format(url, headers), is_debug=True)
            resp = self.api_client.get(
                url,
                headers=headers,
                verify=self.verify_ssl,
                timeout=(self.connect_timeout, self.read_timeout),
                allow_redirects=True,
            )
            log(
                "Received HTTP Status {} for {}".format(resp.status_code, url),
                is_debug=True,
            )
            resp.raise_for_status()
        # Only catch API Errors, let other Exceptions bubble up
        except requests.exceptions.HTTPError as ex:
            # Resource not found
            if resp.status_code == 404:
                msg = resp.json().get("error", "No such resource at {}".format(url))
                raise cryptowatch.errors.APIResourceNotFoundError(
                    msg, resp.text, resp.status_code, resp.request.headers,
                )
            # Allowance exceeded
            elif resp.status_code == 429:
                msg = resp.json().get(
                    "error",
                    "You have exceeded your current API allowance. "
                    "Upgrade for a higher allowance at https://cryptowat.ch/pricing",
                )
                raise cryptowatch.errors.APIRateLimitError(
                    msg, resp.text, resp.status_code, resp.request.headers,
                )
            # Any HTTP 4XX Error
            elif str(resp.status_code).startswith("4"):
                msg = resp.json().get(
                    "error", "Your request failed. Please try again in a moment."
                )
                raise cryptowatch.errors.APIRequestError(
                    msg, resp.text, resp.status_code, resp.request.headers,
                )
            # Any HTTP 5XX Error
            elif str(resp.status_code).startswith("5"):
                msg = resp.json().get(
                    "error",
                    "The Cryptowatch API is having some issues. Please try again in a moment.",
                )
                raise cryptowatch.errors.APIServerError(
                    msg, resp.text, resp.status_code, resp.request.headers,
                )
            # Any other HTTP Error
            else:
                raise cryptowatch.errors.APIError(
                    "Error connecting to the API. Please try again in a moment.",
                    resp.text,
                    resp.status_code,
                    resp.request.headers,
                )
        else:
            return resp.text, resp
