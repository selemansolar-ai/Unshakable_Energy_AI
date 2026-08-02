import requests
import streamlit as st
import pandas as pd
from datetime import datetime
import os
import time
import sqlite3
import folium
import africastalking
import json
from streamlit_folium import st_folium
from africastalking import SMS

st.set_page_config(page_title="JUMEME_API", layout="wide")
query_params = st,query_params
if "predict" in st.query_params:
 data = {
  "city": "Mwanza",
  "prediction": "Power. SIFURI - Ni Usiku",
  "power_percent":0,
  "alert": "Mvua inakuja"
 }
 st.write(json.dump(data)) 
 st.stop()
 
st.write("API yako ipo:", "NDIO" if st.secrets.get("AT_API_KEY") else "HAPANA")

def send_sms_africastalking(message):
 try:
    username = st.secrets["AT_USERNAME"]
    api_key = st.secrets["AT_API_KEY"]
    phone = st.secrets["ALERT_PHONE"]
    shortcode = "84882"
     
    africastalking.initialize(username, api_key)
    sms = africastalking.SMS
  
    response = sms.send(message, [phone], shortcode)

    recipient = response['SMSMessageData']['Recipients'][0]
    if recipient['status'] == 'Success':
     st.success(f"✅ SMS Imetumwa kutoka {shortcode} kwenda  kwa {phone}")
    else:
     st.error(f"SMS Imeshindikana: {response}")
     
 except Exception as e:
    st.error(f"📢 SMS Error: {e}")
   
if 'shown_times' not in st.session_state:
  st.session_state.shown_times = []
  
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
CITY = "Mwanza, TZ"
LAT, LON = -2.5164, 32.9166

st.set_page_config(page_title="Unshakable Energy", page_icon="☀️", layout="wide")
st.title("☀️ UNSHAKABLE ENERGY - AI SOLAR PREDICTION")
st.subheader("📊 LIVE MONITORING - MWANZA")
col1, col2, col3 = st.columns(3)
col1.metric("Power Sasa", "86%", "JUU")
col2.metric("Joto", "23°C", "")
col3.metric("Upepo", "3.5m/s", "")

conn = sqlite3.connect('solar_data.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS history(time TEXT UNIQUE, temp REAl, cloud INTEGER, prediction TEXT)''')

def save_data(time, temp, cloud, pred):
  conn = sqlite3.connect('solar_data.db')
  c = conn.cursor()
  c.execute("INSERT OR IGNORE INTO history VALUES(?, ?, ?, ?)",(time, temp, cloud, pred))
  conn.commit()
  conn.close()
  
def get_weather():
  url=f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={WEATHER_API_KEY}&units=metric&lang=sw"
  
  with st.spinner('Inapakia data ya hali ya hewa... ⛅ Tafadhali subiri 10sec'):
    response = requests.get(url)
  
  if response.status_code == 200:
    return response.json()
  else:
    st.error(f"API Error: {response.status_code}")
    return None
data = get_weather()
def send_alert(message):
  st.warning(f"📢 ALERT: {message}")
  send_sms_africastalking(message)
  
if data and 'list' in data:
  times, temps, clouds, preds = [], [], [], []
  st.subheader(f"⛅ Hali ya Hewa Mwanza - saa 24 zijazo")

  for item in data['list'][:12]: # saa 8 = Masaa 24
    dt_obj = datetime.fromtimestamp(item['dt'])
    time_str = dt_obj.strftime("%Y-%m-%d %H:%M")
    temp = item['main']['temp']
    cloud = item['clouds']['all'] # % ya mawingu ndio muhimu kwa jua
    wind = item['wind']['speed'] # m/s
    weather = item['weather'][0]['description']
    rain_chance = 0
    if 'rain' in weather.lower() or cloud > 80:
      rain_chance = 80
    elif cloud > 60:
      rain_chance = 50
    if rain_chance > 70:
      alert_message = f"TEST: Power CHINI leo saa {time.strftime('%H:%M')}.Funngua diesel!"
      send_alert(alert_message)
      
    col1,col2,col3,col4 = st.columns(4)
    col1.write(f"**{time_str}**")
    col2.write(f"{weather} | {temp}°C")
    col3.write(f"Mawingu: {cloud}%")
    col4.write(f"💨 Upepo: {wind}m/s")
    hour = dt_obj.hour
    is_day = 6<= hour<18
           
    if is_day:
      if 10 <= hour <= 15:
        power = 115 - cloud
        if power > 100: power = 100
      else:
         power = 100 - cloud
      if wind > 5:
        power = power + 5 # Upepo unapooza paneli
        if power > 100: power = 100
        note = " + Upepo mzuri"
      else:
        note = ""
      if power > 75:
        pred = f"Power JUU - {power}%  - Jua kali"
        st.success(f"☀️ PREDICTION: {pred}")
      elif power > 45:
        pred = f"Power ya KATI - {power}% - Mawingu kidogo"
        st.warning(f"⛅ PREDICTION: {pred}")
      else:
        pred = f"Power CHINI {power}%- Mawingu mengi"
        st.error(f"☁️ PREDICTION: {pred}")
    else:
      power = 0 #usiku hakuna jua
      pred = "Power SIFURI - Ni Usiku"
      st.info(f"🌙 PREDICTION: {pred}")
   
    if power > 85:
      st.balloons()
      st.toast(f"🔔 ALERT: Charge batteries! power itakuwa {power}% saa {hour}: 00") 
    if power < 20:
      st.error("⚠️ ALERT: Low Solar Power Generation Expected at this time")
     
    times.append(time)
    temps.append(temp)
    clouds.append(cloud)
    preds.append(pred)

  if time_str not in st.session_state.shown_times:
    save_data(time_str, temp, cloud, pred)
    st.session_state.shown_times.append(time_str)
    st.divider()
    if st.button("🧪 Jaribu kutuma SMS sasa", key="test_sms_btn"):
     send_sms_africastalking("TEST: Mfumo wa Unishakable Energy unafanya kazi vizuri")
     
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
st.sidebar.markdown("---")
st.sidebar.subheader("API kwa JUMEME")
if st.sidebar.button("Pata Utabiri wa leo"):
 latest_pred = preds[-1] if preds else "Hakuna data"
 latest_power = power
 st.sidebar.json({
  "city": "Mwanza",
  "prediction": latest_pred,
  "power_percent": latest_power,
  "alert": "Mvua inakuja" if rain_chance > 70 else "Sawa"
 })
 
