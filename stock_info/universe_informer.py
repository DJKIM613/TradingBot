from database.db_manager import *
from stock_info.crawl_universe import *
from _datetime import *

db_universe = 'stock_info'
db_price_data = 'price_data'
db_order = 'order'


class universe_informer():
	def __init__(self):
		self.db_manager = db_manager()
		self.check_database_exist()
		self.universe_crawler = universe_crawler()

	def get_universe(self, date, sql=None):
		db_name = db_universe
		if sql is None:
			sql = "select * from [{}]".format(date)

		if not self.db_manager.check_table_exist(db_name, date):
			df = self.universe_crawler.crawlUniverse(date)
			df = df[(~df.종목명.str.contains("지주")) & (~df.종목명.str.contains("홀딩스"))]
			self.db_manager.insert_df_to_db('stock_info', date, df)

		else:
			datalist = self.db_manager.execute_sql(db_name, sql).fetchall()
			columns = ['index', '종목코드', '종목명', '종가', '대비', '등락률', 'EPS', 'PER', '선행 EPS', '선행 PER', 'BPS', 'PBR',
			           '주당배당금',
			           '배당수익률']

			df = pd.DataFrame(datalist, columns=columns)
			del df['index']

		return df

	def check_database_exist(self):
		self.db_manager.check_database_exist(db_universe)
		self.db_manager.check_database_exist(db_price_data)
		self.db_manager.check_database_exist(db_order)


if __name__ == "__main__":
	universe_informer = universe_informer()
	start = "2019-01-02"
	end = datetime.now().strftime("%Y-%m-%d")
	for date in pd.date_range(start=start, end=end):
		cur_date = date.to_pydatetime().strftime("%Y%m%d")
		print(cur_date)
		universe_informer.get_universe(cur_date)
