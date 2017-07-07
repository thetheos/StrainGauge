#-*- coding: utf-8 -*-

import serial
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
 
class ChatApp(App):
 
    def build(self):
        #reconnaissance de la carte Arduino:
        self.Arduino = serial.Serial('COM13', 9600)

        self.fichier=open("data.txt","a")
 
        #On cree une disposition pour l'affichage:
        Layout=BoxLayout(orientation='vertical',spacing=40,padding=(200,20))
        #On cree un label:
        self.Label1=Label(text='2 + 3 = ?', font_size=20)
        Layout.add_widget(self.Label1)
        #On cree deux boutons reponses:
        self.Bouton5=Button(text='5')
        self.Bouton5.bind(on_press=self.send)
        #On ajoute le bouton dans l'affichage:
        Layout.add_widget(self.Bouton5)
        self.Bouton6=Button(text='6')
        self.Bouton6.bind(on_press=self.send)
        #On ajoute le bouton dans l'affichage:
        Layout.add_widget(self.Bouton6)
 
        #On renvoie l'affichage:
        return Layout
 
    def send(self,instance):
        self.Arduino.write('1')
        self.fichier.write("\nbonjour ca marche")
        
 
if __name__ == '__main__':
    ChatApp().run()