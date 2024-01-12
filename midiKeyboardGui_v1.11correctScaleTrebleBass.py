'''
File: midiKeyboardGui_v1.10correctScaleTrebleBass.py
Date: Jan8 2023
Python version: Python 3.11.4
OS: macOS ventura 13.5
Hardware: 15inch M2 Macbook Air
How To Run This File: plug in usb B cable to MIDI piano and also to computer, when prompt comes up click accept, then run this file in terminal 'python3 midiKeyboardGui_v1.10correctScaleTrebleBass.py'
...remember to Plug in the other end of the USB cable to computer
GPT: ChatGPT 3.5
Prompter: MatthewBDavis
Liscense: Copyright Matthew B. Davis © 2024
Description: goal is to get notes popping up on a staff
Status: treble clef notes on lines line up correctly with piano keys
#FIXME except notes in the spaces aren't centered

DONE draw Bass clef lines correctly positioned
'''

import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk
import mido
from mido import MidiFile, MidiTrack, Message

class MidiPianoRoll:
    def __init__(self, root):
        self.root = root
        self.root.title("MIDI Piano Roll")

        # Create a frame to hold the widgets
        frame = tk.Frame(root)
        frame.grid(row=0, column=0, sticky="nsew")

        # Create a canvas
        self.canvas_width = 600
        self.canvas_height = 980 # for pads of 40 at top and bottom of piano keyboard   #FIXME
        self.canvas = tk.Canvas(frame, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.grid(row=0, column=1, sticky="nsew")
        #these worked:
        #self.canvas = Canvas(root, width=2400, height=1200, bg="white")
        #self.canvas.pack()

        # Configure grid weights for resizing #idk what this is
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(0, weight=1)

        self.note_width = 15
        self.note_height = self.canvas_height / 90
        self.setup_midi()
        self.draw_staff()

    def setup_midi(self):
        self.midi_input = mido.open_input('USB Device') #LIve
        #self.midi_input = mido.open_input('MPK Mini Mk II')
        self.root.after(100, self.check_midi_input)

    def check_midi_input(self):
        for msg in self.midi_input.iter_pending():
            print(msg)
            if msg.type == 'note_on':
                self.draw_note_on(msg.note)
            elif msg.type == 'note_off':
                self.draw_note_off(msg.note)
        self.root.after(100, self.check_midi_input)

    def draw_staff(self):

        #FIXME draw a box for if u cant see all 4 corners this isnt gong to work correctlyj,
        #NVM the staff itself should show that
        #self.canvas.create_rectangle(x, y, x + self.note_width, y + self.note_height, fill="black")

        #draw a piano keyboard on the left edge of the screen: it needs to fit
        #between 0,40 and 0,940 so that there is a 40 pixel boundary around the outside

        # Load Treble Clef Image
        treble_clef_img = Image.open("TrebleAndBassStaff.jpg")
        treble_clef_img = ImageTk.PhotoImage(treble_clef_img)
        self.canvas.create_image(50, self.canvas_height // 2, anchor=tk.W, image=treble_clef_img)


        # Draw Treble Staff Lines
        LeftMargin = 80

        '''the E needs to align with the bottom line of the staff
        note=64
        note_on channel=0 note=64 velocity=79 time=0
        note = (64)
        Drawing Note On at (40, 261.33333333333337)
        note_off channel=0 note=64 velocity=0 time=0
        Drawing Note Off at (40, 261.33333333333337)

        #FIXME the middle C note=60 alignment is going to eventually be weird but right now we'll keep it uniform for easyness

        '''
        #okay lets draw the E line first -- should be at y position 261.33
        #E4_location = 261.33333333333337 + 5 #what is this based on!?! why not put it
        E4_location = (self.canvas_height // 2) + 5 #need the 5 to position right on the money
        ySpacing = self.note_height
        self.canvas.create_line(LeftMargin, E4_location, self.canvas_width, E4_location, fill="black")
        G4_location = E4_location - (3 * ySpacing)
        self.canvas.create_line(LeftMargin, G4_location, self.canvas_width, G4_location, fill="black")
        B4_location = G4_location  - (4 * ySpacing)
        self.canvas.create_line(LeftMargin, B4_location, self.canvas_width, B4_location, fill="black")
        D5_location = B4_location  - (3 * ySpacing)
        self.canvas.create_line(LeftMargin, D5_location, self.canvas_width, D5_location, fill="black")
        F5_location = D5_location  - (3 * ySpacing)
        self.canvas.create_line(LeftMargin, F5_location, self.canvas_width, F5_location, fill="black")
        '''
        for i in range(5):
            ySpacing = self.note_height #self.canvas_height // 2 - 30 + i * 10
            self.canvas.create_line(80, ySpacing, self.canvas_width, ySpacing, fill="black")
        '''

        C4_location = E4_location + (4 * ySpacing) #this is Middle C
        self.canvas.create_line(2 * LeftMargin, C4_location, self.canvas_width, C4_location, fill="black")
#FIXME ok random thought I think my stuff doesn't quite line up like it should as I get toward thh realy high really low of the staff
        A3_location = C4_location + (3 * ySpacing)
        self.canvas.create_line(LeftMargin, A3_location, self.canvas_width, A3_location, fill="black")
        F3_location = A3_location + (4 * ySpacing)
        self.canvas.create_line(LeftMargin, F3_location, self.canvas_width, F3_location, fill="black")
        D3_location = F3_location + (3 * ySpacing)
        self.canvas.create_line(LeftMargin, D3_location, self.canvas_width, D3_location, fill="black")
        B2_location = D3_location + (3 * ySpacing)
        self.canvas.create_line(LeftMargin, B2_location, self.canvas_width, B2_location, fill="black")
        G2_location = B2_location + (4 * ySpacing)
        self.canvas.create_line(LeftMargin, G2_location, self.canvas_width, G2_location, fill="black")

        # Draw Bass Staff Lines
        for i in range(5):
            y = (C4_location + (3 * ySpacing)) * i * ySpacing
#######self.canvas.create_line(LeftMargin, G4_location, self.canvas_width, G4_location, fill="black")

            #y = self.canvas_height // 2 + 40 + i * 10 #changed 20 t0 40 -- that looks better now
            self.canvas.create_line(40, y, self.canvas_width, y, fill="black")


    def draw_note_on(self, note):
        x = 40 #note * self.note_width
        print(f"note = ({note})")
        '''note_on channel=0 note=48 velocity=97 time=0
        note = (48)
        Drawing Note On at (40, 960) --- #why the fuck at 960 and not 0 or 40 !?!?!?!
        note_on channel=0 note=72 velocity=103 time=0
        note = (72)
        Drawing Note On at (40, 1440)

        #FIXME '940' so for our purposes, with his little 2 octave keyboard we are going to
        restrict our window to only deal with these values... This would not work for bigger piano
        '''

        ''' what's wrong with our y value why flipped?

        note = (48)
        Drawing Note On at (40, 960) --- #why the fuck at 960 and not 0 or 40 !?!?!?!
        Because 48 * 20 = 960.

        note = (72)
        Drawing Note On at (40, 1440)

        Ok what's the lowest number note I can expect to see?
        Probbably 0 is a safe bet. Highest, prob 89 ?

        so I want position 0 to corresood to y of 40 and then increaase aafter that:

        note_on channel=0 note=72 velocity=127 time=0
        Drawing Note On at (40, 500)
        note_off channel=0 note=72 velocity=0 time=0
        Drawing Note Off at (40, 500)
        '''

        '''
OK SO lol here: the lowest key is 21 but there are indeed 88 keys. Highest note is 108
    '''



        y = (88+21 - note) * self.note_height #- 940 #* .1 does not work like I want it to here, It makes the notes like pixel line size each impossible to resolve
        print(f"Drawing Note On at ({x}, {y})")
        self.canvas.create_rectangle(x, y, x + self.note_width, y + self.note_height, fill="black")

    def draw_note_off(self, note):
        x = 40 #note * self.note_width
        y = (88+21 - note) * self.note_height #y = note * self.note_height - 940
        print(f"Drawing Note Off at ({x}, {y})")
        self.canvas.create_rectangle(x, y, x + self.note_width, y + self.note_height, fill="white", outline="white")

if __name__ == "__main__":
    root = tk.Tk()
    app = MidiPianoRoll(root)
    root.mainloop()
