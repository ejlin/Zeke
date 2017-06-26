#############################################################################################
# Name: Eric Lin                                                                            #
# Date: June 22nd, 2017                                                                     #
#############################################################################################

import os
import time
import string
import soco
import sys
import speech_recognition as sr

#############################################################################################

# This is where our global variables will go

#############################################################################################

# Name: get_time_here()
# Parameters: None
# Description: This function will return the local time and convert it from text to speech

def get_time_here():
    time.ctime()
    os.system("say 'The time is'" + str(time.strftime('%l:%M%p %Z')))

#############################################################################################

# Name: query_time()
# Parameters: Takes in a single variable string 'command' of the spoken command.
# Description: This function will take in a string command and return the time of the
#              location given in the command. This function will parse the string until it
#              finds a location, otherwise it will simply return local time.

def query_time(command):
    if "in" in command:
        list_of_words = command.split()
        location = list_of_words[list_of_words.index("in") + 1]
        print location
    else:
        get_time_here()

#############################################################################################

# Name: get_date()
# Parameters: None
# Description: This function will return the current date of the current location.

def get_date():
    time.ctime()
    os.system("say 'The date is'" + str(time.strftime('%b %d, %Y')))

#############################################################################################

# Name: play_sonos(room)
# Parameters: This function takes in a parameter of type 'room'
# Description: This function allows us to play sonos in the specified room that was passed in

def play_sonos(room):

    for zone in soco.discover():
        print zone.player_name
        if zone.player_name == room:
            global current_sonos_device
            current_sonos_device = zone
            track = zone.get_current_track_info()
            try:
                os.system("say 'Now playing;'" + track['title'] + "by" + track['artist'])
            except:
                os.system("say 'Now playing'")
            zone.play()

#############################################################################################

# Name: pause_sonos()
# Parameters: None
# Description: This function will pause the sonos device currently playing.

def pause_sonos():
    try:
        current_sonos_device.pause()
        os.system("say 'Pausing'")
    except:
        os.system("say 'There is nothing to pause.")

#############################################################################################

# Name: next_track_sonos()
# Parameters: None
# Description: This function will play the next song in the queue of the device currently
#              playing music.

def next_track_sonos():
    try:
        current_sonos_device.next()
        track = current_sonos_device.get_current_track_info()
        os.system("say 'Skipping to next track'")
        try:
            os.system("say 'Now playing;'" + track['title'] + "by" + str(track['artist']))
        except:
            os.system("say 'Now playing'")
    except:
        os.system("say 'Could not skip")

#############################################################################################

# Name: previous_track_sonos()
# Parameters: None
# Description: This function will play the previous song in the queue of the device currently
#              playing music.

def previous_track_sonos():
    try:
        current_sonos_device.previous()
        track = current_sonos_device.get_current_track_info()
        os.system("say 'Back to the last track'")
        try:
            os.system("say 'Now playing;'" + track['title'] + "by" + str(track['artist']))
        except:
            os.system("say 'Now playing'")
    except:
        os.system("say 'Could not rewind")

#############################################################################################

# Name: modify_volume_sonos(change)
# Parameters: This funtion takes in an integer parameter of either 1 or -1
# Description: This function will either change the volume by +10 or -10 depending on whether
#              +1 or -1 was passed in.

def modify_volume_sonos(change):
    if change == 1:
        current_sonos_device.volume += 10
    elif change == -1:
        if current_sonos_device.volume > 0:
            current_sonos_device.volume -= 10

#############################################################################################

# Name: get_num_volume(command)
# Parameters: This function takes in a string parameter 'command'
# Description: This function will allow us to return an int according to the string passed
#              in.

def get_num_volume(command):
    list_of_words = command.split()
    if "to" in command:
        num = list_of_words[list_of_words.index("to") + 1]
    else:
        num = list_of_words[list_of_words.index("volume") + 1]
    return num

#############################################################################################

# Name: set_volume_sonos(num)
# Parameters: This function takes in an int 'num'
# Description: This function takes in a num to set the volume of the currently playing sonos
#              device to the passed in parameter.

def set_volume_sonos(num):
    os.system("say 'Setting volume to'" + str(num))
    current_sonos_device.volume = num

#############################################################################################

# Name: contains(text)
# Parameters: This function takes in a parameter of type string 'command'
# Description: This function takes in a strng and checks if it contains certain strings and
#              returns accordingly responses.

def contains(text):
    if "Sonos" in text and ("master" in text or "master's" in text or "Master's" in text):
        return "play Sonos in Master's room"
    elif "Sonos" in text and "Eric" in text:
        return "play Sonos in Eric's room"
    elif "Sonos" in text and "family" in text:
        return "play Sonos in Eric's room"
    elif "Sonos" in text and "office" in text:
        return "play Sonos in office"
    elif "Sonos" in text:
        return "play Sonos"

#############################################################################################

# Name: play_commands(command)
# Parameters: This function takes in a parameter string 'command'
# Description: This function will take in a string command and then perform an action
#              accordingly. This function is for Sonos play commands only.

def play_commands(command):
    if contains(command) == "play Sonos":
        play_sonos("Eric's Bedroom")
    elif contains(command) == "play Sonos in Master's room":
        play_sonos("Master Bedroom")
    elif contains(command) == "play Sonos in Eric's room":
        play_sonos("Eric's Bedroom")
    elif contains(command) == "play Sonos in family room":
        play_sonos("Family Room")
    elif contains(command) == "play Sonos in office":
        play_sonos("Office")

#############################################################################################

# Name: goodbye()
# Parameters: None
# Description: This function will say "goodbye" and then exit the zeke program.

def goodbye():
    os.system("say 'Goodbye!'")
    sys.exit()

#############################################################################################

# Name: zeke(command)
# Parameters: This function takes in a string parameter 'command'
# Description: This function will take in a string command and perform actions
#              correspondingly.

def zeke(command):
    if "play" in command:
        play_commands(command.replace('play', ''))
    elif "time" in command:
        query_time(command)
    elif "date" in command:
        get_date()
    elif "pause" in command and "Sonos" in command:
        pause_sonos()
    elif "next" in command or "skip" in command:
        next_track_sonos()
    elif "go back" in command or "previous" in command:
        previous_track_sonos()
    elif "lower" in command and "volume" in command:
        modify_volume_sonos(-1)
    elif "raise" in command and "volume" in command:
        modify_volume_sonos(1)
    elif "set" in command and "volume" in command:
        set_volume_sonos(get_num_volume(command))
    elif "goodbye" in command or "good-bye" in command:
        goodbye()
    else:
        os.system("say 'I could not understand what you said'")

#############################################################################################

# Name: record_audio()
# Parameters: None
# Description: This funtion will record audio frm the default microphone and using the
#              google_speech recognition API, convert it into text, which it will then return

def record_audio():

    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)

    data = ""
    try:
        data = r.recognize_google(audio)
        print("You said: " + data)
    except sr.UnknownValueError:
        os.system("say 'I could not understand what you said'")
    except sr.RequestError as e:
        print("Could not request results from Speech Recognition service; {0}".format(e))
    except:
        print("Could not return meaningful data")
    return data

#############################################################################################

# Name: main()
# Parameters: None
# Description: This is our main function that will stitch together our recorded audio and
#              corresponding actions.

def main():
    os.system("say 'Hello. My names Zeke. How can I help you today?'")
    while 1:
        data = record_audio()
        zeke(data)

#############################################################################################

# Call our 'main' function here
main()
