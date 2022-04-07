from trader import *
from PyQt5.QtWidgets import *
import sys

from datetime import *

from investor.investor import *
from investor.wallet.dict_wallet import *


class backtestTrader(trader):
	def __init__(self, investors={}):
		super().__init__(investors)

	def run(self):
		start = "2019-01-02"
		end = datetime.now().strftime("%Y-%m-%d")

		for date in pd.date_range(start=start, end=end):
			cur_date = date.to_pydatetime().strftime("%Y%m%d")
			universe = self.data_manager.get_universe(cur_date)
			if not self.is_market_open(universe):
				continue

			stock_info = universe.set_index('종목코드').to_dict('index')
			stock_prices = universe.set_index('종목코드')['종가']
			for investor in self.investors:
				print(f'{cur_date} : {investor.getAccountValue()}')
				investor.updateStockPrices(stock_prices)

				for code, info in stock_info.items():
					if investor.wantSell(code, info):
						(code, price, quantity) = investor.apply_sell_order(code, info)
						investor.confirm_sell_order(code, price, quantity)
						print(f'{date} : sell {code}, {info["PER"]}, {price}')

					if investor.wantBuy(code, info):
						(code, price, quantity) = investor.apply_buy_order(code, info)
						investor.confirm_buy_order(code, quantity)
						print(f'{date} : buy {code}, {info["PER"]}, {price}')

	def is_market_open(self, universe):
		return universe['종가'][0] is not None


if __name__ == "__main__":
	app = QApplication(sys.argv)
	name = 'RSI7'
	RSI_strategy = strategy(name, '', '')
	wallet = dict_wallet(name, 1000000)
	investor = investor(name, wallet, RSI_strategy)
	trader = backtestTrader([investor, ])
	trader.run()
	app.exec_()
