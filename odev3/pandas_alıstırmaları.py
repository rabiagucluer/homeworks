##############################
#Pandas Alıştırmalar
##############################
import pandas as pd

#Görev 1:Seaborn kütüphanesi içerisinden Titanic veri setini tanımlayınız
import seaborn as sns
df = sns.load_dataset("titanic")

# Görev 2:  Titanic veri setindeki kadın ve erkek yolcuların sayısını bulunuz
df["sex"].value_counts()

#Görev 3:  Her bir sütuna ait unique değerlerin sayısını bulunuz.
df.columns.nunique()

#Görev 4:  pclass değişkeninin unique değerlerinin sayısını bulunuz.
df["pclass"].nunique()

#Görev5:  pclass ve parch değişkeninin unique değerlerinin sayısını bulunuz.
df[["pclass","parch"]].nunique() #çift köşeli parantez df anlamına gelir

#pandas.core.series.Series(df['pclass'].unique()).value_counts() --->bu kodun mantığı var mı yok mu tekrar bak?

#Görev 6:   embarked değişkeninin tipini kontrol ediniz. Tipini category olarak değiştiriniz ve tekrar kontrol ediniz.
#type(df["embarked"]) --->bununla df nin farkını öğren
df["embarked"].dtypes
df["embarked"].astype("category")

#Görev 7:   embarked değeri C olanların tüm bilgelerini gösteriniz.
df[df["embarked"]=="C"].head()

#Görev 8:   embarked değeri S olmayanların tüm bilgelerini gösteriniz.
df[df["embarked"]!="S"].head()

#Görev 9:   Yaşı 30 dan küçük ve kadın olan yolcuların tüm bilgilerini gösteriniz.
df.loc[(df["age"] < 30) & (df["sex"]=="female")].head()

#Görev 10:  Fare 'i500' den büyük veya yaşı 70 den büyük yolcuların bilgilerini gösteriniz.
df.loc[(df["fare"] > 500) | (df["age"] > 70)].head()

#Görev 11:  Her bir değişkendeki boş değerlerin toplamını bulunuz.
df.isnull().sum()

#Görev 12:  who değişkenini dataframe’den çıkarınız.
df.columns.drop("who")

#Görev 13:  deck değikenindeki boş değerlerideck değişkenin en çok tekrar eden değeri(mode) ile doldurunuz.
df["deck"]=["deck"].fillna(df["deck"].mode()[0])

#Görev 14:  age değikenindeki boş değerleri age değişkenin medyanı ile doldurunuz.
df["age"]=df["age"].fillna(df["age"].median())

#Görev 15:  survived değişkeninin pclass ve cinsiyet değişkenleri  kırılımınında sum, count, mean değerlerini bulunuz.
df.groupby(["pclass","sex"]).agg({"survived": ["sum", "count", "mean"]})

#Görev 16:  30 yaşın altında olanlar 1, 30'a eşit ve üstünde olanlara 0 vericek bir fonksiyon yazın.
#Yazdığınız fonksiyonu kullanarak titanik veri setinde age_flag adında bir değişken  oluşturunuz. (apply ve lambda yapılarını kullanınız)'
#df["age_flag"] = df["age"].apply(lambda x: 1 if x < 30 else 0)

def age_30(age):
    if age < 30:
        return 1
    else:
        return 0

df["age_flag"]=df["age"].apply(lambda x:age_30(x))

#Görev 17:  Seaborn kütüphanesi içerisinden Tips veri setini tanımlayınız.
df = sns.load_dataset("tips")
df.head()

#Görev 18:  Time değişkeninin kategorilerine (Dinner, Lunch) göre total_bill değerlerinin toplamını, min, max ve ortalamasını bulunuz.
df.groupby(["time"]).agg({"total_bill": ["sum","min","max","mean"]})

#Görev 19:  Günlere ve time göre total_bill değerlerinin toplamını, min, max ve ortalamasını bulunuz.
df.groupby(["day","time"]).agg({"total_bill": ["sum","min","max","mean"]})

#Görev 20:  Lunch zamanına ve kadın müşterilere ait total_bill ve tip  değerlerinin day'e göre toplamını, min, max ve ortalamasını bulunuz.
df.loc[(df["time"] == "Lunch") & (df["sex"] == "Female")].groupby(["day"]).agg({"total_bill": ["sum","min","max","mean"],
                                                                                "tip":["sum","min","max"]})
#df[(df["time"] == "Lunch") & (df["sex"] == "Female")].groupby(["day"]).agg({"total_bill": ["sum","min","max","mean"],
#                                                                                "tip":["sum","min","max"]})

#Görev 21:  size'i 3'ten küçük, total_bill'i 10'dan büyük olan siparişlerin ortalaması nedir? (loc kullanınız)
df.loc[(df["size"]<3) & (df["total_bill"]>10), "total_bill"].mean()

#Görev 22:  total_bill_tip_sum adında yeni bir değişken oluşturunuz. Her bir müşterinin ödediği total bill ve tip in toplamını versin.
df["total_bill_tip_sum"] = df["total_bill"]+df["tip"]

#Görev 23:  total_bill_tip_sum değişkenine göre büyükten küçüğe sıralayınız ve ilk 30 kişiyi yeni bir dataframe'e atayınız.
df_new = df.sort_values(by='total_bill_tip_sum', ascending=False)[:30]
df_new.head()


df.set_index("day", inplace=True)