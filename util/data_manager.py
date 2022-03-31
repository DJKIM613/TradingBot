import sys
from util.crawl_universe import *
from api.Kiwoom import *

from database.db_manager import *
from util.singleton import *

db_universe = 'universe'
db_price_data = 'price_data'
db_order = 'order'

table_holding_stock = 'holding_stock'
table_open_sell_order = 'open_sell_order'
table_open_buy_order = 'open_buy_order'


@singleton
class data_manager():
	def __init__(self):
		self.kiwoom = Kiwoom()
		self.db_manager = db_manager()

		self.db_manager.check_database_exist(db_universe)
		self.db_manager.check_database_exist(db_price_data)
		self.db_manager.check_database_exist(db_order)

	def get_universe(self, date, sql=None):
		db_name = db_universe
		if sql is None:
			sql = "select * from [{}]".format(date)

		if not self.db_manager.check_table_exist(db_name, date):
			crawlUniverse(date)

		datalist = self.db_manager.execute_sql(db_name, sql).fetchall()

		columns = ['index', '종목코드', '종목명', '종가', '대비', '등락률', 'EPS', 'PER', '선행 EPS', '선행 PER', 'BPS', 'PBR', '주당배당금',
		           '배당수익률']

		df = pd.DataFrame(datalist, columns=columns)
		del df['index']

		return df

	def get_price_data(self, code, data_period='minute', sql=None):
		db_name = db_price_data
		if data_period == 'minute':
			table_name = 'M' + code
			get_price_data = self.kiwoom.get_price_minute_data
			columns = ['timeline', 'price']
		else:
			table_name = 'D' + code
			get_price_data = self.kiwoom.get_price_data
			columns = ['timeline', 'open', 'high', 'low', 'close', 'volume']

		if sql is None:
			sql = "select * from [{}]".format(table_name)

		if not (self.db_manager.check_table_exist(db_name, table_name) and len(self.db_manager.execute_sql(db_name, sql).fetchall()) > 0):
			df = get_price_data(code)
			self.db_manager.insert_df_to_db(db_name, table_name, df, 'append')

		datalist = self.db_manager.execute_sql(db_name, sql).fetchall()
		df = pd.DataFrame(datalist, columns=columns)

		return df

	def process_buy_order(self, strategy_name, code, quantity, price):
		data = {'code': code, 'quantity': quantity, 'price': price, 'strategy_name': strategy_name}
		self.db_manager.insert(db_order, table_open_buy_order, data)

	def process_sell_order(self, strategy_name, code, quantity, price):
		data = {'code': code, 'quantity': quantity, 'price': price, 'strategy_name': strategy_name}
		self.db_manager.insert(db_order, table_open_sell_order, data)

	def process_open_buy_order(self, strategy_name, code, quantity, purchase_price):
		data = {'code': code, 'quantity': quantity, 'purchase_price': purchase_price, 'strategy_name': strategy_name}
		set_values = {'quantity': -quantity}
		where_values = {'code': code, 'price': purchase_price, 'strategy_name': strategy_name}

		self.db_manager.insert(db_order, table_holding_stock, data)
		self.db_manager.update(db_order, table_open_buy_order, set_values, where_values)

	def process_open_sell_order(self, strategy_name, code, quantity, sell_price):
		set_values = {'quantity': -quantity}
		where_values = {'code': code, 'strategy_name': strategy_name}

		self.db_manager.update(db_order, table_holding_stock, set_values, where_values)
		self.db_manager.update(db_order, table_open_sell_order, set_values, where_values)


if __name__ == '__main__':
	app = QApplication(sys.argv)

	data_manager = data_manager()
	data_manager.process_sell_order('python', '000660', 3, 13000)
	data_manager.process_open_sell_order('python', '000660', 3, 13000)
	# data_manager.process_open_buy_order('python', '000660', 2, 13000)

	print('end')
	app.exec_()
