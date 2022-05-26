from command.Command import Command
from trade.backtestTrader import *

from invest.wallet.db_wallet import *


class AddInvestorCommand(Command):
	name = 'add'

	class CLICommand(Command.CLICommand):
		def __init__(self):
			super().__init__(AddInvestorCommand.name)

		def options(self):
			options = [('-n', '--name', 'The name of strategy'),
			           ('-d', '--deposit', 'Set deposit of strategy'),
			           ('-b', '--buy_condition', 'Set buy condition of strategy'),
			           ('-s', '--sell_condition', 'Set sell condition of strategy')]

			return options

	class ControllerCommand(Command.ControllerCommand):
		def __init__(self):
			super().__init__(AddInvestorCommand.name)

		def func(self, name, deposit, buy_condition=None, sell_condition=None):
			wallet_instance = dict_wallet(name, int(deposit))
			strategy_instance = strategy(name, buy_condition, sell_condition)
			investor_val = Investor(name, wallet_instance, strategy_instance)
			Command.ControllerCommand.backtestTrader.addInvestor(investor_val)


Command.registCommand(AddInvestorCommand)
