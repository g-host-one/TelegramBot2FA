#!/usr/bin/env python3

import os
import platform
from telegrambot2fa import TelegramBot2FA
import subprocess
import sys
from threading import Thread 

apiKey=""
chatId=""

def telegram_callback():
    auth_bot.notifyUser("You are successfully loged in!")
    auth_bot.finish()
    sys.stdout.write("\n")
    proc = subprocess.Popen('cmd.exe')
    os._exit(proc.wait())
    
auth_bot = TelegramBot2FA(apiKey, chatId, telegram_callback)

curr_login = os.getlogin()
hostname = platform.uname()[1]

print("\n --------------------- ")
print(" | 2 F A - S h e l l | ")
print(" |     L o g i n     | ")
print(" --------------------- ")
print(" Login with \'{}\' [at] {} \n".format(curr_login, hostname))

auth_bot.askUser("Confirm")

while auth_bot.isWorking():
    try:
        val = input("Enter your code: ") 
        if auth_bot.verifyCode(val):
            telegram_callback()
            break
    except:
        pass
    

while True:
    continue