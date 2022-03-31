from util.data_manager import *

from PyQt5.QtWidgets import *

import sys
from datetime import *
import time
import pandas as pd

from util.indicator_caculator import *

app = QApplication(sys.argv)

# 1. 일별로 universe 요청
start = "2018-01-01"
end = datetime.now().strftime("%Y-%m-%d")
for date in pd.date_range(start=start, end=end):
	cur_date = date.to_pydatetime().strftime("%Y%m%d")
	# print(date.to_pydatetime().strftime("%Y%m%d"))
	data = data_manager()
	df = data.get_universe(cur_date)
	print(df)

	# 2. 일봉 데이터 요청 data_manager
	for code in df['종목코드'][0:3]:
		print(code)
		price_data = data.get_price_data(code=code, data_period='day')

		rsi = indicator_caculator().RSI(price_data, 2)
		print(rsi)

		time.sleep(10)
# 3. RSI(2)
app.exec_()
