from strategy import *
from strategy.strategy_wallet import *


class investor():
	def __init__(self, name, strategy, deposit):
		self.strategy = strategy
		self.strategy_wallet = strategy_wallet(name, deposit)

	def wantBuy(self, code, info):
		return self.strategy_wallet.get_quantity == 0 and self.strategy.check_buy_condition(info) == True

	def wantSell(self, code, info):
		return self.strategy_wallet.get_quantity(code) > 0 and self.strategy.check_sell_condition(info) == True

	def getQuantity(self, code):
		return self.strategy_wallet.get_quantity(code)
