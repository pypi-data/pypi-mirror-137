from jesse.strategies import Strategy, cached
import jesse.indicators as ta
from jesse import utils


class EmaStrategy(Strategy):
    def should_cancel(self):
        # cancel entry orders if not filled until next candle
        return True

    def should_long(self):
        # go long when the EMA 8 is above the EMA 21
        short_ema = ta.ema(self.candles, 8)
        long_ema = ta.ema(self.candles, 21)
        return short_ema > long_ema

    def go_long(self):
        entry_price = self.price - 10 # limit buy order at $10 below the current price
        qty = utils.size_to_qty(self.capital*0.05, entry_price) # spend only 5% of my total capital
        self.buy = qty, entry_price
        self.take_profit = qty, entry_price*1.2 # take profit at 20% above the entry price
        self.stop_loss = qty, entry_price*0.9 # stop loss at 10% below the entry price

    def should_short(self):
        # return False if you don't want to open short positions
        return False

    def go_short(self):
        pass
