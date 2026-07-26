import streamlit as st
import pandas as pd
import numpy as np
import pickle
import datetime
import os

# 1.TITLE + DESIGN YA UNSHAKABLE
st.set_page_config(page_title="UNSHAKABLE ENERGY AI", layout="wide")

st.markdown("""
<style>
      .main {background-color: #0E1117;}
      h1 {color: #00FF88;}
      .stButton>button {background-color: #00FF88; black; font-weight: bold}
</style>
""", unsafe_allow_html=True)

st.title("UNSHAKABLE ENERGY AI - MWANZA")
st.write("**AI inayotabiri Power ya Solar kwa usahihi wa 98%**")

model=pickle.load(open('model.pkl','rb'))

# 2.INPUTS ZA MTEJA
st.header("Ingiza Hali ya Hewa ya leo")
col1,col2 = st.columns(2)

with col1:
  saa=st.slider("Saa ya siku", 6,18,12)
  joto=st.number_input("Joto °C",0.0,50.0,30.0)
with col2:
  mwangaza=st.number_input("Mwanga wa jua (W/m2)",0,1200,600)
  mawingu=st.number_input("Asilimia ya Mawingu %",0,100,20)

# 3.KITUFE CHA TABIRI + HIFADHI
if st.button("TABIRI POWER SASA"):
  input_data=pd.DataFrame([[saa, joto, mwangaza, mawingu]],
                          columns=['saa', 'joto_c', 'mwangaza', 'mawingu_%'])
  prediction=model.predict(input_data)
  power=prediction[0]

  st.success(f"🔋 POWER INAYOTABIRIWA: {power:.2f} Watts")

  if power > 70:
    st.info("☀️ Muda mzuri wa kuchaji na kutumia machine kubwa")
  else:
    st.warning("⚠️ Punguza matumizi. Jua ni dogo sasa")
                                                             
  # HIFADHI MATOKEO
  new_row=pd.DataFrame([{'Tarehe':datetime.datetime.now(), 'saa':saa,'Power_W':round(power,2)}])
  if os.path.exists('historia.csv'):
     new_row.to_csv('historia.csv',mode='a',header=False,index=False)
  else:
     new_row.to_csv('historia.csv',mode='w', header=True, index=True)  
  st.write("✅ matokeo yamehifadhiwa")

# 4.GRAFU YA MASAA 24
st.header("Grafu ya Tabiri ya masaa 24")
if st.button("ONYESHA GRAFU YA LEO ✅"):
  hours=list(range(6,19))
  # Tunatabiri kwa mwangaza unapanda na kushuka kwa jua
  mwangaza_sim=[max(0,1000*np.sin((h-6)/12*np.pi)) for h in hours]
  

  predictions=[]
  for i, h in enumerate(hours):
    data=pd.DataFrame([[h, joto, mwangaza_sim[i], mawingu]],
                      columns=['saa', 'joto_c', 'mwangaza', 'mawingu_%'])
    pred=model.predict(data)[0]
    predictions.append(model.predict(data)[0])

  df_grafu=pd.DataFrame({'saa':hours,'Power_Tabiri_W':predictions})
  st.line_chart(df_grafu,x='saa',y='Power_Tabiri_W')
  st.write("Grafu hii inaonyesha jinsi Power itakavyokuwa siku nzima")
