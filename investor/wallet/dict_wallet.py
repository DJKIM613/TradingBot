from investor.wallet.abstract_wallet import *
import numpy as np


class dict_wallet(abstract_wallet):
	def __init__(self, name, deposit):
		super().__init__(name, deposit)
		self.stock_detail = {'open_buy': dict1D(), 'holding_stock': dict1D(), 'open_sell': dict1D()}
		self.stock_abstract = dict1D()

	def get_balance(self) -> float:
		return self.balance

	def increase_balance(self, value: int) -> None:
		self.balance += value

	def get_stock_detail(self) -> dict:
		return self.stock_detail

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


class dict1D(dict):
	def __init__(self):
		super().__init__()

	def __getitem__(self, key):
		val = self.get(key)
		if val is None:
			return np.array((0, 0))
		else:
			return val

	def __setitem__(self, key, value):
		quantity, amount = value
		if quantity == 0:
			self.pop(key)

		else:
			super().__setitem__(key, np.array(value))

	def __len__(self) -> int:
		return super().__len__()
