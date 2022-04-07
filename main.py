import numpy as np

class A:
	def f(self):
		print('A::f')

	def d(self):
		self.f()

def f(x, y) :
	a, b, c = x
	print(a)

if __name__ == '__main__':
	x = (1, 2)

	f(-x)