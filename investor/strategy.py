import pandas as pd


class strategy():
	def __init__(self, name, buy_condition, sell_condition, deposit):
		self.name = name
		self.buy_condition = parse_condition(buy_condition)
		self.sell_condition = parse_condition(sell_condition)
		self.deposit = deposit

	def get_name(self):
		return self.name

	def check_code_exist(self, code):
		return False

	def check_buy_condition(self, info):
		if pd.isna(info['PER']):
			return False
		return 7.9 < info['PER'] < 8

	def check_sell_condition(self, info):
		if pd.isna(info['PER']):
			return False
		return info['PER'] > 8.1


def parse_condition(condition_sentence):
	return ''
