from requests import session 
import json
import random
import os
from threading import Thread 

class TelegramBot2FA:
    def __init__(self, apiKey, chatId, callback):
        self.__apiKey = apiKey
        self.__chatId = chatId
        self.__callback = callback
        self.__message_id = -1
        self.__code = -1
        self.__read_timeout = 20
        self.__session = session()
        self.__isWorking = True
        self.__message_thread = Thread(target=self.__retrive_message, args=(self.__callback,))
        self.__url_update = "https://api.telegram.org/bot{}/getUpdates?timeout={}&allowed_updates=[\"callback_query\"]".format(self.__apiKey, self.__read_timeout)

    def askUser(self, message):
        self.__code = self.__generate_code()
        message += "\nYour one time code: " + self.__code
        reply_markup = json.dumps({"inline_keyboard" : [[{ "text": "Allow","callback_data": self.__code}, { "text": "Decline", "callback_data": "decline" }]]})
        url = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&reply_markup={}".format(self.__apiKey, self.__chatId, message, reply_markup)
        response = self.__session.get(url = url).json()
        if response['ok']:
            self.__message_id = response['result']['message_id']
            self.__message_thread.start()

    def notifyUser(self, message):
        url = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}".format(self.__apiKey, self.__chatId, message)
        self.__session.get(url = url)

    def verifyCode(self, code):
        return code == self.__code

    def finish(self):
        self.__isWorking = False

    def isWorking(self):
        return self.__isWorking
    
    def __generate_code(self):
        code = ""
        while len(code) < 6:
            code += str(random.randint(0,9))
        return code

    def __retrive_message(self, callback):
        while self.__isWorking:
            response = self.__session.get(url=self.__url_update, timeout=(3.5, self.__read_timeout + 10)).json()
            if response['ok'] and self.__isWorking :
                for msg in response['result']:
                    msg = msg['callback_query']
                    if msg['message']['message_id'] != self.__message_id:
                        pass
                    else:
                        if msg['data'] == self.__code:
                            self.__isWorking = False
                            callback()
                        else:
                            os._exit(1)