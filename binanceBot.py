from binance import Client


class BinanceBot():
    def __init__(self, binance_api_key, binance_api_secret):
        self.client = Client(binance_api_key=binance_api_key, binance_api_secret=binance_api_secret)

    def getBalance(self, asset):
        return self.client.get_asset_balance(asset=self.asset)

    def getPrice(self, asset):
        return self.client.get_symbol_ticker(symbol=f"{self.asset}USDT")["price"]

    def buy(self, asset, quantity):
        usdtBalance = self.client.get_asset_balance(asset='USDT').get('free')
        buy_limit = self.client.order_limit_buy(symbol=self.asset + 'USDT', quantity=min(usdtBalance, quantity), price=self.getPrice())
        return min(usdtBalance, quantity), usdtBalance

    def sell(self, asset, quantity):
        cryptoBalance = self.client.get_asset_balance(asset=self.asset).get('free')
        market_order = self.client.order_market_sell(symbol=self.asset + "USDT", quantity=min(cryptoBalance, quantity))
        return min(cryptoBalance, quantity), cryptoBalance