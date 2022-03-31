from api.Kiwoom import *
from util.make_up_universe import *
from database.db_manager import *
from util.time_helper import *

import sys


class backtestTrader(QThread):
	def __init__(self, deposit):
		QThread.__init__(self)
		self.backtest_name = "RSIStrategy"
		self.kiwoom = Kiwoom()
		self.db_manager = db_manager()

		# 유니버스 정보를 담을 딕셔너리
		self.universe = {}

		# 계좌 예수금
		self.deposit = deposit

		# 초기화 함수 성공 여부 확인 변수
		self.is_init_success = False

	def check_and_get_universe(self):
		"""유니버스가 존재하는지 확인하고 없으면 생성하는 함수"""
		if not self.db_manager.check_table_exist(self.strategy_name, 'universe'):
			universe_list = get_universe()
			print(universe_list)
			universe = {}
			# 오늘 날짜를 20210101 형태로 지정
			now = datetime.now().strftime("%Y%m%d")

			# KOSPI(0)에 상장된 모든 종목 코드를 가져와 kospi_code_list에 저장
			kospi_code_list = self.kiwoom.get_code_list_by_market("0")

			# KOSDAQ(10)에 상장된 모든 종목 코드를 가져와 kosdaq_code_list에 저장
			kosdaq_code_list = self.kiwoom.get_code_list_by_market("10")

			for code in kospi_code_list + kosdaq_code_list:
				# 모든 종목 코드를 바탕으로 반복문 수행
				code_name = self.kiwoom.get_master_code_name(code)

				# 얻어온 종목명이 유니버스에 포함되어 있다면 딕셔너리에 추가
				if code_name in universe_list:
					universe[code] = code_name

			# 코드, 종목명, 생성일자자를 열로 가지는 DaaFrame 생성
			universe_df = pd.DataFrame({
				'code': universe.keys(),
				'code_name': universe.values(),
				'created_at': [now] * len(universe.keys())
			})

			# universe라는 테이블명으로 Dataframe을 DB에 저장함
			self.db_manager.insert_df_to_db(self.strategy_name, 'universe', universe_df)

		sql = "select * from universe"
		cur = self.db_manager.execute_sql(self.strategy_name, sql)
		universe_list = cur.fetchall()
		for item in universe_list:
			idx, code, code_name, created_at = item
			self.universe[code] = {
				'code_name': code_name
			}
		print(self.universe)

	def make_price_data(self, code):
		db_name = "Common"
		table_name = code
		if not self.db_manager.check_table_exist(db_name, table_name):
			# price_data = key : time, value : (cur_price)
			price_data = self.kiwoom.get_price_minute_data(code)
			self.db_manager.insert_df_to_db(db_name, table_name, price_data)

		else:
			sql = 'select * from [{}]'.format(table_name)
			cur = self.db_manager.execute_sql(db_name, sql)
			price_data = cur.fetchall()

			timeline = []
			price = []

			for t, p in price_data:
				timeline.append(t)
				price.append(p)

			price_data = pd.DataFrame({'price': price}, index=timeline)

		return price_data


if __name__ == "__main__":
	app = QApplication(sys.argv)
	trader = backtestTrader(10000000)
	trader.make_price_data('000660')

	app.exec_()
