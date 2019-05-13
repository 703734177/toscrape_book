import redis
import json

ITEM_KEY = 'books:items'

def process_item(item):
	pass

def main():
	r = redis.StrictRedis(host='192.168.30.128', port = 6379)
	for _ in range(r.llen(ITEM_KEY)):
		data = r.lpop(ITEM_KEY)
		item = json.loads(data.decode('utf8'))
		process_item(item)


if __name__ =='__main__':
	main()