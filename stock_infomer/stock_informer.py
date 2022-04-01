import sys
from stock_info.crawl_universe import *
from util.singleton import *
from stock_info.universe_informer import *
from stock_info.single_stock import *


@singleton
class stock_informer():
	def __init__(self):
		self.universe_informer = universe_informer()
		self.single_stock_informer = single_stock_informer()

	def get_universe(self, date, sql=None):
		return self.universe_informer.get_universe(date, sql)

	def get_price_data(self, code, data_period='minute', sql=None):
		return single_stock_informer.get_price_data(code, data_period, sql)


if __name__ == '__main__':
	app = QApplication(sys.argv)

	data_manager = stock_informer()
	select_values = ['quantity'],
	where_values = {'strategy_name': 'python', 'code': '000660'}
	data_manager.process_sell_order('python', '000660', 3, 13000)
	data_manager.process_open_sell_order('python', '000660', 3, 13000)
	# data_manager.process_open_buy_order('python', '000660', 2, 13000)

	print('end')
	app.exec_()
