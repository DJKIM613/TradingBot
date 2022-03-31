import math


class trader():
	def __init__(self, deposit):
		self.deposit = deposit

	def run(self):
		"""실질적 수행 역할을 하는 함수"""
		while self.is_init_success:
			try:
				# (0)장중인지 확인
				if not check_transaction_open():
					print("장시간이 아니므로 5분간 대기합니다.")
					time.sleep(5 * 60)
					continue

				for idx, code in enumerate(self.universe.keys()):
					print('[{}/{}_{}]'.format(idx + 1, len(self.universe), self.universe[code]['code_name']))
					time.sleep(0.5)

					# (1)접수한 주문이 있는지 확인
					if code in self.kiwoom.order.keys():
						# (2)주문이 있음
						print('접수 주문', self.kiwoom.order[code])

						# (2.1) '미체결수량' 확인하여 미체결 종목인지 확인
						if self.kiwoom.order[code]['미체결수량'] > 0:
							pass

					# (3)보유 종목인지 확인
					elif code in self.kiwoom.balance.keys():
						print('보유 종목', self.kiwoom.balance[code])
						# (6)매도 대상 확인
						if self.check_sell_signal(code):
							# (7)매도 대상이면 매도 주문 접수
							self.order_sell(code)

					else:
						# (4)접수 주문 및 보유 종목이 아니라면 매수대상인지 확인 후 주문접수
						self.check_buy_signal_and_order(code)

			except Exception as e:
				print(traceback.format_exc())

	# LINE 메시지를 보내는 부분
	# send_message(traceback.format_exc(), RSI_STRATEGY_MESSAGE_TOKEN)

	def buy_order(self, code, price):
		if (self.get_balance_count() + self.get_buy_order_count()) >= 10:
			return

		budget = self.deposit / (10 - (self.get_balance_count() + self.get_buy_order_count()))

		quantity = math.floor(budget / price)

		if quantity < 1:
			return

		amount = quantity * price
		self.deposit = math.floor(self.deposit - amount * 1.00015)

	def sell_order(self, code, price):
		# 보유 수량 확인(전량 매도 방식으로 보유한 수량을 모두 매도함)
		quantity =
		self.deposit = self.deposit + quantity * price
