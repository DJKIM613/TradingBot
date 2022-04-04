from trader import *
from PyQt5.QtWidgets import *
import sys

from datetime import *
import pandas as pd

from investor.investor import *
from investor.strategy import *


class backtestTrader(trader):
	def __init__(self, investors={}):
		super().__init__(investors)

	def run(self):
		start = "2019-01-02"
		end = datetime.now().strftime("%Y-%m-%d")
		for date in pd.date_range(start=start, end=end):
			cur_date = date.to_pydatetime().strftime("%Y%m%d")
			universe = self.data_manager.get_universe(cur_date)
			self.update_price_data(universe)

			universe = universe.set_index('종목코드').to_dict('index')

			for investor in self.investors:
				print(cur_date, investor.getAccountValue())
				for code, info in universe.items():
					price = info['종가']
					quantity = investor.wantSell(code, info)
					if quantity != 0:
						print(f'{date} : sell {code}, {info["PER"]}, {price}')
						self.apply_sell_order(investor.getName(), code, quantity, price)
						pay = self.confirm_sell_order(investor.getName(), code, quantity, price)
						investor.setBalance(investor.getBalance() + pay)

					quantity = investor.wantBuy(code, info)
					if quantity != 0:
						print(f'{date} : buy {code}, {info["PER"]}, {price}')
						pay = self.apply_buy_order(investor.getName(), code, quantity, price)
						investor.setBalance(investor.getBalance() - pay)
						self.confirm_buy_order(investor.getName(), code, quantity, price)

	def update_price_data(self, universe):
		mapping = {None: 0}
		stock_price_data = universe.loc[:, ['종목코드', '종가']]
		stock_price_data.replace(mapping, inplace=True)
		stock_price_data.rename(columns={'종목코드': 'code', '종가': 'price'}, inplace=True)
		self.account_manager.insert_df_to_db('order', 'stock_price_info', stock_price_data)


if __name__ == "__main__":
	app = QApplication(sys.argv)
	RSI_strategy = strategy('RSI7', '', '', 1000000)
	investor = investor('RSI7', RSI_strategy, 1000000)
	trader = backtestTrader([investor, ])
	trader.run()
	app.exec_()
