from trade.dealer import *
from trade.trader import *
from invest.investor import *
from invest.wallet.db_wallet import *
from invest.wallet.dict_wallet import *
from pykrx import stock


class backtestTrader(Trader):
	def __init__(self, dealer):
		super().__init__(dealer)

	def run(self, fromdate='20190101', todate='20211231'):
		for date in stock.get_previous_business_days(fromdate=fromdate, todate=todate):
			cur_date = date.strftime("%Y%m%d")
			universe = self.data_manager.get_universe(cur_date)

			stock_info = universe.to_dict('index')
			stock_prices = universe['종가']
			for investor in self.investors.values():
				investor.updateStockPrices(stock_prices)
				print(f'{cur_date} : {investor.getAccountValue()}')
				for code, info in stock_info.items():
					if investor.wantSell(code, info):
						(code, price, quantity) = investor.apply_sell_order(code, info['종가'])
						investor.confirm_sell_order(code, price, quantity)
						print(f'{date} : sell (code :{code}, PER: {info["PER"]}, price: {price}, quantity: {quantity})')

					if investor.wantBuy(code, info):
						(code, price, quantity) = investor.apply_buy_order(code, info['종가'])
						investor.confirm_buy_order(code, price, quantity)
						print(f'{date} : buy (code :{code}, PER: {info["PER"]}, price: {price}, quantity: {quantity})')


if __name__ == "__main__":
	name = 'RSI7'
	RSI_strategy = strategy(name, '', '')
	db_wallet = db_wallet(name, 1000000)
	dict_wallet = dict_wallet(name, 1000000)
	investor = Investor(name, dict_wallet, RSI_strategy)
	dealer = Dealer()
	trader = backtestTrader(dealer)
	trader.addInvestor(investor)
	trader.run('20190101', '20220407')
