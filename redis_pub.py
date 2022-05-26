import redis
import random

conn = redis.Redis()
cats = ['a', 'b', 'c', 'd', 'e']
hats = ['f', 'g', 'h', 'i', 'j']

for msg in range(10):
	cat = random.choice(cats)
	hat = random.choice(hats)
	print('Publish: %s wears %s' % (cat, hat))
	conn.publish(cat, hat)
