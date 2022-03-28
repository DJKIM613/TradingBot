import pandas as pd

from strategy.RSIStrategy import *
import sys

# app = QApplication(sys.argv)
#
# rsi_strategy = RSIStrategy()
# rsi_strategy.start()
#
# app.exec_()

value1 = [1, 2, 3, 4, 5]
value2 = [6, 7, 8, 9, 10]
keys = [chr(i) for i in range(ord('a'), ord('f'))]
print(keys)

print(value1)
df = pd.DataFrame(index=keys, data={'value1': value1, 'value2': value2})
print(df)

conn = sqlite3.connect('common.db')
cur = conn.cursor()
# cur.execute(
# 	"CREATE TABLE {} \
# 	(keys varchar(10) PRIMARY KEY, \
# 	value1 int(10) NOT NULL, \
# 	value2 int(10) NOT NULL\
# 	)".format('hihi'))

# with sqlite3.connect('common.db') as conn:
# 	df.to_sql('hihi', con=conn, if_exists='replace')

