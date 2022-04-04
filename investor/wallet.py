from database.db_manager import db_manager
import math

MAX_STOCK_NUM = 10

db_order = 'order'

holding_and_open_sell_quantity_view = 'holding_and_open_sell_quantity_view'
total_quantity_view = 'total_quantity_view'


class wallet():
	def __init__(self, name, deposit):
		self.balance = deposit
		self.name = name
		self.account_manager = db_manager()

	def get_amount(self):
		select_values = ['sum(amount)']
		where_values = {'strategy_name': self.name}
		amount = self.account_manager.select(db_order, holding_and_open_sell_quantity_view, select_values,
		                                     where_values).fetchone()[0]

		if amount == None:
			amount = 0

		return amount

	def get_account_value(self):
		return self.balance + self.get_amount()

	def get_applied_stock_type_num(self):
		select_values = []
		where_values = {'strategy_name': self.name}
		cur = self.account_manager.select(db_order, total_quantity_view, select_values, where_values)
		applied_stock_type_num = len(cur.fetchall())
		return applied_stock_type_num

	def get_quantity(self, code):
		quantity = self.account_manager.select('order', holding_and_open_sell_quantity_view, ['quantity'],
		                                       {'strategy_name': self.name, 'code': code}).fetchone()

		if quantity == None:
			quantity = 0
		else:
			quantity = quantity[0]

		return quantity

	def check_buy_condition(self, code):
		return self.get_applied_stock_type_num() < MAX_STOCK_NUM and self.get_quantity(code) == 0

	def check_sell_condition(self, code):
		return self.get_quantity(code) > 0

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
	print(wallet.get_quantity('000660'))
