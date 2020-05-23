import datetime
import streamlit as st
#from playsound import playsound
def alarm(alarmH,alarmM,ap):
    if ap == 'pm':
        alarmH=alarmM+12
    while(True):
        if(alarmH==datetime.datetime.now().hour and alarm==datetime.datetime.now().minute):
            st.write("Time to wake up")
            audio_file=open("song.mp3","rb")
            st.audio(audio_file,format='audio/mp3')
            break


           

