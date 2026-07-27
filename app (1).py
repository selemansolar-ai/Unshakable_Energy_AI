import requests
import streamlit as st
import pandas as pd
from datetime import datetime
import time
import sqlite3
import folium
from streamlit_folium import st_folium

API_KEY = st.secrets["API_KEY"]
CITY = "Mwanza, TZ"
LAT, LON = -2.5164, 32.9166

st.set_page_config(page_title="Unshakable Energy", page_icon="☀️", layout="wide")
st.title("☀️ UNSHAKABLE ENERGY - AI SOLAR PREDICTION")

conn = sqlite3.connect('solar_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS history(time TEXT, temp REAl, cloud INTEGER, prediction TEXT)''')

def save_data(time, temp, cloud, pred):
  c.execute("INSERT INTO history VALUES(?, ?, ?, ?)",(time, temp, cloud, pred))
  conn.commit()
  
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
  times, temps, clouds, preds = [], [], [], []
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
      pred = "Power JUU - Jua kali"
      st.success(f"☀️ PREDICTION: {pred}")
    elif cloud < 60:
      pred = "Power ya KATI - Mawingu kidogo"
      st.warning("⛅ PREDICTIO: {pred}")
    else:
      pred = "Power CHINI - Mawingu mengi"
      st.error("☁️ PREDICTION: {pred}")

    times.append(time)
    temps.append(temp)
    clouds.append(cloud)
    preds.append(pred)


    save_data(time, temp, cloud, pred)
    st.divider()

  st.subheader("📊 Chati ya joto vs Mawingu")
  df = pd.DataFrame({'saa': times, 'Joto c': temps, 'mawingu %': clouds})
  st.line_chart(df.set_index('saa'))

  st.subheader("🗺️ Ramani ya Mwanza")
  m = folium.Map(location=[LAT, LON], zoom_start=10)
  folium.Marker([LAT, LON], popup = "Mwanza - Solar Prediction Hub").add_to(m)
  st_folium(m, width=700, height=400)

if st.button("Ona Historia ya Data"):
  df_hist = pd.read_sql_query("SELECT * FROM history ORDER BY time DESC LIMIT 20", conn)
  st.dataframe(df_hist)

conn.close()
