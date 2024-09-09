# Görev 1: list comp. kullanarak car_crashes verisindeki numeric değişkenlerin isimlerini
# büyük harfe çevir ve başına NUM koy

import seaborn as sns
df= sns. load_dataset("car_crashes")
df.columns


for col in df.columns:
    df.columns=["NUM_"+ col.upper() if df[col].dtype!= "0" else col.upper for col in df.columns]


# Görev 2: list comp. kullarak car_crashes verisinde isminde no barındırmayan değişkenlerin sonuna "FLAG" yaz

[col + "_FLAG"  if "NO" not in col else col for col in df.columns]

# Görev 3: list comp. kullarak aşağıdaki verilerin değişkenlerin isimlerini seç ve yeni bir data frame oluştur

import seaborn as sns
df = sns.load_dataset("car_crashes")
df.columns # mevcut df' in col isimleri

og_list = ["abbrev","no_previous"]

new_cols= [col for col in df.columns if col not in og_list] # og_list' ten farklı olan  df'in col isimleri
new_df= df[new_cols] # yeni df
new_df.head()

