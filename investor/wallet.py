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


class wallet():
	def __init__(self, name, deposit):
		self.balance = deposit
		self.name = name
		self.account_manager = db_manager()

	def check_buy_condition(self, code, price):
		return self.get_applied_stock_type_num() < MAX_STOCK_NUM and self.get_holding_quantity(
			code) == 0 and self.get_desired_quantity(price) > 0

	def check_sell_condition(self, code):
		return self.get_holding_quantity(code) > 0

	def apply_buy_order(self, code, info):
		price = info['종가']
		quantity = self.get_desired_quantity(price)
		amount = quantity * price * (1 + COMMISION_FEE)
		data = {'code': code, 'quantity': quantity, 'price': price, 'strategy_name': self.name}

		self.account_manager.insert(db_order, table_open_buy_order, data)
		self.balance -= amount
		return (code, price, quantity)

	def confirm_buy_order(self, code, purchase_price, quantity):
		data = {'code': code, 'quantity': quantity, 'purchase_price': purchase_price,
		        'strategy_name': self.name}
		set_values = {'quantity': -quantity}
		where_values = {'code': code, 'price': purchase_price, 'strategy_name': self.name}

		self.account_manager.insert(db_order, table_holding_stock, data)
		self.account_manager.increase(db_order, table_open_buy_order, set_values, where_values)

	def apply_sell_order(self, code, info):
		price = info['종가']
		quantity = self.get_holding_quantity(code)
		set_values = {'quantity': -quantity}
		where_values = {'code': code, 'strategy_name': self.name}
		self.account_manager.increase(db_order, table_holding_stock, set_values, where_values)

		data = {'code': code, 'quantity': quantity, 'price': price, 'strategy_name': self.name}
		self.account_manager.insert(db_order, table_open_sell_order, data)
		return (code, price, quantity)

	def confirm_sell_order(self, code, sell_price, quantity):
		set_values = {'quantity': -quantity}
		where_values = {'code': code, 'strategy_name': self.name}
		self.account_manager.increase(db_order, table_open_sell_order, set_values, where_values)

		amount = quantity * sell_price * (1 - COMMISION_FEE)
		self.balance += amount
		return amount

	def get_amount(self):
		select_values = ['sum(amount)']
		where_values = {'strategy_name': self.name}
		amount = self.account_manager.select(db_order, holding_and_open_sell_quantity_view, select_values,
		                                     where_values).fetchone()[0]

		if amount == None:
			amount = 0

		return amount

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


if __name__ == '__main__':
	wallet = wallet('python', 100000)
	print(wallet.get_holding_quantity('000660'))
