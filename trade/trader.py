import math
from stock_info.stock_informer import *


class Trader:
	def __init__(self, dealer):
		self.data_manager = stock_informer()
		self.investors = {}
		self.dealer = dealer

	def addInvestor(self, investor):
		self.investors[investor.getName()] = investor

	def removeInvestor(self, name):
		self.investors.pop(name, None)

	def showInvestorInfo(self, names=None):
		if names is None:
			names = self.investors

		messages = []
		for name in names:
			info = self.investors[name].get_stock_detail()
			msg = f'{name} : {info}'
			messages.append(msg)

		return messages

	def applyBuy(self, name, code, quantity, price=None):
		self.investors[name].apply_buy_order(code, price, quantity)
		apply_result = self.dealer.applyBuy(code, price, quantity)
		if apply_result is True:
			self.investors[name].confirm_buy_order(code, price, quantity)
		else:
			raise NotImplementedError

	def applySell(self, name, code=None, quantity=None, price=None):
		self.investors[name].apply_sell_order(code, price, quantity)
		apply_result = self.dealer.applySell(code, price, quantity)
		if apply_result is True:
			self.investors[name].confirm_sell_order(code, price, quantity)
		else:
			raise NotImplementedError

	def run(self):
		pass
