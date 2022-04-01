from util.singleton import *
import sqlite3

root_path = r"C:\Users\spong\PycharmProjects\TradingBot"
database_path = root_path + r"\database"


@singleton
class db_manager():
	def select(self, db_name, table_name, select_values=[], where_values={}):
		select_clause = get_simple_condition(select_values)
		where_clause = get_where_condition(_dict_to_strdict(where_values))

		sql = f"select {select_clause} from {table_name} {where_clause}"
		return self.execute_sql(db_name, sql)

	def insert(self, db_name, table_name, values={}):
		values = _dict_to_strdict(values)

		into_clause = get_simple_condition(values.keys())
		values_clause = get_simple_condition(values.values())

		sql = f"insert into {table_name}({into_clause}) VALUES({values_clause})"

		self.execute_sql(db_name, sql)

	def update(self, db_name, table_name, set_values={}, where_values={}):
		set_cluase = get_set_clause(_dict_to_strdict(set_values))
		where_cluase = get_where_condition(_dict_to_strdict(where_values))

		sql = f"update {table_name} set {set_cluase} where id = (SELECT id from {table_name} {where_cluase} order by id asc)"

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


def get_simple_condition(list):
	clause = ''
	if len(list) == 0:
		clause += '*'
	else:
		clause += ', '.join(list)
	return clause


def get_set_clause(dict):
	clause = ''
	for key, val in dict.items():
		if len(clause) != 0:
			clause += ' and '
		clause += f'{key} = {key} + {val}'

	return clause


def get_where_condition(dict):
	if len(dict) == 0:
		return ''

	clause = 'where '
	init_length = len(clause)
	for key, val in dict.items():
		if len(clause) != init_length:
			clause += ' and '
		clause += f'{key} = {val}'

	return clause


def _dict_to_strdict(dict):
	ret = dict.copy()
	for key, value in ret.items():
		if type(value) == str:
			ret[key] = f"'{value}'"
		else:
			ret[key] = str(value)

	return ret


if __name__ == '__main__':
	set_values = {'quantity': -5}
	where_values = {'code': '12312', 'price': 13200, 'strategy_name': 'hello'}

	account_manager = db_manager()
	quantity = account_manager.select('order', 'holding_stock', set_values, where_values)
	account_manager.update('order', 'open_buy_order', set_values, where_values)
