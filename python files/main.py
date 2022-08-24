import os # for removing the path of file from filename varible and printing the name of the file only
from tkinter import *
import tkinter.messagebox # for message box
from tkinter import filedialog # for importing file from any location
from mutagen.mp3 import MP3 # for accessing mp3 files
import time # for passing the value in seconds
import threading # since our program hanged due to current time while loop
from tkinter import ttk # for themes -> ttk stands for themed tkinter
from pygame import mixer # for audio controls -> mixer class
from ttkthemes import themed_tk as tk # for themes and styling the GUI


# Root window contains - Statusbar , Leftframe , Rightframe
# Leftframe - The listbox playlist
# Rightframe - Topframe , Middleframe and Bottom frame

root = tk.ThemedTk()   # Creating a main window
root.get_themes()      # Returns a list of all themes that can be set
root.set_theme("radiance") # sets an available theme

# Fonts - Arial (corresponds to Helevetical) , Courier New (Courier) , Comic Sans MS. , Fixedays ,
# MS Sans Serif, MS Serif , Symbol , System , Times New Roman (Times) and Verdana
#
# Styles - normal , bold , roman , italic , underline and overstrike

statusbar = ttk.Label(root, text = "Welcome to Music Adda",relief = SUNKEN, anchor = W,font = 'Times 10 italic') # SUNKEN gives the border around text, W stands for west
# anchor moves the text inside the status bar
statusbar.pack(side = BOTTOM, fill = X) # Bottom gives text at bottom , X means X axis and it will fill/complete the whole X axis
# or left to right if we write Y then nothing will happen as there are lot of widgets in y axis


# Create the menubar
menubar = Menu(root) # Created a blank menu bar
root.config(menu = menubar) # configuration of menu bar is important because the menu bar should always be at the top and menu bar should be ready to receive the sub -menus

# Create the submenu

subMenu = Menu(menubar, tearoff = 0) # to remove the dashed line from the top use tearoff

playlist = []

# playlist - contains full path + filename
# playlistbox - contains only filename
# fullpath + filename is required to play the music inside play_music load function

def browse_file():
    global filename_path # now filename becomes the global variable
    filename_path = filedialog.askopenfilename() # finalname is a variable since we have to open a file/music or browse the window so we are
    # saying that askopenfilename() other wise the command would be different
    # filename stores the path of the file
    add_to_playlist(filename_path)

def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlist_box.insert(index, filename)
    playlist.insert(index,filename_path)
    index += 1


menubar.add_cascade(label="File",menu=subMenu)
subMenu.add_command(label="Open",command = browse_file)
subMenu.add_command(label="Exit",command = root.destroy) # command is for exiting the music player

def About_us():
    tkinter.messagebox.showinfo("About Music Adda","This is a music player build using Python tkinter by @nigam1081") # shows the info that we want to print when we click on about us section in music player



subMenu = Menu(menubar, tearoff = 0)
menubar.add_cascade(label="Help",menu=subMenu)
subMenu.add_command(label="About Us",command = About_us)


mixer.init() # initializing the mixer -> very important


#root.geometry("300x300") # This is for giving the dimension of the screen when it opens initially.Don't use any space.Use the format as given
root.title("Music Adda") # This is for title
root.iconbitmap(r'Images/Music Adda.ico') # r means raw string it is used whenever we want to enter any location we enter location in single quotes

leftframe = Frame(root)
leftframe.pack(side = LEFT,padx = 30,pady = 30)   # pack() stacks objects from top to bottom

playlist_box = Listbox(leftframe)
playlist_box.pack()

addbtn = ttk.Button(leftframe,text ="+ Add",command = browse_file)
addbtn.pack(side = LEFT)

def del_song():
    selected_song = playlist_box.curselection()  # returns tuple and in that tuple there is the position/index of the song
    selected_song = int(selected_song[0])
    playlist_box.delete(selected_song)
    playlist.pop(selected_song)

delbtn = ttk.Button(leftframe, text = "- Delete",command = del_song)
delbtn.pack(side = LEFT)

rightframe = Frame(root)
rightframe.pack(pady = 30)

topframe = Frame(rightframe)
topframe.pack()


# Whenever we want to enter anything in the tkinter window it is called a  --> WIDGET
#filelabel = Label(root,text="Let's make some noise!!") # Label is a widget for text
# First parameter is name of the tkinter window and second one is what text we want
#filelabel.pack() # This is for displaying the text .Without this the text will not be displayed

lengthLabel = ttk.Label(topframe,text = "Total Length : --:--")
lengthLabel.pack(pady = 5)

currenttimeLabel = ttk.Label(topframe,text = "Current Time : --:--",relief = GROOVE)
currenttimeLabel.pack()

def show_details(play_song):
    global total_length
    #filelabel['text'] = "Playing" + " - " + os.path.basename(filename)

    file_data = os.path.splitext(play_song)

    if file_data[1] == ".mp3":
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        length_of_file = mixer.Sound(play_song) # mixer.Sound is for files other than mp3
        total_length = length_of_file.get_length()

    # div - total_length / 60 mod - total_length % 60
    mins,seconds = divmod(total_length, 60)
    mins = round(mins)
    seconds = round(seconds)
    timeformat = "{:02d}:{:02d}".format(mins,seconds)
    lengthLabel['text'] = "Total Length" + " - " + timeformat


    thread = threading.Thread(target=start_count)
    thread.setDaemon(True) # screen shot in music player folder
    thread.start()

def start_count(): # t will be received in seconds
    global total_length
    global paused
    # continue ignores all statements below it: we check if music is paused or not
    current_time  = 0
    while current_time <= total_length and mixer.music.get_busy():
        # mixer.music.get_busy() function returns FALSE as soon as the stop button is pressed or music stops playing
        if paused:
            continue
        else:
            mins, seconds = divmod(current_time, 60)
            mins = round(mins)
            seconds = round(seconds)
            timeformat = "{:02d}:{:02d}".format(mins, seconds)
            currenttimeLabel['text'] = "Current Time" + " - " + timeformat
            time.sleep(1) # it takes values in seconds
            current_time += 1

            

def play_music():
    global paused

    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music Resumed"
        paused = FALSE
    else:
        try:
            stop_music()  # before switching it will stop the music
            time.sleep(1) # it has buffer time of 1s before switching the music because in threading the difeerenece between each iteration is 1s
            selected_song = playlist_box.curselection() # returns tuple and in that tuple there is the position/index of the song
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing Music" + " - " + os.path.basename(play_it)
            show_details(play_it)
        except NameError:
            tkinter.messagebox.showerror("File Not Found","Music Adda could not find the file.Please check again")
   # try:
    #    paused # checks whether pause varible is initilaized or not or pause button is pressed or not
    #except NameError: # if not initialized it executes the except condition
    
    #else: # if initialized it goes under else condition'''

def rewind_music():
    play_music()
    statusbar['text'] = "Music Rewinded"

muted = FALSE

def mute_music():
    global muted
    if muted: # if music is muted or muted == TRUE then unmute the music
        mixer.music.set_volume(0.7)
        volumeBtn.configure(image = volumephoto)
        scale.set(70)
        muted = FALSE
        statusbar['text'] = "Playing Music"
    else: # if the music is unmuted or muted == FALSE then mute the music
        mixer.music.set_volume(0)
        volumeBtn.configure(image = mutephoto)
        scale.set(0)
        muted = TRUE
        statusbar['text'] = "You have muted the music. Please unmute to restart!"

paused = FALSE

def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music Paused"

def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music Stopped"

def set_Vol(val): # automatically the value comes of the increase and decrease will come in val variable
    volume = float(val)/100 # because default type of val is string
    mixer.music.set_volume(volume) # dividing by 100 because mixer class set_volume function always takes values between 0 and 1 e.g -> 0.1,0.99 etc

# creating a middle-frame for play, pause and stop etc.

middleframe = Frame(rightframe)
middleframe.pack(padx = 30, pady = 30)

# bottom frame for mute, volume, rewind etc

bottomframe = Frame(rightframe)
bottomframe.pack()

Playphoto = PhotoImage(file ='Images/Play.png') # Photo image is a widget that enables us to add photos in the tkinter window
#labelphoto = Label(root,image = photo) # Here Label is acting as container
#labelphoto.pack()
playBtn = ttk.Button(middleframe,image = Playphoto, command = play_music)
playBtn.grid(row = 0, column = 0,padx = 10) # side = left helps position the elements of the widgets in a proper manner

Stopphoto = PhotoImage(file ='Images/Stop.png')
stopBtn = ttk.Button(middleframe,image = Stopphoto, command = stop_music)
stopBtn.grid(row = 0, column = 1,padx = 10)

Pausephoto = PhotoImage(file ='Images/Pause.png')
pauseBtn = ttk.Button(middleframe,image = Pausephoto, command = pause_music)
pauseBtn.grid(row = 0, column = 3, padx = 10)

# rewind button just restarts the music
rewindphoto = PhotoImage(file ='Images/Rewind.png')
rewindBtn = ttk.Button(bottomframe,image = rewindphoto, command = rewind_music)
rewindBtn.grid(row = 0, column = 0)

# mute button makes volume 0 and when we touch the volume button it again makes the volume from where we left
mutephoto = PhotoImage(file ='Images/mute.png')
volumephoto = PhotoImage(file ='Images/volume.png')
volumeBtn = ttk.Button(bottomframe,image = volumephoto, command = mute_music)
volumeBtn.grid(row = 0, column = 1)

scale = ttk.Scale(bottomframe,from_ = 0, to = 100, orient = HORIZONTAL, command = set_Vol) # for increase and decrease in volume from -> min , to -> max
scale.set(70) # sets the scale default value of music player
mixer.music.set_volume(0.7) # Now internally also the default value of music player is changed to 70 because set_volume takes the volume between 0 to 1
scale.grid(row = 0, column = 2, pady = 15,padx = 30) # we can set the to variable to 1000 also but 100 is quite relevant


def on_closing(): # This makes us handle the close button on the top of the tkinter window
    stop_music()
    root.destroy()

root.protocol("WM_DELETE_WINDOW",on_closing)




root.mainloop() # Persisting that window to remain there only because the window is created for small duration.
# this should always be always at bottom



# START FROM DAY 26