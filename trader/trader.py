import math
from database.db_manager import *
from util.data_manager import *
from investor.investor import *

MAX_STOCK_NUM = 10
COMMISION_FEE = 0.00015

db_universe = 'universe'
db_price_data = 'price_data'
db_order = 'order'

table_holding_stock = 'holding_stock'
table_open_sell_order = 'open_sell_order'
table_open_buy_order = 'open_buy_order'

stock_tables = [table_holding_stock, table_open_sell_order, table_open_buy_order]


class trader():
	def __init__(self, deposit, investors):
		self.balance = deposit
		self.account_manager = AccountManager()
		self.data_manager = data_manager()
		self.investors = investors

	def run(self):
		pass

	def check_buy_condition(self):
		return (self.get_balance_count() + self.get_buy_order_count()) >= 10

	def get_total_amount(self):
		select_values = ["sum(quantity * price)", ]
		where_values = {}

		total_amount = self.balance
		for stock_table in stock_tables:
			total_amount = total_amount + self.account_manager.select(db_order, stock_table, select_values,
			                                                          where_values)

		return total_amount

	def get_quantity(self, price):
		budget = self.balance / (10 - (self.get_balance_count() + self.get_buy_order_count()))
		quantity = math.floor(budget / price)
		return quantity

	def apply_buy_order(self, strategy_name, code, price):
		if self.check_buy_condition():
			return False

		quantity = self.get_quantity(price)
		amount = quantity * price
		self.balance = math.floor(self.balance - amount * (1 + COMMISION_FEE))

		data = {'code': code, 'quantity': quantity, 'price': price, 'strategy_name': strategy_name}
		self.db_manager.insert(db_order, table_open_buy_order, data)
		return quantity

	def confirm_buy_order(self, strategy_name, code, quantity, purchase_price):
		data = {'code': code, 'quantity': quantity, 'purchase_price': purchase_price,
		        'strategy_name': strategy_name}
		set_values = {'quantity': -quantity}
		where_values = {'code': code, 'price': purchase_price, 'strategy_name': strategy_name}

		self.db_manager.insert(db_order, table_holding_stock, data)
		self.db_manager.update(db_order, table_open_buy_order, set_values, where_values)

	def apply_sell_order(self, strategy_name, code, quantity, price):
		set_values = {'quantity': -quantity}
		where_values = {'code': code, 'strategy_name': strategy_name}
		self.db_manager.update(db_order, table_holding_stock, set_values, where_values)

		data = {'code': code, 'quantity': quantity, 'price': price, 'strategy_name': strategy_name}
		self.db_manager.insert(db_order, table_open_sell_order, data)

	def confirm_sell_order(self, strategy_name, code, quantity, sell_price):
		set_values = {'quantity': -quantity}
		where_values = {'code': code, 'strategy_name': strategy_name}
		self.db_manager.update(db_order, table_open_sell_order, set_values, where_values)

		amount = quantity * sell_price
		self.balance = math.floor(self.balance + amount * (1 + COMMISION_FEE))
