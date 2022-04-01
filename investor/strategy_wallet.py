from database.db_manager import AccountManager

table_quantity_view = 'quantity_view'


class strategy_wallet():
	def __init__(self, name, deposit):
		self.deposit = deposit
		self.name = name

	def get_quantity(self, code):
		account_manager = AccountManager()
		quantity = account_manager.select('order', table_quantity_view, ['quantity'],
		                                  {'strategy_name': self.name, 'code': code}).fetchone()

		if quantity == None:
			quantity = 0
		else:
			quantity = quantity[0]

		return quantity

	def get_deposit(self):
		return self.deposit

	def set_deposit(self, deposit):
		self.deposit = deposit


if __name__ == '__main__':
	wallet = stratey_wallet('python', 100000)
	print(wallet.get_quantity('000660'))
