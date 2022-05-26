# 1. 매일 8시 30분에 매매 종목을 정해야 한다:
# 2. 터미널로부터 오는 명령(매매 신청, 계좌 조회 등) 을 수행해야 한다.
# 3. 1, 2 항목은 이벤트로 처리하는것이 효과적일 것이다.
# 4. subject, options, callback
# 5. trade - cli
# 			- invest
# 			- kiwoom
# 위처럼 trade 는 subject, function, option을 관리할 수 있어야한다.
# 6. polling 보다는 interrupt 방식을 채택하자.

import argparse
import sys
import redis
import json


class Command:
	def __init__(self, command, args, func):
		global subparsers
		parser = subparsers.add_parser(command)
		parser.set_defaults(func=func)
		for option, help in args.items():
			parser.add_argument(option)


def foo(args):
	conn = redis.Redis()
	dict = args.__dict__
	dict.pop('func', None)
	json_val = json.dumps(dict)
	conn.publish('a', json_val)


global conn
conn = redis.Redis()

# create the top-level parser
parser = argparse.ArgumentParser()

global subparsers
subparsers = parser.add_subparsers()

Command('foo', {'-x': 'This is x'}, foo)

while True:
	print('>>> ', end='')
	line = sys.stdin.readline()
	try:
		args = parser.parse_args(line.strip().split(' '))
		args.func(args)
	except:
		print('Error!')
