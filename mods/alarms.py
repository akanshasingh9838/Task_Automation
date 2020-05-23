import datetime
import streamlit as st
from threading import Thread

def run(alarmH,alarmM):
    while(True):
        if(alarmH==datetime.datetime.now().hour and alarmM==datetime.datetime.now().minute):
            st.write("Time to wake up")
            audio_file=open("song.mp3","rb")
            st.audio(audio_file,format='audio/mp3')
            break

def activate_alarm(alarmH,alarmM):
    process = Thread(target=run,args=[alarmH,alarmM])
    process.start()
    return True