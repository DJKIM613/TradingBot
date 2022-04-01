from api.Kiwoom import *
from database.db_manager import *

db_price_data = 'price_data'


class single_stock_informer():
	def __init__(self):
		self.kiwoom = Kiwoom()
		self.db_manager = db_manager

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

		if not (self.db_manager.check_table_exist(db_name, table_name) and len(
				self.db_manager.execute_sql(db_name, sql).fetchall()) > 0):
			df = get_price_data_from_kiwoom(code)
			self.db_manager.insert_df_to_db(db_name, table_name, df, 'append')

		datalist = self.db_manager.execute_sql(db_name, sql).fetchall()
		df = pd.DataFrame(datalist, columns=columns)

		return df
