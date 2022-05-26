# 1. 매일 8시 30분에 매매 종목을 정해야 한다:
# 2. 터미널로부터 오는 명령(매매 신청, 계좌 조회 등) 을 수행해야 한다.
# 3. 1, 2 항목은 이벤트로 처리하는것이 효과적일 것이다.
# 4. subject, options, callback
# 5. trade - cli
# 			- invest
# 			- kiwoom
# 위처럼 trade 는 subject, function, option을 관리할 수 있어야한다.
# 6. polling 보다는 interrupt 방식을 채택하자.

# cli - controller 사의 redis 객체로 통신
# Command 추가시 Command 객체를 상속 후 Command 이름을 생성자 파라미터로 입력, func 함수를 overriding 하면 된다.
# 이 때, 반환 값이 있을 경우 단순 return 문을 활용하면 된다.

from command import *
from command.Command import Command
import json

if __name__ == '__main__':
	for com in Command.Commands:
		controller_command = com.ControllerCommand()
		controller_command.register(controller_command.name)

	for msg in Command.ControllerCommand.sub.listen():
		if msg['type'] == 'message':
			msg = msg['data'].decode('utf-8')
			dict = json.loads(msg)
			print(dict)
			command = Command.ControllerCommand.commands[dict['cmd']]
			command.execute(**dict['args'])
