from command.Command import Command


class ShowInvestorCommand(Command):
	name = 'show'

	class CLICommand(Command.CLICommand):
		def __init__(self):
			super().__init__(ShowInvestorCommand.name)

		def postFunc(self):
			msg = self.receiveMessage()
			print(msg)

		def options(self):
			options = [('-n', '--names', 'The name of invest')]
			return options

	class ControllerCommand(Command.ControllerCommand):
		def __init__(self):
			super().__init__(ShowInvestorCommand.name)

		def func(self, **kwargs):
			investor_info = Command.ControllerCommand.backtestTrader.showInvestorInfo(**kwargs)
			return investor_info


Command.registCommand(ShowInvestorCommand)
