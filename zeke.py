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

sonos = {}

#############################################################################################

def get_time_here():
    import time
    time.ctime()
    os.system("say 'The time is'" + str(time.strftime('%l:%M%p %Z')))

#############################################################################################

def query_time(command):
    if "in" in command:
        list_of_words = command.split()
        location = list_of_words[list_of_words.index("in") + 1]
        print location
    else:
        get_time_here()

#############################################################################################

def get_date():
    import time
    time.ctime()
    os.system("say 'The date is'" + str(time.strftime('%b %d, %Y')))

#############################################################################################

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

def pause_sonos():
    try:
        current_sonos_device.pause()
        os.system("say 'Pausing'")
    except:
        os.system("say 'There is nothing to pause.")

#############################################################################################

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
        os.system("say 'Couldn't skip")

#############################################################################################

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
        os.system("say 'Couldn't rewind")

#############################################################################################

def modify_volume_sonos(change):
    if change == 1:
        current_sonos_device.volume += 10
    elif change == -1:
        if current_sonos_device.volume > 0:
            current_sonos_device.volume -= 10

#############################################################################################

def get_num_volume(command):
    list_of_words = command.split()
    if "to" in command:
        num = list_of_words[list_of_words.index("to") + 1]
    else:
        num = list_of_words[list_of_words.index("volume") + 1]
    return num

#############################################################################################

def set_volume_sonos(num):
    os.system("say 'Setting volume to'" + str(num))
    current_sonos_device.volume = num

#############################################################################################

def recordAudio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)

    data = ""
    try:
        data = r.recognize_google(audio)
        print("You said: " + data)
    except sr.UnknownValueError:
        os.system("say 'I couldn't understand what you said'")
    except sr.RequestError as e:
        print("Could not request results from Speech Recognition service; {0}".format(e))
    return data

#############################################################################################

def contains(text):
    if "Sonos" in text and "master" in text:
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
        os.system("say 'Goodbye!'")
        sys.exit()
    else:
        os.system("say 'I couldn't understand what you said'")

#############################################################################################

def main():
    os.system("say 'Hello. My names Zeke. How can I help you today?'")
    while 1:
        data = recordAudio()
        zeke(data)

#############################################################################################

main()
