
import requests
import streamlit as st
import pandas as pd
from datetime import datetime
import time


API_KEY = st.secrets["API_KEY"]
CITY = "Mwanza, TZ"
st.set_page_config(page_title="Unshakable Energy", page_icon="☀️", layout="wide")

def get_weather():
  API_URL=f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API-kEY}&units=metric&lang=sw"
  with st.spinner('Inapakia data ya hali ya hewa... ⛅ Tafadhali subiri 10sec'):
    response = requests.get(url)
    data = response.json()
 
  return data
  st.title("☀️ UNSHAKABLE ENERGY - AI SOLAR PREDICTION")
  st.subheader(f"⛅ Hali ya Hewa Mwanza - saa 24 zijazo")
  for item in data['list'][:8]: # saa 8 = 24 saa
    time = datatime.fromtimestamp(item['dt']).strftime('%d/%m %H:%M')
    temp = item['main']['temp']
    cloud = item['clouds']['all'] # % ya mawingu ndio muhimu kwa jua
    weather = item['weather'][0]['description']

    col1,col2,col3 = st.columns(3)
    col1.write(f"**{time}**")
    col2.write(f"{weather} | {temp}°C")
    col3.write(f"Mawingu: {cloud}%")

    if cloud < 20:
      st.success("☀️ PREDICTION: Jua kali - power itakuwa JUU ")
    elif cloud < 60:
      st.warning("⛅ PREDICTIO:Jua la kawaida- Power ya kati, dhibiti matumizi")
    else:
      st.error("☁️ PREDICTION: Mawingu meng - Power itakuwa chini ,chaji betri leo")
    st.divider()
