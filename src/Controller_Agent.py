import subprocess, socket, threading, pickle, time


buffer_size = 3000
def write(_socket, data):
	f = _socket.makefile('wb', buffer_size)
	pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
	f.close()


def read(_socket):
	f = _socket.makefile('rb', buffer_size)
	data = pickle.load(f)
	f.close()
	return data


REST_API='http://127.0.0.1:8181/onos/v1/links?device='
def requestLinks(id):
	global REST_API
	REST_API+=id
	cmd = ['curl', REST_API, '--user', 'karaf:karaf']
	fd_popen = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
	data = fd_popen.read().strip()
	fd_popen.close()
	print data
	print '\n'


def agentSession(conn):
	tmp = read(conn)
	switch_role.append(tmp)
	print tmp
	requestLinks(tmp['ID'])
	while 1:
		monitoring_result.append(read(conn))
		print monitoring_result
		print '\n'


def acceptConnection():
	while 1:
		conn, addr = SOCK_AGENT.accept() #conn, addr = s.accept()
		session_th = threading.Thread(target=agentSession, args=(conn,))
		session_th.start()


def multiPathCreator():
	time.sleep(120)
	
	


switch_role = []
monitoring_result = []


CONTROLLER_AGENT_IP = '192.168.0.50'
TCP_PORT = 5555
SOCK_AGENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SOCK_AGENT.bind((CONTROLLER_AGENT_IP, TCP_PORT))
SOCK_AGENT.listen(10)

print '\n'
print 'Controller Agent Ready..'
print '\n'

accept_th = threading.Thread(target=acceptConnection, args=())
accept_th.start()



#REST_API='http://127.0.0.1:8181/onos/v1/links?device='
#cmd = ['curl','http://127.0.0.1:8181/onos/v1/links', '--user', 'karaf:karaf']
#fd_popen = subprocess.Popen(cmd, stdout=subprocess.PIPE).stdout
#data = fd_popen.read().strip()
#fd_popen.close()

#print data
