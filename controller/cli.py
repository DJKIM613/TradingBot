from command import *
from command.Command import Command
import sys

if __name__ == '__main__':
	for com in Command.Commands:
		cli_command = com.CLICommand()
		cli_command.registCommand(com.name, cli_command.func, cli_command.options())

	while True:
		print('>>> ', end='')
		line = sys.stdin.readline()
		try:
			args = Command.CLICommand.parseCommand(line)
			args.func(args)
		except:
			print('Error!')
