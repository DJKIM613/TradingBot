from database.db_manager import *
from stock_info.crawl_universe import *
from pykrx import stock

db_universe = 'stock_info'
db_price_data = 'price_data'
db_order = 'order'


class universe_informer():
	def __init__(self):
		self.db_manager = db_manager()
		self.check_database_exist()

	def get_universe(self, date, sql=None):
		db_name = db_universe
		if sql is None:
			sql = "select * from [{}]".format(date)

		if not self.db_manager.check_table_exist(db_name, date):
			ohlcv = stock.get_market_ohlcv(date, 'ALL')
			fundamental = stock.get_market_fundamental(date)

			df = pd.concat([ohlcv, fundamental], axis=1)
			self.db_manager.insert_df_to_db('stock_info', date, df)

		else:
			datalist = self.db_manager.execute_sql(db_name, sql).fetchall()
			columns = ['티커', '시가', '고가', '저가', '종가', '거래량', '거래대금', '등락률', 'BPS', 'PER', 'PBR', 'EPS', 'DIV', 'DPS']

			df = pd.DataFrame(datalist, columns=columns)
			df = df.set_index('티커')

		return df

	def check_database_exist(self):
		self.db_manager.check_database_exist(db_universe)
		self.db_manager.check_database_exist(db_price_data)
		self.db_manager.check_database_exist(db_order)


if __name__ == "__main__":
	universe_informer = universe_informer()
	business_days = stock.get_previous_business_days(fromdate="20190102", todate="20221231")
	for date in business_days:
		print(date.strftime("%Y%m%d"))
# start = "2019-01-02"
# end = datetime.now().strftime("%Y-%m-%d")
# for date in pd.date_range(start=start, end=end):
# 	cur_date = date.to_pydatetime().strftime("%Y%m%d")
# 	print(cur_date)
# 	df = universe_informer.get_universe(cur_date)
# 	print(df)
