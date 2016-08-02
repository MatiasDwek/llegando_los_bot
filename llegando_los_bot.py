#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
import telepot
from telepot.delegate import per_chat_id, create_open
import threading
import time
import datetime
from random import randint
from ChatData import ChatData, ScheduleTime

days = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
	
class MessageCounter(telepot.helper.ChatHandler):
	def __init__(self, seed_tuple, timeout):
		super(MessageCounter, self).__init__(seed_tuple, timeout)

	def on_chat_message(self, msg):
		lock.acquire()
		try:
			if telepot.glance(msg)[2] not in chats_config:
				new_chat = ChatData()
				chats_config[telepot.glance(msg)[2]] = new_chat
		finally:
			lock.release()
			
		if msg['text'].split(' ', 1)[0] == '/set_schedule_time@llegando_los_bot' or msg['text'].split(' ', 1)[0] == '/set_schedule_time':
			lock.acquire()
			try:
				chats_config[telepot.glance(msg)[2]].schedule_active = True;
				try:
					if ScheduleTime.validate_time(int(msg['text'].split(' ', 1)[1].split(':', 1)[0]), int(msg['text'].split(' ', 1)[1].split(':', 1)[1])) == True:
						chats_config[telepot.glance(msg)[2]].schedule_time.hour = int(msg['text'].split(' ', 1)[1].split(':', 1)[0])
						chats_config[telepot.glance(msg)[2]].schedule_time.minute = int(msg['text'].split(' ', 1)[1].split(':', 1)[1])
						self.sender.sendMessage("Automatic schedule activated for " + \
						"{0:0=2d}".format(int(msg['text'].split(' ', 1)[1].split(':', 1)[0])) + \
						":" + \
						"{0:0=2d}".format(int(msg['text'].split(' ', 1)[1].split(':', 1)[1])) + \
						"hs")
					else:
						self.sender.sendMessage("Wrong time format. It should be HOUR:MINUTE, with 0 <= HOUR < 24 and 0 <= MINUTE < 60")
				except IndexError:
					self.sender.sendMessage("/set_schedule_time should be called with one argument, which is the time, e.g.: /set_schedule_time 14:30")
			finally:
				lock.release()

		if msg['text'].split(' ', 1)[0] == '/set_schedule@llegando_los_bot' or msg['text'].split(' ', 1)[0] == '/set_schedule':
			lock.acquire()
			try:
				try:
					if msg['text'].split(' ', 1)[1].lower() == 'on':
						chats_config[telepot.glance(msg)[2]].schedule_active = True;
						self.sender.sendMessage("Automatic schedule activated")
					elif msg['text'].split(' ', 1)[1].lower() == 'off':
						chats_config[telepot.glance(msg)[2]].schedule_active = False;
						self.sender.sendMessage("Automatic schedule deactivated")
					else:
						self.sender.sendMessage("/set_schedule's argument is either 'on' or 'off', e.g.: /set_schedule on")
				except IndexError:
					self.sender.sendMessage("/set_schedule should be called with one argument, which is either 'on' or 'off', e.g.: /set_schedule on")
			finally:
				lock.release()
				
		if msg['text'].split(' ', 1)[0] == '/set_schedule_period@llegando_los_bot' or msg['text'].split(' ', 1)[0] == '/set_schedule_period':
			lock.acquire()
			try:
				try:
					if ChatData.validate_modulo(int(msg['text'].split(' ', 1)[1])) == True:
						chats_config[telepot.glance(msg)[2]].schedule_modulo = int(msg['text'].split(' ', 1)[1]);
						self.sender.sendMessage("Schedule period set to modulo " + msg['text'].split(' ', 1)[1] + ".")
					else:
						self.sender.sendMessage("/set_schedule_period's argument should be an integer between 1 and 31, e.g.: /set_schedule_frequency 2")
				except IndexError:
					self.sender.sendMessage("/set_schedule_period should be called with one argument, which is an integer between 1 and 31, e.g.: /set_schedule_period 2")
			finally:
				lock.release()
	
		if msg['text'] == '/oh_si@llegando_los_bot' or msg['text'] == '/oh_si':
			f = open(sys.argv[2], encoding = 'utf-8', mode = 'r')
			try:
				for i in range(0, randint(0, file_len(sys.argv[2]) - 1)):
					f.readline()
				line_to_send = f.readline()
				if line_to_send.strip():
					self.sender.sendMessage(line_to_send)
			finally:
					f.close()

chats_config = dict()
lock = threading.Lock()

TOKEN = sys.argv[1]  # get token from command-line

bot = telepot.DelegatorBot(TOKEN, [ \
    (per_chat_id(), create_open(MessageCounter, timeout=3)), \
])
bot.message_loop()

while(1):
	time.sleep(1)
	lock.acquire()
	try:
		for chats, config in chats_config.items():
			if config.schedule_active:
				if not(datetime.datetime.now().day % config.schedule_modulo):
					if config.schedule_time.hour == datetime.datetime.now().hour and config.schedule_time.minute == datetime.datetime.now().minute and datetime.datetime.now().second == 0:
						f = open(sys.argv[2], encoding = 'utf-8', mode = 'r')
						try:
							for i in range(0, randint(0, file_len(sys.argv[2]) - 1)):
								f.readline()
							line_to_send = f.readline()
							if line_to_send.strip():
								bot.sendMessage(chats, "Arriba el " + days[datetime.datetime.now().weekday()] + ":")
								bot.sendMessage(chats, line_to_send)
						finally:
								f.close()
	finally:
		lock.release();