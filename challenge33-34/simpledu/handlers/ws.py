from flask import Blueprint
import redis
import gevent
import json
ws = Blueprint('ws', __name__, url_prefix='/ws')

# 创建redis连接
redis = redis.from_url('redis://127.0.0.1:6379')

class Chatroom(object):

	def __init__(self):
		self.clients = []  
		# 初始化pubsub系统
		self.pubsub = redis.pubsub()  
		# 订阅chat频道
		self.pubsub.subscribe('chat')

	def register(self, client):
		self.clients.append(client)

	def send(self, client, data):
		# 给每一个客户端client发送消息data
		try:
			# python3中接受到的消息是二进制的，使用decode函数转化为字符 串
			client.send(data.decode('utf-8'))
		except:
			# 发生错误可能是客户端已经关闭，移除该客户端
			self.clients.remove(client)

	def run(self):
		# 依次将接收到的消息再发给所有的客户端
		for message in self.pubsub.listen():
			if message['type'] == 'message':
				data = message.get('data')
				for client in self.clients:
					# 使用gevent异步发送
					gevent.spawn(self.send, client, data)

	def start(self):
		# 异步执行run函数
		gevent.spawn(self.run)

# 初始化聊天室
chat = Chatroom()
# 异步启动聊天室
chat.start()

@ws.route('/send')
def inbox(ws):
	''' 使用flask-sockets, ws链接对象会被自动注入到路由处理函数， 该函数用来处理前端发过来的消息
		while循环里面的receive()函数实际是在阻塞运行的，直到前端发送消息过来
		消息会被放入到chat频道，也就是我么的消息队列中，这样一直循环，直到websockets连接关闭
	'''
	while not ws.closed:
		gevent.sleep(0.1)
		message = ws.receive()
		if message:
			# 发送消息到chat频道
			redis.publish('chat', message)
			
@ws.route('/recv')
def outbox(ws):
	'''该函数用来注册客户端连接，并在Chatroom中将从其它客户端接收到的消息发送给这些客户端
	'''
	chat.register(ws)
	redis.publish('chat', json.dumps(dict
		(username='New user come in, people count: ',text=len(chat.clients))
		))
    
	while not ws.closed:
		gevent.sleep(0.1)