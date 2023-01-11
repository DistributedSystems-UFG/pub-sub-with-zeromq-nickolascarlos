import zmq, threading, sys
from constPS import * #-

# Obtém a porta de acordo com o nome
# de usuário especificado
try:
	my_port = registry[sys.argv[1]][1]
except IndexError:
	print('Especifique o usuário (alice ou bob) no primeiro parâmetro do script')
	sys.exit(-1)

context = zmq.Context()

# Cria o socket usado para enviar
# mensagens ao servidor
req_s = context.socket(zmq.REQ)
req_s.connect('tcp://127.0.0.1:5679')

# Cria o socket usado para receber
# mensagens de tópicos em que se
# está inscrito
sub_s = context.socket(zmq.SUB)
sub_s.connect('tcp://127.0.0.1:5678')

# Cria o socket usado para receber
# mensagens enviadas diretamente
# para o usuário
rep_s = context.socket(zmq.REP)
rep_s.bind('tcp://*:' + str(my_port))

# Função para a thread que escuta os tópicos
def subject_listener():
	while True:
		msg = sub_s.recv().decode('utf-8')
		print('Mensagem de tópico::: ' + msg)

# Função para a thread que escuta as mensagens diretas
def direct_listener():
	while True:
		msg = rep_s.recv().decode('utf-8')
		print('Mensagem direta::: ' + msg)
		rep_s.send('ok'.encode('utf-8'))

# Cria e inicia as threads direct e subject
direct_listener_thread = threading.Thread(target=direct_listener)
subject_listener_thread = threading.Thread(target=subject_listener)
direct_listener_thread.start()
subject_listener_thread.start()

while True:
	message = input('>> ')

	# Se message for uma única palavra,
	# inscreve o socket ao tópico de mesmo nome
	if len(message.split(' ')) == 1:
		sub_s.setsockopt_string(zmq.SUBSCRIBE, message)
	# Do contrário, assume-se ser uma mensagem mesmo
	# e a envia ao servidor para ela seja tratada
	else:
		req_s.send(message.encode('utf-8'))
		print(req_s.recv())

