from investor.wallet.abstract_wallet import *
from database.db_manager import db_manager
import math

MAX_STOCK_NUM = 10

COMMISION_FEE = 0.00015

db_universe = 'universe'
db_price_data = 'price_data'
db_order = 'order'

table_holding_stock = 'holding_stock'
table_open_sell_order = 'open_sell_order'
table_open_buy_order = 'open_buy_order'

holding_and_open_sell_quantity_view = 'holding_and_open_sell_quantity_view'
total_quantity_view = 'total_quantity_view'

stock_tables = [table_holding_stock, table_open_sell_order, table_open_buy_order]


class db_wallet(abstract_wallet):
	def __init__(self, name, deposit):
		super().__init__()
		self.account_manager = db_manager()

	def get_amount(self):
		select_values = ['sum(amount)']
		where_values = {'strategy_name': self.name}
		amount = self.account_manager.select(db_order, holding_and_open_sell_quantity_view, select_values,
		                                     where_values).fetchone()[0]

		if amount == None:
			amount = 0

		return amount

	def get_stock_quantity(self, status, code) -> int:
		def get_holding_quantity(self, code):
			quantity = self.account_manager.select('order', holding_and_open_sell_quantity_view, ['quantity'],
			                                       {'strategy_name': self.name, 'code': code}).fetchone()

			if quantity == None:
				quantity = 0
			else:
				quantity = quantity[0]

			return quantity

	def get_applied_stock_type_num(self):
		select_values = []
		where_values = {'strategy_name': self.name}
		cur = self.account_manager.select(db_order, total_quantity_view, select_values, where_values)
		applied_stock_type_num = len(cur.fetchall())
		return applied_stock_type_num

	def get_holding_quantity(self, code):
		quantity = self.account_manager.select('order', holding_and_open_sell_quantity_view, ['quantity'],
		                                       {'strategy_name': self.name, 'code': code}).fetchone()

		if quantity == None:
			quantity = 0
		else:
			quantity = quantity[0]

		return quantity

	def get_desired_quantity(self, price):
		applied_stock_type_num = self.get_applied_stock_type_num()
		budget = self.balance / (10 - applied_stock_type_num)
		quantity = math.floor(budget / price)
		return quantity

	def get_balance(self):
		return self.balance

	def set_balance(self, value):
		self.balance = value


class dictDB(dict):
	def __init__(self, db_name, table_name, strategy_name):
		super().__init__()
		self.db_name = db_name
		self.table_name = table_name
		self.strategy_name = strategy_name
		self.account_manager = db_manager()

	def __getitem__(self, key):
		value = self.account_manager.select(self.db_name, self.table_name, ['quantity'],
		                                    {'strategy_name': self.strategy_name, 'code': key}).fetchone()

		if value == None:
			value = 0

		return value

	def __setitem__(self, key, value):
		value = self.__getitem__(key)
		if value == 0:
			data = {'strategy_name': self.name, 'code': key, 'quantity': value}
			self.account_manager.insert(self.db_name, self.table_name, data)

		else:
			set_values = {'quantity': value}
			where_values = {'strategy_name': self.name, 'code': key, }
			self.account_manager.update(self.db_name, self.table_name, set_values, where_values)
