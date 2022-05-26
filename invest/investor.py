from invest.wallet.abstract_wallet import *
from invest.strategy import *
import math

MAX_STOCK_NUM = 10
COMMISION_FEE = 0.00015

open_buy = 'open_buy'
open_sell = 'open_sell'
holding_stock = 'holding_stock'


class Investor:
	def __init__(self, name, wallet, strategy):
		self.name = name
		self.strategy = strategy
		self.wallet = wallet
		self.stock_prices = {}

	def getName(self):
		return self.name

	def getBalance(self):
		return self.wallet.get_balance()

	def updateStockPrices(self, stock_prices):
		self.stock_prices = stock_prices

	def getStockValue(self):
		stock_detail = self.wallet.get_stock_detail()
		stock_value = 0
		for _, amount in stock_detail[open_buy].values():
			stock_value += amount

		for status in [holding_stock, open_sell]:
			for code, (quantity, _) in stock_detail[status].items():
				stock_value += quantity * self.stock_prices[code]

		return stock_value

	def getAccountValue(self):
		return self.getStockValue() + self.wallet.get_balance()

	def wantBuy(self, code, info) -> bool:
		price = info['종가']
		is_under_max_stock_num = self.wallet.get_applied_stock_type_num() < MAX_STOCK_NUM
		if is_under_max_stock_num == False:
			return False

		is_quantity_zero = self.wallet.get_stock_quantity_and_amount(holding_stock, code)[0] == 0
		is_desired_quantity_positive = self.get_desired_quantity(price) > 0
		is_satify_strategy = self.strategy.check_buy_condition(info)
		return is_quantity_zero and is_desired_quantity_positive and is_satify_strategy

	def wantSell(self, code, info) -> bool:
		return self.wallet.get_stock_quantity_and_amount(holding_stock, code)[
			       0] > 0 and self.strategy.check_sell_condition(
			info) == True

	def apply_buy_order(self, code, price, quantity=None) -> (str, int, float):
		if quantity is None:
			quantity = self.get_desired_quantity(price)
		amount = quantity * price
		pay = (1 + COMMISION_FEE) * amount

		if self.getBalance() < pay:
			return None

		self.wallet.increase_stock_quantity_and_amount(open_buy, code, (quantity, amount))
		self.wallet.increase_balance(-pay)
		return (code, price, quantity)

	def confirm_buy_order(self, code, price, quantity) -> None:
		self.wallet.increase_stock_quantity_and_amount(open_buy, code, (-quantity, -quantity * price))
		self.wallet.increase_stock_quantity_and_amount(holding_stock, code, (quantity, quantity * price))

	def apply_sell_order(self, code, price) -> (str, int, float):
		self.wallet.get_stock_quantity_and_amount(holding_stock, code)
		quantity, amount = self.wallet.get_stock_quantity_and_amount(holding_stock, code)
		self.wallet.increase_stock_quantity_and_amount(holding_stock, code, (-quantity, -amount))
		self.wallet.increase_stock_quantity_and_amount(open_sell, code, (quantity, amount))
		return (code, price, quantity)

	def confirm_sell_order(self, code, sell_price, quantity):
		amount = quantity * sell_price
		pay = (1 - COMMISION_FEE) * amount

		self.wallet.increase_stock_quantity_and_amount(open_sell, code, (-quantity, -amount))
		self.wallet.increase_balance(pay)

	def get_desired_quantity(self, price):
		applied_stock_type_num = self.wallet.get_applied_stock_type_num()
		budget = self.wallet.get_balance() / (10 - applied_stock_type_num)
		quantity = math.floor(budget / (price * (1 + COMMISION_FEE)))
		return quantity

	def get_stock_detail(self):
		return self.wallet.get_stock_detail()
