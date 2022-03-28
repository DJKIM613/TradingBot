import sys
from util.crawl_universe import *
from api.Kiwoom import *

from util.singleton import *


@singleton
class data_manager():
	def __init__(self):
		check_database_exist('universe')
		check_database_exist('price_data')
		self.kiwoom = Kiwoom()

	def get_universe(self, date, sql=None):
		db_name = 'universe'
		if sql is None:
			sql = "select * from [{}]".format(date)

		if not check_table_exist(db_name, date):
			crawlUniverse(date)

		datalist = execute_sql(db_name, sql).fetchall()

		columns = ['index', '종목코드', '종목명', '종가', '대비', '등락률', 'EPS', 'PER', '선행 EPS', '선행 PER', 'BPS', 'PBR', '주당배당금',
		           '배당수익률']

		df = pd.DataFrame(datalist, columns=columns)
		del df['index']

		return df

	def get_price_data(self, code, data_period='minute', sql=None):
		db_name = 'price_data'
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

		if not (check_table_exist(db_name, table_name) and len(execute_sql(db_name, sql).fetchall()) > 0):
			df = get_price_data(code)
			insert_df_to_db(db_name, table_name, df, 'append')

		datalist = execute_sql(db_name, sql).fetchall()
		df = pd.DataFrame(datalist, columns=columns)

		return df


if __name__ == '__main__':
	app = QApplication(sys.argv)

	universe = data_manager()
	df = universe.get_price_data('000660', 'day')

	print(df)
	app.exec_()
