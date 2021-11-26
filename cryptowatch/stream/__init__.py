import websocket
import json
import traceback
import threading
from google import protobuf

import cryptowatch
from cryptowatch.utils import log
from cryptowatch.errors import APIKeyError
from cryptowatch.utils import forge_stream_subscription_payload
from cryptowatch.stream.proto.public.stream import stream_pb2
from cryptowatch.stream.proto.public.client import client_pb2


subscriptions = []

_ws = None


def _on_open(ws):
    subs_payload = forge_stream_subscription_payload(subscriptions, client_pb2)
    log(
        "Connection established. Sending subscriptions payload: {}".format(
            subs_payload
        ),
        is_debug=True,
    )
    ws.send(subs_payload)


def _on_error(ws, error):
    log(str(error), is_error=True)


def _on_close(ws, close_status_code, close_reason):
    log("Connection closed.", is_debug=True)


def on_market_update(ws, message):
    try:
        stream_message = stream_pb2.StreamMessage()
        stream_message.ParseFromString(message)
        if str(stream_message.marketUpdate.intervalsUpdate):
            on_intervals_update(stream_message)
        elif str(stream_message.marketUpdate.tradesUpdate):
            on_trades_update(stream_message)
        elif str(stream_message.marketUpdate.orderBookUpdate):
            on_orderbook_snapshot_update(stream_message)
        elif str(stream_message.marketUpdate.orderBookDeltaUpdate):
            on_orderbook_delta_update(stream_message)
        elif str(stream_message.marketUpdate.orderBookSpreadUpdate):
            on_orderbook_spread_update(stream_message)
        else:
            log(stream_message, is_debug=True)
    except protobuf.message.DecodeError as ex:
        log("Could not decode this message: {}".format(message), is_error=True)
        log(traceback.format_exc(), is_error=True)
    except Exception as ex:
        log(traceback.format_exc(), is_error=True)


def on_trades_update(trades_update):
    pass


def on_intervals_update(intervals_update):
    pass


def on_orderbook_spread_update(orderbook_spread_update):
    pass


def on_orderbook_delta_update(orderbook_delta_update):
    pass


def on_orderbook_snapshot_update(orderbook_snapshot_update):
    pass


def connect(ping_timeout=20, ping_interval=70):
    if cryptowatch.api_key:
        DSN = "{}?apikey={}&format=binary".format(
            cryptowatch.ws_endpoint, cryptowatch.api_key
        )
    else:
        raise APIKeyError(
            "An API key is required to use the Cryptowatch Websocket API.\n"
            "You can create one at https://cryptowat.ch/account/api-access"
        )
    log("DSN used: {}".format(DSN), is_debug=True)
    websocket.enableTrace(False)
    global _ws
    _ws = websocket.WebSocketApp(
        DSN,
        on_message=on_market_update,
        on_error=_on_error,
        on_close=_on_close,
        on_open=_on_open,
    )
    wst = threading.Thread(
        target=_ws.run_forever,
        kwargs={"ping_timeout": ping_timeout, "ping_interval": ping_interval},
    )
    wst.daemon = False
    wst.start()
    log(
        "Ping timeout used: {}. Ping interval used: {}".format(
            ping_timeout, ping_interval
        ),
        is_debug=True,
    )


def disconnect():
    global _ws
    _ws.close()
