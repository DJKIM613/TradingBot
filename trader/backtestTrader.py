from trader import *
from PyQt5.QtWidgets import *
import sys

from datetime import *
import pandas as pd

from investor.investor import *
from investor.strategy import *
class backtestTrader(trader):
	def __init__(self, deposit, investors={}):
		super().__init__(deposit, investors)

	def run(self):
		start = "2019-01-02"
		end = datetime.now().strftime("%Y-%m-%d")
		for date in pd.date_range(start=start, end=end):
			cur_date = date.to_pydatetime().strftime("%Y%m%d")
			universe = self.data_manager.get_universe(cur_date)
			universe = universe.set_index('종목코드').to_dict('index')
			for investor in self.investors:
				for code, info in universe.items():
					price = info['종가']
					if investor.wantSell(code, info):
						print(code, info['PER'], price)
						quantity = investor.getQuantity(code)
						self.apply_sell_order(strategy.name, code, quantity, price)
						self.confirm_sell_order(strategy.name, code, quantity, price)

					if investor.wantBuy(code, info):
						print(code, info['PER'], price)
						quantity = self.apply_buy_order(strategy.name, code, price)
						self.confirm_buy_order(strategy.name, code, quantity, price)


if __name__ == "__main__":
	app = QApplication(sys.argv)
	RSI_strategy = strategy('RSI', '', '', 1000000)
	investor = investor('RSI', RSI_strategy, 1000000)
	trader = backtestTrader(1000000, [investor,])
	trader.run()
	app.exec_()
