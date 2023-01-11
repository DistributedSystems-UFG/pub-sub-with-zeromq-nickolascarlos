import zmq, threading
from constPS import * #-

# context = zmq.Context()
# s = context.socket(zmq.SUB)          # create a subscriber socket
# p = "tcp://"+ HOST +":"+ PORT        # how and where to communicate
# s.connect(p)                         # connect to the server
# s.setsockopt_string(zmq.SUBSCRIBE, "TIME")  # subscribe to TIME messages

# for i in range(5):  # Five iterations
# 	time = s.recv()   # receive a message
# 	print (bytes.decode(time))

me = input('alice or bob? ')
my_port = registry[me][1]

context = zmq.Context()
req_s = context.socket(zmq.REQ)
req_s.connect('tcp://127.0.0.1:5679')

sub_s = context.socket(zmq.SUB)
sub_s.connect('tcp://127.0.0.1:5678')

rep_s = context.socket(zmq.REP)
rep_s.bind('tcp://*:' + str(my_port))

def direct_listener_thread(_rep_s):
	print('DL thread iniciada')

	while True:
		m = _rep_s.recv().decode('utf-8')
		print('Recebido::: ' + m)
		_rep_s.send('ok'.encode('utf-8'))

def subject_listener_thread(_sub_s):
	print('SL thread iniciada')

	while True:
		print('TÓPICO::: ' + _sub_s.recv().decode('utf-8'))

dlt = threading.Thread(target=direct_listener_thread, args=(rep_s,))
slt = threading.Thread(target=subject_listener_thread, args=(sub_s,))
dlt.start()
slt.start()

while True:
	message = input('>> ')

	if len(message.split(' ')) == 1:
		sub_s.setsockopt_string(zmq.SUBSCRIBE, message)
	else:
		req_s.send(message.encode('utf-8'))
		print(req_s.recv())

