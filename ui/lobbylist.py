from json.decoder import JSONDecodeError
import requests
from functools import partial

from config import *

from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock

from ui.modals import GameModal
from ui.buttons import DummyBtn


class LobbyList(Screen):
    lobby_type = ObjectProperty(None)  # public or private lobby to create
    lobby_code = ObjectProperty(None)  # lobby code to join
    lobby_view = ObjectProperty(None)  # lobby grid layout

    def __init__(self, CApp, **kwargs):
        super(LobbyList, self).__init__(**kwargs)
        self.app = CApp

    def create(self):
        p = {
            'name': self.app.player_name,
            'action': 'create',
            'type': self.lobby_type.text
        }
        a = requests.get(url=LOBBYURL, params=p).json()
        if a['status'] == 'OK':
            self.app.sm.current = 'Lobby'
            self.app.LobbyScreen.secret = int(a['secret'])
            self.app.LobbyScreen.create(a, first=True, 
                type=a['type'])
        else:
            popup = GameModal()
            popup.modal_txt.text = 'Unable to create lobby: %s' % a['msg']
            popup.close_btn.text = 'Dismiss'
            popup.close_btn.bind(on_release=partial(popup.dismiss))
            popup.open()

    def join(self, obj=None, code=None):
        if code is None:
            c = self.lobby_code.text.strip()
        else:
            c = code
        p = {
            'name': self.app.player_name,
            'action': 'join',
            'id': c
        }
        try:
            a = requests.get(url=LOBBYURL, params=p, timeout=5).json()
        except JSONDecodeError:
            popup = GameModal()
            popup.modal_txt.text = 'Bad response from the server. Try again.'
            popup.close_btn.text = 'Dismiss'
            popup.close_btn.bind(on_release=partial(popup.dismiss))
            popup.open()
        else:
            if a['status'] == 'OK':
                self.app.sm.current = 'Lobby'
                self.app.LobbyScreen.secret = int(a['secret'])
                self.app.LobbyScreen.create(
                    a, first=True, type=a['type'])
                self.lobby_code.text = ''
            else:
                popup = GameModal()
                popup.modal_txt.text = a['msg']
                popup.close_btn.text = 'Dismiss'
                popup.close_btn.bind(on_release=partial(popup.dismiss))
                popup.open()

    def refresh(self):
        if self.app.LobbyScreen.lobby_updater != None:
            Clock.schedule_once(lambda dt: self.switch_to_lobby(),0)
            return None
        try:
            a = requests.get(url=LOBBYURL, params={'action':'list'}).json()
            self.lobby_view.clear_widgets()
            if a['lobbies'] != []:
                for i in a['lobbies']:
                    b = DummyBtn()
                    b.halign = 'left'
                    b.text = "ID %s: %s players" % (i[0], i[1])
                    b.bind(on_release=partial(self.join, code=i[0]))
                    self.lobby_view.add_widget(b)
            else:
                b = DummyBtn()
                b.halign = 'left'
                b.text = "No public lobbies found. Why not create one?"
                self.lobby_view.add_widget(b)
            if self.app.sm.current != 'LobbyList':
                Clock.schedule_once(lambda dt: self.switch_to_list(),0)
        except requests.exceptions.ConnectionError as e:
            Clock.schedule_once(lambda dt: self.switch_to_online(),0)
            p = GameModal()
            p.modal_txt.text = 'Unable to establish a connection to lobby server.'
            p.close_btn.text = 'Close'
            p.close_btn.bind(on_release=p.dismiss)
            p.open()

    def switch_to_list(self):
        self.app.sm.current = 'LobbyList'
    
    def switch_to_online(self):
        self.app.sm.current = 'Online'

    def switch_to_lobby(self):
        self.app.sm.current = 'Lobby'