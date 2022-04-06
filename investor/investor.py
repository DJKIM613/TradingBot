from investor.strategy import *
from investor.wallet import *


class investor():
	def __init__(self, name, strategy, deposit):
		self.name = name
		self.strategy = strategy
		self.strategy_wallet = wallet(name, deposit)

	def getName(self):
		return self.name

	def getAccountValue(self):
		return self.strategy_wallet.get_amount() + self.strategy_wallet.get_balance()

	def wantBuy(self, code, info):
		price = info['종가']
		return self.strategy_wallet.check_buy_condition(code, price) == True and self.strategy.check_buy_condition(
			info) == True

	def wantSell(self, code, info):
		return self.strategy_wallet.check_sell_condition(code) == True and self.strategy.check_sell_condition(
			info) == True

	def apply_buy_order(self, code, info):
		return self.strategy_wallet.apply_buy_order(code, info)

	def confirm_buy_order(self, code, purchase_price, quantity):
		self.strategy_wallet.confirm_buy_order(code, purchase_price, quantity)

	def apply_sell_order(self, code, info):
		return self.strategy_wallet.apply_sell_order(code, info)

	def confirm_sell_order(self, code, sell_price, quantity):
		self.strategy_wallet.confirm_sell_order(code, sell_price, quantity)
