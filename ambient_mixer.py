"""ambient.py - plays an ambient mix with pygame. Mash CTRL+C to quit.
 
Usage:
  ambient.py <file>
 
Options:
  <file>             XML file of the ambient mix to play (called preset). Make sure you have the correct "sounds/" folder in your current working directory.
  -h --help          Show this help message.

"""
__author_original__      = "Philooz"
__author__      = "Alaster"
__copyright__   = "2017 GPL"

# ----------------------------------------------------------
# Audio Playback imports
import random, sys
import os
import pygame, untangle
from time import sleep
import time
millis = lambda: int(round(time.time()*1000))

# GUI importsra
from tkinter import *
import tkinter.ttk as ttk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
from tkinter import messagebox
import tkinter.font as font

# ----------------------------------------------------------

def initPyGameMixer():
    pygame.mixer.init()
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.init()
    global clock
    clock = pygame.time.Clock()

CLOCK_TICKER = 10

unit_duration_map = {
    '1m': 600*CLOCK_TICKER,
    '10m': 6000*CLOCK_TICKER,
    '1h': 36000*CLOCK_TICKER
}

#import time
#millis = lambda: int(round(time.time() * 1000))





# Declare global variables
global xml_file
output_file_name = ''

play_general = True
play_general_recently_reactivated = False
play_track = [True]*8
play_track_recently_reactivated = [False]*8
script_path = os.path.dirname(os.path.realpath(__file__))

def newFile():
    #print("New File!")
    MsgBox = messagebox.askquestion ('Create new file','Are you sure you want to close the current preset?\nAll unsaved data will be lost!',icon = 'warning')
    if MsgBox == 'yes':
        openFile(r'presets\silence.xml')
        return True
    else:
        return False
    
def saveFile():
    preset_path = script_path + '\presets'
    file_name = asksaveasfilename(initialdir = preset_path, defaultextension=".xml", title='Save as', filetypes=[('Preset file', '*.xml')])
    if file_name is None: # asksaveasfile return `None` if dialog closed with "cancel".
        return
    textToSave = getPresetFileData()
    writeFile(file_name, textToSave)
    print('Preset saved as: ', file_name)
    
def writeFile(file_name, data):
    file = open(file_name,'w')
    file.write(data)
    file.close()
    
def getPresetFileData():
    string_header = '<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<audio_template>\n'
    string_tracks = ''
    current_string = ''
    global channels
    for track_no, channel in enumerate(channels):
        current_string =    ' <channel' + str(track_no+1) + '>\n'\
                            '  <id_audio>' + channel.sound_id + '</id_audio>\n'\
                            '  <name_audio>' + channel.name + '</name_audio>\n'\
                            '  <url_audio>sounds_named/' + channel.sound_id + '.ogg</url_audio>\n'\
                            '  <mute>' + str(channel.muteStatus).lower() + '</mute>\n'\
                            '  <volume>' + str(channel.volume) + '</volume>\n'\
                            '  <balance>' + str(channel.balance) + '</balance>\n'\
                            '  <random>' + str(channel.random).lower() + '</random>\n'\
                            '  <random_counter>' + str(channel.random_counter) + '</random_counter>\n'\
                            '  <random_unit>' + str(channel.random_unit) + '</random_unit>\n'\
                            '  <crossfade>' + str(channel.crossfade).lower() + '</crossfade>\n'\
                            ' </channel' + str(track_no+1) + '>\n'
        string_tracks = string_tracks + current_string
    current_string = ''
    if len(channels) < 8:
        for track_no in range(len(channels), 8):
            current_string =    ' <channel' + str(track_no+1) + '>\n'\
                                '  <id_audio>0</id_audio>\n'\
                                '  <name_audio>-</name_audio>\n'\
                                '  <url_audio></url_audio>\n'\
                                '  <mute>true</mute>\n'\
                                '  <volume>0</volume>\n'\
                                '  <balance>0</balance>\n'\
                                '  <random>true</random>\n'\
                                '  <random_counter>5</random_counter>\n'\
                                '  <random_unit>10m</random_unit>\n'\
                                '  <crossfade>false</crossfade>\n'\
                                ' </channel' + str(track_no+1) + '>\n'
            string_tracks = string_tracks + current_string
    string_footer = ' <id_template>6420</id_template>\n <id_session_user>false</id_session_user>\n <id_session_player>2e584355c198bfcd90dae4bd7d8516be</id_session_player>\n</audio_template>\n'
    return (string_header + string_tracks + string_footer)

    
def openFile(preset_name = ''):
    global channels
    #print("Select file to load...")
    preset_path = script_path + '\presets'
    if preset_name == '':
        preset_name = askopenfilename(initialdir = preset_path, defaultextension=".xml", title='Open file', filetypes=[('Preset file', '*.xml')])
    if not preset_name:
        print("No preset file loaded!")
        return False
    else:
        print("Selected preset file: ", preset_name)
        global xml_file
        xml_file = preset_name.split('/')[-1]
        print(preset_name)
        for channel in channels:
            channel.stop()        
        for track_no in range(0,8):
            resetTrack(track_no)        
        #pygame.quit()
        #sleep(0.5)
        channels=[]
        root.title('RPG Atmosphere Mixer:  ' + xml_file.split('.xml')[0])
        initPyGameMixer()
        bootstrap_chanlist(load_file(preset_name))
        #root.after(CLOCK_TICKER, task)
        return True

def resetTrack(track_no):
    file_name[track_no].delete('1.0', END)
    file_name[track_no].configure(background="#E1E1E1")
    scroll_bar[track_no].set(100)
    combobox_random_amount[track_no].set("1x")
    combobox_random_timeframe[track_no].set("10m")
    deactivatePlayOnceButton(track_no)
    deactivatePlayPauseButton(track_no)
    button_random[track_no].config(relief=RAISED)    
    button_crossfade[track_no].config(relief=RAISED)
    button_mute[track_no].config(relief=RAISED)

#def Save():
#    print(output_file_name)	
#    print("Save file as...")
#    if output_file_name == '':
#        print(xml_file)
#    else:
#        print(output_file_name)	

def SaveAs():
    print("Save file as...")
    output_file_name = asksaveasfilename()
    print(output_file_name)	

def About():
    print("This is a simple example of a menu")

def on_closing():
    closeWindowProperly()

# This function is called when window is closed
def closeWindowProperly():
    global pygame
    global root
    #pygame.display.quit()
    pygame.mixer.quit()
    pygame.quit()
    sleep(0.1)
    root.destroy()
    sys.exit()

#print('len(argv): ', len(sys.argv))
if len(sys.argv) <= 1:
    #xml_file = ".presets\\silence.xml"
    xml_file = script_path + r'\presets\silence.xml'
    #xml_file = r'presets\01-sailing-into-fog.xml'
else:    
    xml_file = sys.argv[1]
print('Loading preset file: ', xml_file)

root = Tk()
menu = Menu(root)
root.config(menu=menu)
root.protocol("WM_DELETE_WINDOW", on_closing)       # launch function on_closing when tkinter window is closed
root.iconbitmap(script_path + '\mixer.ico')
root.geometry("+400+5")                             # position window on +x+y coordinates on screen
#window_height = root.winfo_height()
#window_width = root.winfo_width()
#screen_height = root.winfo_screenheight() # height of the screen
#screen_width = root.winfo_screenwidth() # width of the screen
#x_pos_window = (screen_width/2) - (window_width/2)
#y_pos_window = (screen_height/2) - (window_height/2)
#print('{}, {} | {}, {} | {}, {}'.format(window_height, window_width, screen_height, screen_width, x_pos_window, y_pos_window))
#root.geometry('%dx%d+%d+%d' % (window_height, window_width, x_pos_window, y_pos_window))

myFont = font.Font(size=20)
root.title('RPG Atmosphere Mixer:  ' + xml_file.split('\\')[-1].split('.xml')[0])
filemenu = Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New file", command=newFile)
filemenu.add_command(label="Open...", command=openFile)
filemenu.add_separator()
#filemenu.add_command(label="Save", command=Save)
filemenu.add_command(label="Save as...", command=saveFile)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=closeWindowProperly)

helpmenu = Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About...", command=About)

# This function is called whenever the button is pressed
def random_amount_click(event, track_no):
    global channels
    print('mouse triggered on track #', track_no)
    if event: # <-- this works only with bind because `command=` doesn't send event
        amount = event.widget.get()
        print("amount event:", amount)
        channels[track_no].setRandomAmount(int(amount.replace('x','')))
	
def random_amount_keyboard(event, track_no):
    global channels
    print('keyboard triggered on track #', track_no)
    if event: # <-- this works only with bind because `command=` doesn't send event
        amount = event.widget.get()
        print("amount event:", amount)
        channels[track_no].setRandomAmount(int(amount.replace('x','')))	

def random_timeframe_click(event, track_no):
    print('mouse triggered on track #', track_no)
    if event: # <-- this works only with bind because `command=` doesn't send event
        timeframe = event.widget.get()
        print("timeframe event:", timeframe)
        if (timeframe=='1m' or timeframe=='10m' or timeframe=='1h'):
            channels[track_no].setRandomTimeframe(timeframe)
	
def random_timeframe_keyboard(event, track_no):
    print('keyboard triggered on track #', track_no)
    if event: # <-- this works only with bind because `command=` doesn't send event
        timeframe = event.widget.get()
        print("timeframe event:", timeframe)
        if (timeframe=='1m' or timeframe=='10m' or timeframe=='1h'):
            channels[track_no].setRandomTimeframe(timeframe)

def button_load_pressed(track_no):
    global channels
    global xml_file
    print('button load pressed on track: ', track_no)
    sound_path = script_path + '\sounds_named'
    sound_name = askopenfilename(initialdir = sound_path, defaultextension=".ogg", title='Open sound file', filetypes=[('OGG file', '*.ogg'), ('WAV file', '*.wav')])
    if not sound_name:
        print("No sound file loaded!")
        return False
    else:
        print("Selected sound file: ", sound_name)
        print(sound_name)
        xml_file = sound_name.split('/')[-1]
        track_info_dict = {
          'sound_id': xml_file.split('.')[0],
          'random': False, 
          'mute': False, 
          'name': xml_file.split('.')[0], 
          'volume': '80', 
          'balance': 0, 
          'random_counter': 1, 
          'random_unit': '1m'
        }
        #print(track_info_dict)
        
        resetTrack(track_no)
        
        if len(channels) <= track_no:
            if track_info_dict["sound_id"] not in ('','0','-'):
                channels.append(Channel(track_no, **track_info_dict))        
        else:
            channels[track_no].stop()
            channels[track_no] = Channel(track_no, **track_info_dict)
        print('Loaded ', channels[track_no])
        channels[track_no].play()
        #bootstrap_chanlist(load_file(preset_name))
        return True

def button_play_pause_pressed(track_no):
    print('button play/pause pressed on track: ', track_no)
    global play_track
    global play_track_recently_reactivated 
    global channels
    play_track[track_no] = not play_track[track_no]
        
    if play_track[track_no]:
        play_track_recently_reactivated[track_no] = True
    else:
        channels[track_no].pause()
        #channels[track_no].stop()
    if play_track_recently_reactivated[track_no] and play_track[track_no]:
        #channels[track_no].play(-1)
        channels[track_no].unpause()
        sleep(0.01)
        play_track_recently_reactivated[track_no] = False

def button_xml_play_pause_pressed():
    print('button xml play/pause pressed!')
    global play_general
    global play_general_recently_reactivated 
    global play_track
    global play_track_recently_reactivated    
    global channels
    play_general = not play_general
    if play_general:
        play_general_recently_reactivated = True
    else:
        for channel in channels:
            channel.pause()
            #channel.stop()
            for i, channel in enumerate(channels):
                play_track[i] = False
                play_track_recently_reactivated[i] = False
    
    if play_general_recently_reactivated and play_general:
        for channel in channels:
            channel.unpause()
            for i, channel in enumerate(channels):
                play_track[i] = True
                play_track_recently_reactivated[i] = True
            #sleep(0.1)
        play_general_recently_reactivated = False

def button_play_once_pressed(track_no):
    print('button \"play once\" pressed on track: ', track_no)
    channels[track_no].playOnce()
    #.configure(bg="red")

def button_mute_pressed(track_no):
    print('button mute pressed on track: ', track_no)
    print('scroll bar value: ', scroll_bar[track_no].get())
    channels[track_no].muteChannel()
	
def button_crossfade_pressed(track_no):
    print('button crossfade pressed on track: ', track_no)
    channels[track_no].setCrossfade()

def button_random_pressed(track_no):
    print('button random pressed on track: ', track_no)
    channels[track_no].setRandom()

def activatePlayOnceButton(track_no):
    button_playonce[track_no].config(relief=SUNKEN)
    button_playonce[track_no].configure(bg='#D7E3BC')
                   
def deactivatePlayOnceButton(track_no):
    button_playonce[track_no].config(relief=RAISED)
    button_playonce[track_no].configure(bg='#F0F0F0')         

def activatePlayPauseButton(track_no):
    button_playpause[track_no].config(relief=SUNKEN)
    button_playpause[track_no].configure(bg='#D7E3BC')
                   
def deactivatePlayPauseButton(track_no):
    button_playpause[track_no].config(relief=RAISED)
    button_playpause[track_no].configure(bg='#F0F0F0') 


# Create widgets
frame = Frame(root)                     # Create the main container
frame.pack(fill=BOTH, expand=True)      # Lay out the main container, specify that we want it to grow with window size

xml_frame = LabelFrame(frame, text = 'General', padx=1, pady=1) #, borderwidth=0, highlightthickness=0)
xml_frame.pack(padx=3, pady=1)

global new_general_track_volume_set
new_general_track_volume_set = False

def set_new_general_volume(event):
    global new_general_track_volume_set
    new_general_track_volume_set = True

xml_scroll_bar = Scale(xml_frame, from_=0, to=100, orient=HORIZONTAL, command=set_new_general_volume)     # Slider volume bars
xml_scroll_bar.set(100)
xml_scroll_bar.grid(row=0, column=0, columnspan=1, padx=5, pady=5, sticky=E)

xml_button_playpause = Button(xml_frame, text='Play/Pause', command=button_xml_play_pause_pressed)
xml_button_playpause.grid(row=0, column=1, columnspan=1, padx=5, pady=5, sticky=E)

track_frame = [0]*8
for i in range(0,8):
	track_frame[i] = LabelFrame(frame, text = 'Track #' + str(i+1), padx=1, pady=1)
	track_frame[i].pack(padx=3, pady=1)

file_name = [0]*8
for i in range(0,8):
	#print(i)
	file_name[i] = Text(track_frame[i], height=1, width=36)
	file_name[i].insert(END, '-')
	file_name[i].configure(background="#E1E1E1")
	file_name[i].grid(row=(i+1), column=0, columnspan=1, padx=5, pady=5, sticky=E)

button_load = [0]*8
for i in range(0,8):
	#print(i)
	button_load[i] = Button(track_frame[i], text=" ... ", command=lambda i=i: button_load_pressed(i))
	button_load[i].grid(row=(i+1), column=1, columnspan=1, padx=(0, 5), pady=5, sticky=E)

global new_track_volume_set
new_track_volume_set = [False]*8

def set_new_track_volume(track_no):
    global new_track_volume_set
    if track_no < len(channels):
        new_track_volume_set[track_no] = True

scroll_bar = [0]*8
for i in range(0,8):
	#print(i)
	scroll_bar[i] = Scale(track_frame[i], from_=0, to=100, orient=HORIZONTAL, command=lambda value, i=i: set_new_track_volume(i))     # Slider volume bars
	scroll_bar[i].set(100)
	#scroll_bar[i].bind("<Configure>", self.reset_scrollregion)
	scroll_bar[i].grid(row=(i+1), column=2, columnspan=1, padx=5, pady=5, sticky=E)

button_playonce = [0]*8
for i in range(0,8):
	#print(i)
	button_playonce[i] = Button(track_frame[i], text='1x', command=lambda i=i: button_play_once_pressed(i))
	button_playonce[i].grid(row=(i+1), column=8, columnspan=1, padx=5, pady=5, sticky=E)

button_playpause = [0]*8
for i in range(0,8):
	#print(i)
	button_playpause[i] = Button(track_frame[i], text='Play/Pause', command=lambda i=i: button_play_pause_pressed(i))
	#button_playpause[i] = Button(track_frame[i], text=u"\u25B6", command=lambda i=i: button_play_pause_pressed(i))
	#button_playpause[i]['font'] = myFont
	button_playpause[i].grid(row=(i+1), column=9, columnspan=1, padx=5, pady=5, sticky=E)

button_mute = [0]*8
for i in range(0,8):
	#print(i)
	button_mute[i] = Button(track_frame[i], text="Mute", command=lambda i=i: button_mute_pressed(i))
	button_mute[i].grid(row=(i+1), column=3, columnspan=1, padx=5, pady=5, sticky=E)
# un muted: u'\U0001F508'
# muted: u'\U0001F507'

button_crossfade = [0]*8
for i in range(0,8):
	#print(i)
	button_crossfade[i] = Button(track_frame[i], text="Crossfade", command=lambda i=i: button_crossfade_pressed(i))
	button_crossfade[i].grid(row=(i+1), column=4, columnspan=1, padx=5, pady=5, sticky=E)

button_random = [0]*8
for i in range(0,8):
	#print(i)
	button_random[i] = Button(track_frame[i], text="Random", command=lambda i=i: button_random_pressed(i))
	button_random[i].grid(row=(i+1), column=5, columnspan=1, padx=5, pady=5, sticky=E)

combobox_random_amount = [0]*8
for i in range(0,8):
	#print(i)
	combobox_random_amount[i] = ttk.Combobox(track_frame[i], width=6, values=["1x", "2x", "3x", "4x", "5x", "6x", "7x", "8x", "9x", "10x"])
	combobox_random_amount[i].set("1x")
	combobox_random_amount[i].bind("<<ComboboxSelected>>", lambda event, track_no=i : random_amount_click(event, track_no))
	combobox_random_amount[i].bind('<Return>', lambda event, track_no=i : random_amount_keyboard(event, track_no))
	combobox_random_amount[i].grid(row=(i+1), column=6, columnspan=1, padx=5, pady=5, sticky=E)
	
combobox_random_timeframe = [0]*8
for i in range(0,8):
	#print(i)
	combobox_random_timeframe[i] = ttk.Combobox(track_frame[i], width=6, values=["1m", "10m", "1h"])
	combobox_random_timeframe[i].set("10m")
	combobox_random_timeframe[i].bind("<<ComboboxSelected>>", lambda event, track_no=i : random_timeframe_click(event, track_no))
	combobox_random_timeframe[i].bind('<Return>', lambda event, track_no=i : random_timeframe_keyboard(event, track_no))
	combobox_random_timeframe[i].grid(row=(i+1), column=7, columnspan=1, padx=5, pady=5, sticky=E)


# Place cursor in entry box by default
#button_load[0].focus()



















def chop_interval(num, prec, max, len):
    values = []
    num += 1
    for i in range(num):
        values.append(random.randint(0, prec))
    norm = sum(values)
    anc = 0
    max_ar = max - 1.5*len*num
    for i in range(num):
        old = values[i]
        values[i] += anc
        anc += old
        values[i] /= norm
        values[i] *= max_ar+i*1.5*len
        values[i] = int(values[i])
    return values

class Channel():
    def __init__(self, channel_id, sound_id, name = "", volume = 100, random = False, random_counter = 1, random_unit = "1h", mute = False, balance = 0):
        try:
            self.sound_object = pygame.mixer.Sound(pygame.mixer.Sound("sounds_named/{}.ogg".format(sound_id)))
        except:
            print('Error while loading sound "sounds_named/{}.ogg". Did you convert it to ogg?'.format(sound_id))
            sys.exit()
        self.channel_object = pygame.mixer.Channel(channel_id)
        self.MUSIC_END = pygame.USEREVENT+1
        self.channel_object.set_endevent(self.MUSIC_END)

        self.fade_length = 500
        self.sound_length = self.sound_object.get_length() * 1000
        self.start_time = millis()

        global play_general, play_general_recently_reactivated, play_track, play_track_recently_reactivated
        play_general = True
        play_general_recently_reactivated = False
        play_track = [True]*8
        play_track_recently_reactivated = [False]*8


        self.name = name
        global file_name
        file_name[channel_id].delete('1.0', END)
        file_name[channel_id].insert(END, self.name + ' [' + str(round(self.sound_object.get_length(),1)) + 's]')
        file_name[channel_id].configure(background="#FFFFFF")
        start_index = len(self.name) + 1
        end_index = start_index + 7
        file_name[channel_id].tag_add("start", '1.' + str(start_index), '1.' + str(end_index))
        file_name[channel_id].tag_config("start", foreground="#9F9F9F")
        #file_name[channel_id].tag_config("start", foreground='blue')


        #print("length", self.sound_length)
        #print("self.start_time", self.start_time/1000.0)
        self.muteStatus = mute
        #print('muteStatus track #{}: {}'.format(self.channel_id, self.muteStatus))
        self.previously_muted = False
        self.volume = volume
        self.volume_before_mute = self.volume
        global scroll_bar
        global xml_scroll_bar
        scroll_bar[channel_id].set(self.volume)
        print('mute on track #{}: {}'.format(channel_id, mute))
#        if not self.muteStatus:
#            self.sound_object.set_volume( (int(self.volume)/100.0) * (int(xml_scroll_bar.get()) / 100.0) )   #Normalize volume
#        else:
#            print('muteStatus present on track #', channel_id)
#            self.sound_object.set_volume( 0 )   #Normalize volume
        #Adjust balance
        self.balance = balance
#        self.left_volume = 1.0 if (balance <= 0) else (1.0-float(balance)/100)
#        self.right_volume = 1.0 if (balance >= 0) else (1.0+float(balance)/100)
#        self.channel_object.set_volume(self.left_volume, self.right_volume)
        
        #Set random
        self.channel_id = channel_id
        self.sound_id = sound_id
        self.random = random
        if self.random:
            self.setRandom(True)
        self.setVolume()
        self.random_counter = random_counter
        global combobox_random_amount
        combobox_random_amount[self.channel_id].set(str(self.random_counter) + 'x')
        self.random_unit = random_unit
        global combobox_random_timeframe
        combobox_random_timeframe[self.channel_id].set(str(self.random_unit))
        self.play_at = []
        self.current_tick = 0
        self.play_once_running = False
        if self.muteStatus:
            self.muteChannel(True)
            
        if self.random:
            self.crossfade = False
            button_crossfade[self.channel_id].config(relief=RAISED)
        else:
            self.crossfade = True
            self.setCrossfade(self.crossfade)
       
        self.fade_running = False
        self.playing = True

    
    def __repr__(self):
        if(self.random):
            return "Channel {channel_id} : {name} (random {ran} per {unit}), {sound_id}.ogg (volume {vol}, balance {bal})".format(
            channel_id=self.channel_id,
            name=self.name,
            sound_id=self.sound_id,
            vol=self.volume,
            bal=self.balance,
            ran=self.random_counter,
            unit=self.random_unit)
        else:
            return "Channel {channel_id} : {name} (looping), {sound_id}.ogg (volume {vol}, balance {bal})".format(
            channel_id=self.channel_id,
            name=self.name,
            sound_id=self.sound_id,
            vol=self.volume,
            bal=self.balance)
            
#    def setVolume(self, volume):
#        self.volume = volume
#        #scroll_bar[self.channel_id].set(self.volume)
#        #print('volume before mute: ', self.volume_before_mute)
#        #print('new volume: ', volume)
#        #print('int(xml_scroll_bar.get()): ', int(xml_scroll_bar.get()))
##        if not self.muteStatus:
#        self.sound_object.set_volume( (int(self.volume)/100.0) * (int(xml_scroll_bar.get()) / 100.0) )
##        if self.volume==0 and self.muteStatus:
##            self.sound_object.set_volume( (int(self.volume)/100.0) * (int(xml_scroll_bar.get()) / 100.0) )

    def setVolume(self):
        global global_volume
        global_volume = xml_scroll_bar.get()                 # update global volume from current global volume scroll bar position
        self.volume = scroll_bar[self.channel_id].get()      # update volume of channel object from current track volume scroll bar position
        l_balance = min(1, 1.0-float(self.balance)/50)
        r_balance = min(1, 1.0+float(self.balance)/50)
        self.channel_object.set_volume( (float(global_volume)/100.0) * (float(self.volume)/100.0) * l_balance, (float(global_volume)/100.0) * (float(self.volume)/100.0) * r_balance )
        if self.muteStatus:
            self.volume_before_mute = self.volume
            self.sound_object.set_volume(0)
            button_mute[self.channel_id].config(relief=SUNKEN)
        else:
            self.sound_object.set_volume(float(self.volume_before_mute))
            button_mute[self.channel_id].config(relief=RAISED)

    def setRandom(self, force=False):
        self.random = not self.random
        if force:
            self.random = True
        if self.random:
            #print('set random: ', self.name)
            button_random[self.channel_id].config(relief=SUNKEN)
            self.play()
        else:
            #print('cancel random: ', self.name)
            button_random[self.channel_id].config(relief=RAISED)
            self.play()

    def setCrossfade(self, force=False):
        self.crossfade = not self.crossfade
        if force:
            self.crossfade = True
        if self.crossfade:
            #print('set crossfade: ', self.crossfade)
            button_crossfade[self.channel_id].config(relief=SUNKEN)
        else:
            #print('cancel crossfade: ', self.crossfade)
            button_crossfade[self.channel_id].config(relief=RAISED)

    def muteChannel(self, force=False):
        global button_mute
        self.muteStatus = not self.muteStatus
        if force:
            self.muteStatus = True
        self.setVolume()
#        if self.muteStatus:
#            #print('muting channel: ', self.name)
#            self.volume_before_mute = self.volume
#            self.sound_object.set_volume( 0 )
#            button_mute[self.channel_id].config(relief=SUNKEN)
#        else:
#            #print('unmuting channel: ', self.name)
#            #print('self.volume_before_mute: ', self.volume_before_mute)
#            self.setVolume( self.volume_before_mute )
#            button_mute[self.channel_id].config(relief=RAISED)
#            #self.play()
            
    def setRandomAmount(self, random_amount):
        self.random_counter = random_amount
        #print('amount set to: ', random_amount)
        
    def setRandomTimeframe(self, random_timeframe):
        self.random_unit = random_timeframe
        #print('timeframe set to: ', random_timeframe)

    def compute_next_ticks(self):
        val = unit_duration_map[self.random_unit]
        sound_len = self.sound_object.get_length()*1.5
        self.play_at = chop_interval(self.random_counter, 100, val, sound_len)

    def play(self, force = False):
        global play_track
        global play_track_recently_reactivated
#        print('mute: ', self.muteStatus)
#        print('crossfade: ', self.crossfade)
#        print('random: ', self.random)
#        print('force: ', force)
        if(not self.random):
            if self.crossfade and not self.random:
                self.channel_object.play(self.sound_object, loops = -1, fade_ms=self.fade_length)
            else:
                self.channel_object.play(self.sound_object, loops = -1)
        elif(force):
            if self.crossfade and not self.random:
                self.channel_object.play(self.sound_object, fade_ms=self.fade_length)
            else:
                self.channel_object.play(self.sound_object)
        play_track[self.channel_id] = True
        play_track_recently_reactivated[self.channel_id] = True  
        activatePlayPauseButton(self.channel_id)
        #print('playing channel / id: {} / {}'.format(self.name, self.channel_id))
        
        #play(loops=0, maxtime=0, fade_ms=0)

    def playOnce(self):
        global play_track
        global play_track_recently_reactivated
        if self.play_once_running:
            if self.previously_muted:
                #print('stopping play 1x from NOT muted')
                self.muteChannel(True)
            if not play_track[self.channel_id] or self.random:
                self.pause()
            else:
                self.play(True)
            deactivatePlayOnceButton(self.channel_id)
            self.previously_muted = False  
            self.play_once_running = False                           
            return False
        if not self.muteStatus:
            #print('starting play 1x from NOT muted')
            self.start_time = millis()
            self.sound_length = self.sound_object.get_length() * 1000
            self.channel_object.play(self.sound_object, loops = 0)
            self.previously_muted = False
            self.play_once_running = True            
        else:
            #print('starting play 1x from muted')
            self.muteChannel()
            self.previously_muted = True
            self.start_time = millis()
            self.sound_length = self.sound_object.get_length() * 1000            
            self.channel_object.play(self.sound_object, loops = 0)
            self.play_once_running = True
        
        activatePlayOnceButton(self.channel_id)

        #print('playing 1x channel / id: {} / {}'.format(self.name, self.channel_id))
        return True

    def stop(self, force = False):
        self.channel_object.stop()
        if not self.play_once_running:
            deactivatePlayPauseButton(self.channel_id)
        #print('stopping channel: ', self.name)
            
    def pause(self, force = False):
        #print('pausing channel: ', self.name)
        self.channel_object.pause()
        if not self.play_once_running:
            deactivatePlayPauseButton(self.channel_id)

    def unpause(self, force = False):
        #print('unpausing channel: ', self.name)
        self.channel_object.unpause()
        activatePlayPauseButton(self.channel_id)
            
#    def quitChannel(self):
#        print('unloading channel: ', self.name)
#        self.channel_object.stop()
#        #self.channel_object.quit()
#        pygame.quit()
        
    def tick(self, force=False):
        if self.crossfade and not self.random:
            if millis() >= (self.start_time + self.sound_length - self.fade_length) and not self.fade_running:
                self.sound_object.fadeout(self.fade_length)
                self.fade_running = True
            if millis() >= (self.start_time + self.sound_length):
                self.fade_running = False
                self.stop()
                self.start_time = millis()
                self.play()

        if(self.random and not self.muteStatus) or (force and not self.muteStatus):
            if(len(self.play_at) > 0):
                self.current_tick += 1
                ref = self.play_at[0]
                if(self.current_tick > ref):
                    #print("Playing : {}".format(self.play_at))
                    self.play_at.pop(0)
                    if(len(self.play_at) >= 1):
                        self.play(True)
            else:
                self.current_tick = 0
                self.compute_next_ticks()
                #print("Recomputed : {}".format(self.play_at))

def load_file(xml_file):
    obj = untangle.parse(xml_file)
    ls = []
    for chan_num in range(1,9):
        channel = getattr(obj.audio_template, "channel{}".format(chan_num))
        dic = {}
        #dic["sound_id"] = channel.id_audio.cdata
        dic["sound_id"] = channel.name_audio.cdata
        dic["random"] = (channel.random.cdata == "true")
        dic["mute"] = (channel.mute.cdata == "true")
        dic["name"] = channel.name_audio.cdata
        dic["volume"] = channel.volume.cdata
        dic["balance"] = int(channel.balance.cdata)
        dic["random_counter"] = int(channel.random_counter.cdata)
        dic["random_unit"] = channel.random_unit.cdata
        ls.append(dic)
        #print('dic: ', dic)
    return ls

def bootstrap_chanlist(chans_to_load):
    #print('chans_to_load: ', chans_to_load)
    global channels
    channels = []
    #print('chans_to_load: ', chans_to_load)
    for(c_id, c_val) in enumerate(chans_to_load):
        #print('c_val track #{}: {}'.format(c_id, c_val))
        #print('type(c_val): ', c_val)
        if c_val["sound_id"] not in ('','0','-'):
            channels.append(Channel(c_id, **c_val))
    #print('channels: ', channels)
    for channel in channels:
        print('Loaded {}.'.format(channel))
    for channel in channels:
        channel.play()
    #print('Press CTRL+C to exit.')
    
            
def task():
    global channels
    global new_track_volume_set
    global new_general_track_volume_set
    #if play_general:
    for track_no, channel in enumerate(channels):
        if new_track_volume_set[track_no] or new_general_track_volume_set:
            channels[track_no].setVolume()
            new_track_volume_set[track_no] = False
            if track_no >= len(channels)-1:
                new_general_track_volume_set = False
            #print('track #{} new volume {} set'.format(track_no, scroll_bar[track_no].get()))
        if play_track[track_no]:
            channel.tick()
    #if channels[0].play_once_running or channels[1].play_once_running or channels[2].play_once_running or channels[3].play_once_running or channels[4].play_once_running or channels[5].play_once_running or channels[6].play_once_running or channels[7].play_once_running:
    for track_no, channel in enumerate(channels):
        if channel.play_once_running and (millis() >= (channel.start_time + channel.sound_length)):
            #print('stopping play 1x with tick (end of file)')
            if channel.previously_muted:
                channel.muteChannel(True)       
            deactivatePlayOnceButton(channel.channel_id)
            if play_track[track_no]:
                channel.play()
            else:
                channel.channel_object.stop()
            channel.play_once_running = False
    root.after(CLOCK_TICKER, task)  # reschedule event in CLOCK_TICKER seconds

from docopt import docopt
if __name__ == "__main__":
    #arguments = docopt(__doc__, version = '0.1ß')
    #bootstrap_chanlist(load_file(arguments.get('<file>')))
    initPyGameMixer()
    bootstrap_chanlist(load_file(xml_file))
    root.after(CLOCK_TICKER, task)
    mainloop()
    
    
    