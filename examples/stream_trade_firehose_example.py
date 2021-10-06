import cryptowatch as cw
import time


cw.stream.subscriptions = ["markets:*:trades"]


def handle_trades_update(trade_update):
    """
    trade_update follows Cryptowatch protocol buffer format:
    https://github.com/cryptowatch/proto/blob/master/public/markets/market.proto
    """
    market_msg = ">>> Market#{} Exchange#{} Pair#{}: {} New Trades".format(
        trade_update.marketUpdate.market.marketId,
        trade_update.marketUpdate.market.exchangeId,
        trade_update.marketUpdate.market.currencyPairId,
        len(trade_update.marketUpdate.tradesUpdate.trades),
    )
    print(market_msg)
    for trade in trade_update.marketUpdate.tradesUpdate.trades:
        trade_msg = "\tID:{} TIMESTAMP:{} TIMESTAMPNANO:{} PRICE:{} AMOUNT:{}".format(
            trade.externalId,
            trade.timestamp,
            trade.timestampNano,
            trade.priceStr,
            trade.amountStr,
        )
        print(trade_msg)


cw.stream.on_trades_update = handle_trades_update


cw.stream.connect()

# Stop receiving after 10 seconds
# time.sleep(10)
# cw.stream.disconnect()
