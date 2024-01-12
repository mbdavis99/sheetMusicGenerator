import tkinter as tk
from tkinter import Canvas
import mido
from mido import MidiFile, MidiTrack, Message






print(mido.get_input_names())

# ['USB Device']
# ['MPK Mini Mk II'] #Ryanson's
'''
self.midi_input = mido.open_input('MPK Mini Mk II')  # Replace 'YourKeyboardName' with the actual name of your MIDI input

def check_midi_input(self):
    for msg in self.midi_input.iter_pending():
        print(msg)
        if msg.type == 'note_on':
            self.draw_note_on(msg.note)
        elif msg.type == 'note_off':
            self.draw_note_off(msg.note)
'''


# print(mido.get_input_names())  still yields: ['MPK Mini Mk II']
