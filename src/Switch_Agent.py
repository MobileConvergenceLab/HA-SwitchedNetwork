import socket, os, threading, pickle


def link_load():
	os.system('bwm-ng -o csv -c 1 -T rate > bandwidth.log')
	f_load=open('bandwidth.log')
	link_load=[]
	line = f_load.readline()
	while line:
		link_load.append([line.split(';')[1], (line.split(';')[2], line.split(';')[3])])
		line = f_load.readline()


	return link_load


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



print '\n...starting Switch Agent...\n'
input_role=raw_input('switch_role: ')
print '\n'


switch_role={}
switch_role['switch_role']=input_role
switch_role['ID']='of:0000080027fd1b60'
print switch_role
print '\n'


CONTROLLER_AGENT_IP = '192.168.0.50'    # The remote host
PORT = 5555              # The same port as used by the server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((CONTROLLER_AGENT_IP, PORT))


write(sock, switch_role) # Report Switch Role
monitoring_result = link_load() #Traffic Monitoring
print monitoring_result
print '\n'
write(sock, monitoring_result) #Report monitoring result

while 1:
	pass

