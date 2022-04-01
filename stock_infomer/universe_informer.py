from api.Kiwoom import *
from database import db_manager
from stock_info.crawl_universe import *

db_universe = 'stock_infomer'
db_price_data = 'price_data'
db_order = 'order'


class universe_informer():
	def __init__(self):
		self.kiwoom = Kiwoom()
		self.db_manager = db_manager()
		self.check_database_exist()

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

	def check_database_exist(self):
		self.db_manager.check_database_exist(db_universe)
		self.db_manager.check_database_exist(db_price_data)
		self.db_manager.check_database_exist(db_order)
