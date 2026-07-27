import requests
import streamlit as st
import pandas as pd
from datetime import datetime
import time


API_KEY = st.secrets["API_KEY"]
CITY = "Mwanza, TZ"

st.set_page_config(page_title="Unshakable Energy", page_icon="☀️", layout="wide")
st.title("☀️ UNSHAKABLE ENERGY - AI SOLAR PREDICTION")

def get_weather():
  url=f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=metric&lang=sw"
  
  with st.spinner('Inapakia data ya hali ya hewa... ⛅ Tafadhali subiri 10sec'):
    response = requests.get(url)
  
  if response.status_code == 200:
    return response.json()
  else:
    st.error(f"API Error: {response.status_code}")
    return None
data = get_weather()

if data:
  st.subheader(f"⛅ Hali ya Hewa Mwanza - saa 24 zijazo")
  
  for item in data['list'][:8]: # saa 8 = Masaa 24
    time = datetime.fromtimestamp(item['dt']).strftime('%d/%m %H:%M')
    temp = item['main']['temp']
    cloud = item['clouds']['all'] # % ya mawingu ndio muhimu kwa jua
    weather = item['weather'][0]['description']

    col1,col2,col3 = st.columns(3)
    col1.write(f"**{time}**")
    col2.write(f"{weather} | {temp}°C")
    col3.write(f"Mawingu: {cloud}%")

    if cloud < 20:
      st.success("☀️ PREDICTION: Power JUU SANA - Weka Solar yako max ")
    elif cloud < 60:
      st.warning("⛅ PREDICTIO: Power ya KATI - Tumia kwa Akili")
    else:
      st.error("☁️ PREDICTION: Power CHINI - Chaji power Bank")
    st.divider()
