from command.Command import Command


class RemoveInvestorCommand(Command):
	name = 'remove'

	class CLICommand(Command.CLICommand):
		def __init__(self):
			super().__init__(RemoveInvestorCommand.name)

		def options(self):
			options = [('-n', '--name', 'The name of strategy')]
			return options

	class ControllerCommand(Command.ControllerCommand):
		def __init__(self):
			super().__init__(RemoveInvestorCommand.name)

		def func(self, **kwargs):
			Command.ControllerCommand.backtestTrader.removeInvestor(**kwargs)


Command.registCommand(RemoveInvestorCommand)
