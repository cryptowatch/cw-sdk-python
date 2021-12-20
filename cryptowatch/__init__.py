from cryptowatch.utils import log
from cryptowatch.auth import read_config
from cryptowatch.requestor import Requestor
from cryptowatch import stream
from cryptowatch.resources.assets import Assets
from cryptowatch.resources.instruments import Instruments
from cryptowatch.resources.exchanges import Exchanges
from cryptowatch.resources.markets import Markets


# Package version
__version__ = "0.0.16"
sdk_version = __version__


# Try to read and set API endpoints from credential file
api_key, rest_endpoint, ws_endpoint = read_config()

# API default endpoints
if not rest_endpoint:
    rest_endpoint = "https://api.cryptowat.ch"
if not ws_endpoint:
    ws_endpoint = "wss://stream.cryptowat.ch/connect"


def is_authenticated():
    return api_key is not None


# HTTP client default settings
verify_ssl = True
connect_timeout = 4  # in seconds
read_timeout = 10  # in seconds
max_retries = 10  # number of time we'll retry a failing request
_user_agent = (
    "Mozilla/5.0 (compatible; Cryptowatch-Official-Python-SDK"
    "/v{} +https://cryptowat.ch/)".format(sdk_version)
)


# Get an instance of the HTTP client
requestor = Requestor(rest_endpoint, _user_agent, locals())


# Serialize resources to namespace
assets = Assets(requestor)
instruments = Instruments(requestor)
exchanges = Exchanges(requestor)
markets = Markets(requestor)
