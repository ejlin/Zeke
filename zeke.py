
################################################################################
# Name: Eric Lin                                                               #
# Date: June 22nd, 2017                                                        #
################################################################################

import os
import time
import string
import speech_recognition as sr

################################################################################

sonos = {}
current_device = list(soco.discover())[0]

################################################################################

def play_sonos(room):

    import soco

    for zone in soco.discover():
        print zone.player_name
        if zone.player_name == room:
            current_device = zone
            print current_device
            print zone
            track = zone.get_current_track_info()
            os.system("say 'Now playing;'" + track['title'] + "by" + track['artist'])
            zone.play()

################################################################################

def pause_sonos():
    os.system("say 'Pausing'")
    print current_device.player_name
    current_device.pause()

################################################################################

def main():

    while True:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            audio = r.listen(source)
            command = r.recognize_google(audio)
            print command
            if command == "play Sonos":
                play_sonos("Eric's Bedroom")
            elif command == "play Sonos in Master's room":
                play_sonos("Master Bedroom")
            elif command == "play Sonos in Eric's room":
                play_sonos("Eric's Bedroom")
            elif command == "play Sonos in family room":
                play_sonos("Family Room")
            elif command == "play Sonos in office":
                play_sonos("Office")
            elif command == "pause Sonos":
                pause_sonos()
            elif command == "close":
                break

################################################################################

main()
