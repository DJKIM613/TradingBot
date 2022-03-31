from util.singleton import *
import sqlite3

root_path = r"C:\Users\spong\PycharmProjects\TradingBot"
database_path = root_path + r"\database"


@singleton
class db_manager():
	def insert(self, db_name, table_name, values={}):
		values = _dict_to_strdict(values)

		sql_colomns = ', '.join(values.keys())
		sql_values = ', '.join(values.values())

		sql = f"insert into {table_name}({sql_colomns}) VALUES({sql_values})"

		self.execute_sql(db_name, sql)

	def update(self, db_name, table_name, set_values={}, where_values={}):
		sql_values = []
		for d in [set_values, where_values]:
			sql_value = ''
			d = _dict_to_strdict(d)

			for key, val in d.items():
				if len(sql_value) != 0:
					sql_value += ' and '

				if len(sql_values) == 0:
					sql_value += f'{key} = {key} + ({val})'
				else:
					sql_value += f'{key} = {val}'

			sql_values.append(sql_value)

		sql = f"update {table_name} set {sql_values[0]} where id = (SELECT id from {table_name} where {sql_values[1]} order by id asc)"
		print(sql)

		self.execute_sql(db_name, sql)

	def check_database_exist(self, db_name):
		with open(database_path + r'\{}.db'.format(db_name), 'a'):
			pass

	def check_table_exist(self, db_name, table_name):
		self.check_database_exist(db_name)
		with sqlite3.connect(database_path + r'\{}.db'.format(db_name)) as con:
			cur = con.cursor()
			sql = "SELECT name FROM sqlite_master WHERE type='table' and name=:table_name"
			cur.execute(sql, {"table_name": table_name})

			if len(cur.fetchall()) > 0:
				return True
			else:
				return False

	def insert_df_to_db(self, db_name, table_name, df, option="replace"):
		self.check_database_exist(db_name)
		with sqlite3.connect(database_path + r'\{}.db'.format(db_name)) as con:
			df.to_sql(table_name, con, if_exists=option)

	def execute_sql(self, db_name, sql, param={}):
		self.check_database_exist(db_name)
		with sqlite3.connect(database_path + r'\{}.db'.format(db_name), isolation_level=None) as con:
			cur = con.cursor()
			cur.execute(sql, param)
			return cur


def _dict_to_strdict(dict):
	for key, value in dict.items():
		if type(value) == str and len(value) > 1 and value[0] == "'" and value[-1] == "'":
			continue
		if type(value) == str:
			dict[key] = f"'{value}'"
		else:
			dict[key] = str(value)

	return dict


if __name__ == '__main__':
	set_values = {'quantity': -5}
	where_values = {'code': '12312', 'price': 13200, 'strategy_name': 'hello'}
	db_manager = db_manager()
	db_manager.update('order', 'open_buy_order', set_values, where_values)
