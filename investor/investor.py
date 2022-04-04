from investor.strategy import *
from investor.wallet import *


class investor():
	def __init__(self, name, strategy, deposit):
		self.name = name
		self.strategy = strategy
		self.strategy_wallet = wallet(name, deposit)

	def getName(self):
		return self.name

	def wantBuy(self, code, info):
		if self.strategy_wallet.check_buy_condition(code) == True and self.strategy.check_buy_condition(
				info) == True:
			amount = self.strategy_wallet.get_desired_quantity(info['종가'])
			return amount

		else:
			return 0

	def wantSell(self, code, info):
		if self.strategy_wallet.check_sell_condition(code) == True and self.strategy.check_sell_condition(
				info) == True:
			return self.strategy_wallet.get_quantity(code)

		else:
			return 0
