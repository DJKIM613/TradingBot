import math
from stock_info.stock_informer import *


class trader():
	def __init__(self, investors):
		self.account_manager = db_manager()
		self.data_manager = stock_informer()
		self.investors = investors

	def run(self):
		pass


	def update_price_data(self, universe):
		mapping = {None: 0}
		stock_price_data = universe.loc[:, ['종목코드', '종가']]
		stock_price_data.replace(mapping, inplace=True)
		stock_price_data.rename(columns={'종목코드': 'code', '종가': 'price'}, inplace=True)
		self.account_manager.insert_df_to_db('order', 'stock_price_info', stock_price_data)
