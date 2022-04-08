from trader import *
from PyQt5.QtWidgets import *
import sys

from investor.investor import *
from investor.wallet.db_wallet import *
from investor.wallet.dict_wallet import *
from pykrx import stock


class backtestTrader(trader):
	def __init__(self, investors={}):
		super().__init__(investors)

	def run(self, fromdate, todate):
		for date in stock.get_previous_business_days(fromdate=fromdate, todate=todate):
			cur_date = date.strftime("%Y%m%d")
			universe = self.data_manager.get_universe(cur_date)

			stock_info = universe.to_dict('index')
			stock_prices = universe['종가']
			for investor in self.investors:
				investor.updateStockPrices(stock_prices)
				print(f'{cur_date} : {investor.getAccountValue()}')
				for code, info in stock_info.items():
					if investor.wantSell(code, info):
						(code, price, quantity) = investor.apply_sell_order(code, info)
						investor.confirm_sell_order(code, price, quantity)
						print(f'{date} : sell (code :{code}, PER: {info["PER"]}, price: {price}, quantity: {quantity})')

					if investor.wantBuy(code, info):
						(code, price, quantity) = investor.apply_buy_order(code, info)
						investor.confirm_buy_order(code, price, quantity)
						print(f'{date} : buy (code :{code}, PER: {info["PER"]}, price: {price}, quantity: {quantity})')


if __name__ == "__main__":
	app = QApplication(sys.argv)
	name = 'RSI7'
	RSI_strategy = strategy(name, '', '')
	db_wallet = db_wallet(name, 1000000)
	dict_wallet = dict_wallet(name, 1000000)
	investor = investor(name, dict_wallet, RSI_strategy)
	trader = backtestTrader([investor, ])
	trader.run('20190101', '20220407')
	app.exec_()
