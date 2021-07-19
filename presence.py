import time
import traceback
import logging
from pypresence import Presence
from pypresence.exceptions import InvalidPipe

APP_ID = '864412248310284289'
RPC = Presence(APP_ID)

def connect():
    try:
        RPC.connect()
    except:
        s = ''.join(traceback.format_stack())
        logging.warning(s)

def close():
    try:
        RPC.close()
    except:
        s = ''.join(traceback.format_stack())
        logging.warning(s)

def menu():
    try:
        RPC.update(start=int(time.time()), details='Menu', large_image='concerto_icon')
    except:
        s = ''.join(traceback.format_stack())
        logging.warning(s)

def character_select(mode,lobby_id=None):
    try:
        if lobby_id:
            RPC.update(state='Character Select', start=int(time.time()), large_image='concerto_icon', details='Public Lobby #%s' % lobby_id, buttons=[{'label': 'Join Lobby', 'url': 'concerto://lobby:' + str(lobby_id)}])
        else:
            RPC.update(state='Character Select', start=int(time.time()), details=mode, large_image='concerto_icon')
    except:
        s = ''.join(traceback.format_stack())
        logging.warning(s)

def generic(mode):
    try:
        RPC.update(start=int(time.time()), details=mode, large_image='concerto_icon')
    except:
        logging.log(''.join(traceback.format_stack()))

def public_lobby(id):
    try:
        RPC.update(state='Idle', start=int(time.time()), details='Public Lobby #%s' % id, large_image='concerto_icon', buttons=[{'label': 'Join Lobby', 'url': 'concerto://lobby:' + str(id)}])
    except:
        s = ''.join(traceback.format_stack())
        logging.warning(s)

def private_lobby():
    try:
        RPC.update(state='Idle', start=int(time.time()), details='Private Lobby', large_image='concerto_icon')
    except:
        s = ''.join(traceback.format_stack())
        logging.warning(s)

def online_game(mode, opponent_name, char_name, char_id, moon_id):
    try:
        RPC.update(state='Playing vs ' + opponent_name, start=int(time.time()), details=mode, large_image='char_' + str(char_id), large_text=char_name, small_image='moon_' + str(moon_id))
    except:
        s = ''.join(traceback.format_stack())
        logging.warning(s)

def public_lobby_game(lobby_id, opponent_name, char_name, char_id, moon_id):
    try:
        RPC.update(state='Playing vs ' + opponent_name, start=int(time.time()), details='Public Lobby #%s' % lobby_id, large_image='char_' + str(char_id), large_text=char_name, small_image='moon_' + str(moon_id), buttons=[{'label': 'Join Lobby', 'url': 'concerto://lobby:' + str(lobby_id)}])
    except:
        s = ''.join(traceback.format_stack())
        logging.warning(s)

def broadcast_game(mode, char1_id, tooltip_1, char2_id, tooltip_2, lobby_id=None):
    try:
        if lobby_id:
            RPC.update(start=int(time.time()), state=mode, large_image='char_' + str(char1_id), large_text=tooltip_1, small_image='char_' + str(char2_id), small_text=tooltip_2, details="Public Lobby #%s" % lobby_id, buttons=[{'label': 'Join Lobby', 'url': 'concerto://lobby:' + str(lobby_id)}])
        else:
            RPC.update(start=int(time.time()), state=mode, large_image='char_' + str(char1_id), large_text=tooltip_1, small_image='char_' + str(char2_id), small_text=tooltip_2)
    except:
        s = ''.join(traceback.format_stack())
        logging.warning(s)

def offline_game(gamemode, char1_name, char1_id, char2_name, char2_id, lobby_id=None):
    try:
        if lobby_id:
            RPC.update(start=int(time.time()), state=gamemode, large_image='char_' + str(char1_id), large_text=char1_name, small_image='char_' + str(char2_id), small_text=char2_name, details="Public Lobby #%s" % lobby_id, buttons=[{'label': 'Join Lobby', 'url': 'concerto://lobby:' + str(lobby_id)}])
        else:
            RPC.update(start=int(time.time()), state=gamemode, large_image='char_' + str(char1_id), large_text=char1_name, small_image='char_' + str(char2_id), small_text=char2_name)
    except:
        s = ''.join(traceback.format_stack())
        logging.warning(s)

def single_game(mode,char_name, char_id, moon_id, lobby_id=None):
    try:
        if lobby_id:
            RPC.update(start=int(time.time()), state=mode, large_image='char_' + str(char_id), large_text=char_name, small_image='moon_' + str(moon_id), details="Public Lobby #%s" % lobby_id, buttons=[{'label': 'Join Lobby', 'url': 'concerto://lobby:' + str(lobby_id)}])
        else:
            RPC.update(start=int(time.time()), state=mode, large_image='char_' + str(char_id), large_text=char_name, small_image='moon_' + str(moon_id))
    except:
        s = ''.join(traceback.format_stack())
        logging.warning(s)