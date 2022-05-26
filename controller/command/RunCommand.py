from command.Command import Command


class RunTraderCommand:
	name = 'run'

	class CLICommand(Command.CLICommand):
		def __init__(self):
			super().__init__(RunTraderCommand.name)

		def options(self):
			options = [('-s', '--start', 'The date of the start'),
			           ('-e', '--end', 'The date of the end')]

			return options

	class ControllerCommand(Command.ControllerCommand):
		def __init__(self):
			super().__init__(RunTraderCommand.name)

		def func(self, **kwargs):
			Command.ControllerCommand.backtestTrader.run(**kwargs)


Command.registCommand(RunTraderCommand)
