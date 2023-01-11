import zmq, time, threading
from constPS import * #-

context = zmq.Context()

# Cria o socket publisher
pub_s = context.socket(zmq.PUB)
pub_s.bind(f'tcp://*:{PORT_PUB}')

# Cria o socket usado para receber
# as mensagens dos usuários
rep_s = context.socket(zmq.REP)
rep_s.bind(f'tcp://*:{PORT_REP}')

while True:
		raw_message = rep_s.recv().decode('utf-8')
		command, dest, message = raw_message.split(' ', 2)

		# Se o primeiro termo de raw_message for 'sub'
		# envia a mensagem para o tópico de nome {dest}
		if command == 'sub':
			print(f'Publicando mensagem no tópico {dest}: {message}')
			pub_s.send_string('%s %s' % (dest, message))
		
		# Se o primeiro termo de raw_message for 'usr'
		# envia a mensagem para o usuário de nome {dest}
		elif command == 'usr':
			print(f'Enviando mensagem para o usuário {dest}: {message}')
			user_ip, user_port = registry[dest]
			user_addr = f"tcp://{user_ip}:{user_port}"
			direct_s = context.socket(zmq.REQ)
			direct_s.connect(user_addr)
			direct_s.send_string(message)
			rep_s.send_string(direct_s.recv().decode('utf-8'))
			direct_s.close()
		
