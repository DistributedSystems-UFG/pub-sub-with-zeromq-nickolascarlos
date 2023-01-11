import zmq, time, threading
from constPS import * #-

# context = zmq.Context()
# s = context.socket(zmq.PUB)        # create a publisher socket
# p = "tcp://"+ HOST +":"+ PORT      # how and where to communicate
# s.bind(p)                          # bind socket to the address
# while True:
# 	time.sleep(5)                    # wait every 5 seconds
# 	msg = str.encode("TIME " + time.asctime())
# 	s.send(msg) # publish the current time

context = zmq.Context()

pub_s = context.socket(zmq.PUB)        # create a publisher socket
pub_s.bind('tcp://*:5678')                          # bind socket to the address

rep_s = context.socket(zmq.REP)
rep_s.bind('tcp://*:5679')

# def pub_thread(s):
# 	print('Iniciada thread #pub')

def rep_thread(_rep_s, _pub_s):
	print('Iniciada thread #rep')

	while True:
		raw_message = _rep_s.recv().decode('utf-8')
		command, dest, message = raw_message.split(' ', 2)
		if command == 'sub':
			_pub_s.send_string('%s %s' % (dest, message))
		elif command == 'usr':
			print('... Enviando mensagem para ' + dest + ': ' + message)

		_rep_s.send_string('ok')


# pub_t = threading.Thread(target=pub_thread, args=(pub_s))
rep_t = threading.Thread(target=rep_thread, args=(rep_s, pub_s))
# pub_t.start()
rep_t.start()
