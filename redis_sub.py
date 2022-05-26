import redis

conn = redis.Redis()

topics = ['a', 'b']
sub = conn.pubsub()
sub.subscribe(topics)
for msg in sub.listen():
	if msg['type'] == 'message':
		cat = str(msg['channel'])
		hat = str(msg['data'])
		print(cat, hat)
