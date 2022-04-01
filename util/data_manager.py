import sys
from universe.crawl_universe import *
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
		self.account_manager = AccountManager()

		self.account_manager.check_database_exist(db_universe)
		self.account_manager.check_database_exist(db_price_data)
		self.account_manager.check_database_exist(db_order)

	def get_universe(self, date, sql=None):
		db_name = db_universe
		if sql is None:
			sql = "select * from [{}]".format(date)

		if not self.account_manager.check_table_exist(db_name, date):
			crawlUniverse(date)

		datalist = self.account_manager.execute_sql(db_name, sql).fetchall()

		columns = ['index', '종목코드', '종목명', '종가', '대비', '등락률', 'EPS', 'PER', '선행 EPS', '선행 PER', 'BPS', 'PBR', '주당배당금',
		           '배당수익률']

		df = pd.DataFrame(datalist, columns=columns)
		del df['index']

		return df

	def get_price_data(self, code, data_period='minute', sql=None):
		db_name = db_price_data
		if data_period == 'minute':
			table_name = 'M' + code
			get_price_data_from_kiwoom = self.kiwoom.get_price_minute_data
			columns = ['timeline', 'price']
		else:
			table_name = 'D' + code
			get_price_data_from_kiwoom = self.kiwoom.get_price_data
			columns = ['timeline', 'open', 'high', 'low', 'close', 'volume']

		if sql is None:
			sql = "select * from [{}]".format(table_name)

		if not (self.account_manager.check_table_exist(db_name, table_name) and len(
				self.account_manager.execute_sql(db_name, sql).fetchall()) > 0):
			df = get_price_data_from_kiwoom(code)
			self.account_manager.insert_df_to_db(db_name, table_name, df, 'append')

		datalist = self.account_manager.execute_sql(db_name, sql).fetchall()
		df = pd.DataFrame(datalist, columns=columns)

		return df


if __name__ == '__main__':
	app = QApplication(sys.argv)

	data_manager = data_manager()
	select_values = ['quantity'],
	where_values = {'strategy_name': 'python', 'code': '000660'}
	data_manager.process_sell_order('python', '000660', 3, 13000)
	data_manager.process_open_sell_order('python', '000660', 3, 13000)
	# data_manager.process_open_buy_order('python', '000660', 2, 13000)

	print('end')
	app.exec_()
