import argparse
import sys
import redis
import json
from trade.backtestTrader import *
from trade.dealer import *


# Command 하위 클래스는 name 클래스 변수를 정의
#
# Class - CLICommand : postFunc, options를 선택적으로 정의 가능
#           postfunc : 주로 반환 값이 있을때 정의
#           options : command의 옵션 파라미터를 정의
#
# Class - ControllerCommand : func을 선택적으로 정의 가능
#           func : cli 에서 명령을 받아 처리, 반환 값이 있을 경우 return을 통해 하면 된다.
#
# 서브 클래스들의 정의가 끝낫을 경우 Command.registCommand(Class 이름)으로 등록한다.

class Command:
	Commands = []

	@classmethod
	def registCommand(cls, command):
		cls.Commands.append(command)

	class CLICommand:
		topics = ['cli']
		conn = redis.Redis()
		sub = conn.pubsub()
		sub.subscribe(topics)

		parser = argparse.ArgumentParser()
		subparsers = parser.add_subparsers()

		def __init__(self, name):
			self.name = name

		@classmethod
		def parseCommand(cls, line):
			args = cls.parser.parse_args(line.strip().split(' '))
			dict = args.__dict__
			remove = [key for key, val in dict.items() if val is None]
			for key in remove:
				del dict[key]

			return args

		def registCommand(self, command, func, args):
			parser = Command.CLICommand.subparsers.add_parser(command)
			parser.set_defaults(func=func)

			if args is not None:
				for flag, name, help in args:
					parser.add_argument(flag, name, help=help)

		def receiveMessage(self):
			for msg in Command.CLICommand.sub.listen():
				if msg['type'] == 'message':
					msg = msg['data'].decode('utf-8')
					msg = json.loads(msg)
					return msg

		def func(self, args):
			dict = args.__dict__
			dict.pop('func', None)
			msg = {'cmd': self.name, 'args': dict}
			print(msg)
			json_val = json.dumps(msg, ensure_ascii=False).encode('utf-8')
			Command.CLICommand.conn.publish('controller', json_val)

			self.postFunc()

		def postFunc(self):
			pass

		def options(self):
			pass

	class ControllerCommand:
		topics = ['controller']
		conn = redis.Redis()
		sub = conn.pubsub()
		sub.subscribe(topics)

		backtestTrader = backtestTrader(Dealer())

		commands = {}

		def __init__(self, name):
			self.name = name
			self.register(name)

		def execute(self, **kwargs):
			message = self.func(**kwargs)
			if message is not None:
				self.send_message(message)

		def send_message(self, dict):
			json_val = json.dumps(dict, ensure_ascii=False).encode('utf-8')
			Command.ControllerCommand.conn.publish('cli', json_val)

		def register(self, name):
			Command.ControllerCommand.commands[name] = self

		def func(self, **kwargs):
			pass
