class abstract_wallet():
	def __init__(self, name, deposit):
		self.name = name
		self.balance = deposit
		self.amount = 0
		self.stock_detail = {}
		self.stock_abstract = {}

	def get_balance(self) -> float:
		pass

	def increase_balance(self, value) -> None:
		pass

	def get_stock_detail(self) -> dict:
		pass

	def get_amount(self) -> int:
		pass

	def get_stock_quantity_and_amount(self, status: str, code: str) -> (int, float):
		pass

	def set_stock_quantity_and_amount(self, status: str, code: str, value: (int, float)) -> None:
		pass

	def increase_stock_quantity_and_amount(self, status: str, code: str, value: (int, float)) -> None:
		pass

	def get_applied_stock_type_num(self) -> int:
		pass
