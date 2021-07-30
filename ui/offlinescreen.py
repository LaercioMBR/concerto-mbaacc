from kivy.uix.screenmanager import Screen
from ui.modals import GameModal
from functools import partial
import threading
import webbrowser
import logging
from ui.playerwiki import *

class OfflineScreen(Screen):
    active_pop = None #active popup on the screen

    def __init__(self,CApp,**kwargs):
        super(OfflineScreen, self).__init__(**kwargs)
        self.app = CApp

    def training(self, *args):
        self.offline_pop("Training")
        caster = threading.Thread(target=self.app.game.training,args=[self],daemon=True)
        caster.start()

    def replays(self, *args):
        self.offline_pop("Replay Theater")
        caster = threading.Thread(target=self.app.game.replays,args=[self],daemon=True)
        caster.start()

    def local(self, *args):
        self.offline_pop("Local VS")
        caster = threading.Thread(target=self.app.game.local,args=[self],daemon=True)
        caster.start()

    def tournament(self, *args):
        self.offline_pop("Tournament VS")
        caster = threading.Thread(target=self.app.game.tournament,args=[self],daemon=True)
        caster.start()

    def standalone(self, *args):
        self.offline_pop("Standalone")
        caster = threading.Thread(target=self.app.game.standalone,args=[self],daemon=True)
        caster.start()

    def offline_pop(self, mode):
        popup = GameModal()
        popup.modal_txt.text = 'Starting %s mode...' % mode
        popup.close_btn.text = "Stand by..."
        popup.close_btn.disabled = True
        popup = fill_wiki_button(self,popup)
        popup.open()
        self.app.offline_mode = mode
        # self.fill_wiki_button()     #TODO Fill popup with the buttons for the wiki here?
        self.active_pop = popup
    
    def error_message(self,e):
        if self.active_pop != None:
            self.active_pop.modal_txt.text = ""
            for i in e:
                self.active_pop.modal_txt.text += i + '\n'
            self.active_pop.close_btn.disabled = False
            self.active_pop.close_btn.bind(on_release=self.active_pop.dismiss)
            self.active_pop.close_btn.text = "Close"
        else:
            popup = GameModal()
            for i in e:
                popup.modal_txt.text += i + '\n'
            popup.close_btn.bind(on_release=popup.dismiss)
            popup.close_btn.text = "Close"
            popup.open()