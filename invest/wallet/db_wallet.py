from invest.wallet.abstract_wallet import *
from database.db_manager import db_manager
import numpy as np

MAX_STOCK_NUM = 10

db_name = 'order'
table_list = ['open_buy', 'holding_stock', 'open_sell', 'stock_abstract']
column_list = ['strategy_name', 'code', 'quantity', 'amount']


class db_wallet(abstract_wallet):
	def __init__(self, name, deposit):
		super().__init__(name, deposit)
		self.stock_detail = {'open_buy': dictDB(db_name, 'open_buy', name),
		                     'holding_stock': dictDB(db_name, 'holding_stock', name),
		                     'open_sell': dictDB(db_name, 'open_sell', name)}
		self.stock_abstract = dictDB(db_name, 'stock_abstract', name)

	def get_balance(self) -> float:
		return self.balance

	def increase_balance(self, value: int) -> None:
		self.balance += value

	def get_stock_detail(self) -> dict:
		ret = self.stock_detail.copy()
		for key in self.stock_detail:
			ret[key] = self.stock_detail[key].todict()

		return ret

	def get_stock_quantity_and_amount(self, status: str, code: str) -> (int, float):
		return tuple(self.stock_detail[status][code])

	def set_stock_quantity_and_amount(self, status: str, code: str, value: (int, float)) -> None:
		diff = value - self.stock_detail[status][code]
		self.stock_detail[status][code] = value
		self.stock_abstract[code] += diff

	def increase_stock_quantity_and_amount(self, status: str, code: str, value: (int, float)) -> None:
		self.stock_detail[status][code] += value
		self.stock_abstract[code] += value

	def get_applied_stock_type_num(self) -> int:
		return len(self.stock_abstract)


class dictDB(dict):
	def __init__(self, db_name, table_name, strategy_name):
		super().__init__()
		self.db_name = db_name
		self.table_name = table_name
		self.strategy_name = strategy_name
		self.account_manager = db_manager()

	def __getitem__(self, key):
		value = self.account_manager.select(self.db_name, self.table_name, ['quantity', 'amount'],
		                                    {'strategy_name': self.strategy_name, 'code': key}).fetchone()

		if value == None:
			value = np.array((0, 0.0))

		return np.array(value)

	def __setitem__(self, key, value) -> None:
		(old_quantity, old_amount) = self.__getitem__(key)
		(new_quantity, new_amount) = value
		if old_quantity == 0:
			data = {'strategy_name': self.strategy_name, 'code': key, 'quantity': new_quantity, 'amount': new_amount}
			self.account_manager.insert(self.db_name, self.table_name, data)

		else:
			set_values = {'quantity': new_quantity, 'amount': new_amount}
			where_values = {'strategy_name': self.strategy_name, 'code': key, }
			self.account_manager.update(self.db_name, self.table_name, set_values, where_values)

	def __len__(self) -> int:
		self.account_manager.select(self.db_name, self.table_name).fetchall()
		return len(self.account_manager.select(self.db_name, self.table_name).fetchall())

	def todict(self) -> dict:
		raw_data = self.account_manager.select(self.db_name, self.table_name).fetchall()
		data = {code: (quantity, amount) for (index, name, code, quantity, amount) in raw_data}
		return data
