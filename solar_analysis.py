import pandas as pd
import matplotlib.pyplot as plt

# DATA YETU YA SIKU 7
data_siku7={ 
          'siku':['Jumatatu', 'Jumanne', 'Juamatano', 'Alhamisi', 'Ijumaa', 'Jumapili'],
          Hali_ya_Hewa:[80.1, 79.3, 65.0, 45.2, 81.0, 78.8, 63.5]
 }
 df_7=pd.DataFrame(data)
 
# Hesabu % Loss
avg_jua=df[df['Hali_ya_Hewa']=='jua']['Power_W'].mean()
avg_mvua=df[df['Hali_ya_Hewa']=='mvua']['Power_w'].mean()
loss_percent=((avg_jua-avg_mvua)/avg_jua)*100
 
print(f"Average Power Jua:{avg_jua:.2f}w")
print(f"Average Power Mvua:{avg_mvua:.2f}w")
print(f"Efficiency Loss:{loss_percent:.2f}")

#Graph
color={'Jua':'gold', 'Mawingu':'gray', 'Mvua':'blue'}
plt.figure(figsize=(10,5))
plt.bar(df['siku'], df['Power_W'], color=df['Hali_ya_Hewa'].map(solars))
plt.title(' 7 Day Solar Trend - Mwanza,TZ')
plt.ylabel('Power (w)')
plt.grid(axis='y', alpha=0.3)
plt.savefig(' 7day_solar_trend_a.png', dpi=300)
plt.show()     

 print("\nGraph imepata rangi! Angalia bluu ndio chini kabisa")                                                 