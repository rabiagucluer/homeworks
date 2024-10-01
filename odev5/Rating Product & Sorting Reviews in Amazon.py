

###################################################
# PROJE: Rating Product & Sorting Reviews in Amazon
###################################################

###################################################
# İş Problemi
###################################################

# E-ticaretteki en önemli problemlerden bir tanesi ürünlere satış sonrası verilen puanların doğru şekilde hesaplanmasıdır.
# Bu problemin çözümü e-ticaret sitesi için daha fazla müşteri memnuniyeti sağlamak, satıcılar için ürünün öne çıkması ve satın
# alanlar için sorunsuz bir alışveriş deneyimi demektir. Bir diğer problem ise ürünlere verilen yorumların doğru bir şekilde sıralanması
# olarak karşımıza çıkmaktadır. Yanıltıcı yorumların öne çıkması ürünün satışını doğrudan etkileyeceğinden dolayı hem maddi kayıp
# hem de müşteri kaybına neden olacaktır. Bu 2 temel problemin çözümünde e-ticaret sitesi ve satıcılar satışlarını arttırırken müşteriler
# ise satın alma yolculuğunu sorunsuz olarak tamamlayacaktır.

###################################################
# Veri Seti Hikayesi
###################################################

# Amazon ürün verilerini içeren bu veri seti ürün kategorileri ile çeşitli metadataları içermektedir.
# Elektronik kategorisindeki en fazla yorum alan ürünün kullanıcı puanları ve yorumları vardır.

# Değişkenler:
# reviewerID: Kullanıcı ID’si
# asin: Ürün ID’si
# reviewerName: Kullanıcı Adı
# helpful: Faydalı değerlendirme derecesi
# reviewText: Değerlendirme
# overall: Ürün rating’i
# summary: Değerlendirme özeti
# unixReviewTime: Değerlendirme zamanı
# reviewTime: Değerlendirme zamanı Raw
# day_diff: Değerlendirmeden itibaren geçen gün sayısı
# helpful_yes: Değerlendirmenin faydalı bulunma sayısı
# total_vote: Değerlendirmeye verilen oy sayısı



###################################################
# GÖREV 1: Average Rating'i Güncel Yorumlara Göre Hesaplayınız ve Var Olan Average Rating ile Kıyaslayınız.
###################################################

# Paylaşılan veri setinde kullanıcılar bir ürüne puanlar vermiş ve yorumlar yapmıştır.
# Bu görevde amacımız verilen puanları tarihe göre ağırlıklandırarak değerlendirmek.
# İlk ortalama puan ile elde edilecek tarihe göre ağırlıklı puanın karşılaştırılması gerekmektedir.



###################################################
# Adım 1: Veri Setini Okutunuz ve Ürünün Ortalama Puanını Hesaplayınız.
###################################################

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
import scipy.stats as st
from networkx import dfs_successors
from streamlit import dataframe

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.5f' % x)


df=pd.read_csv("amazon_review.csv")
df.head()
df.info()
df.describe()
df.isnull().sum()
df.nunique()

#df['overall'].mean()
df['helpful'].nunique()

var= df[df['total_vote']>500]
df.sort_values("overall", ascending=False).head(20)

df["overall"].mean()
df.head()

###################################################
# Adım 2: Tarihe Göre Ağırlıklı Puan Ortalamasını Hesaplayınız.
# Adim 3: Ağırlıklandirilmis puanlamada her bir yaman
###################################################

df.info()
df['reviewTime'] = pd.to_datetime(df['reviewTime'], dayfirst=True)
df.head()

df['day_diff'].max()
df['day_diff'].min()

df[df["day_diff"] <= 30].count()
df.loc[df["day_diff"] <= 30, "overall"].mean()
df.loc[(df["day_diff"] > 30) & (df["day_diff"] <= 90), "overall"].mean()
df.loc[(df["day_diff"] > 90) & (df["day_diff"] <= 180), "overall"].mean()
df.loc[(df["day_diff"] > 180), "overall"].mean()

# daha hassas bir ölcüm yapmak istersek, agirlikli ortalama hesaplama yapabiliriz
# ortalamaya göre hareket ettigimizden agirlik degerlerimiz birbirine yakin oluyor.
# yani ortalama degerden cok sapmak istemiyoruz.

df.loc[df["day_diff"] <= 30, "overall"].mean() * 28/100 + \
    df.loc[(df["day_diff"] > 30) & (df["day_diff"] <= 90), "overall"].mean() * 26/100 + \
    df.loc[(df["day_diff"] > 90) & (df["day_diff"] <= 180), "overall"].mean() * 24/100 + \
    df.loc[(df["day_diff"] > 180), "overall"].mean() * 22/100

# ortalamaya yakin olani tek tek deneyip bulmaktansa fonksiyon yazip onun bulmasini saglariz

def time_based_weighted_average(dataframe, w1=28, w2=26, w3=24, w4=22):
    return dataframe.loc[df["days"] <= 30, "Rating"].mean() * w1 / 100 + \
           dataframe.loc[(dataframe["days"] > 30) & (dataframe["days"] <= 90), "Rating"].mean() * w2 / 100 + \
           dataframe.loc[(dataframe["days"] > 90) & (dataframe["days"] <= 180), "Rating"].mean() * w3 / 100 + \
           dataframe.loc[(dataframe["days"] > 180), "Rating"].mean() * w4 / 100

time_based_weighted_average(df)

time_based_weighted_average (df, w1 = 38, w2 = 26, w3 = 24, w4 = 22)

########

df.loc[df["day_diff"] <= df["day_diff"].quantile(0.25), "overall"].mean()
df.loc[(df["day_diff"] > df["day_diff"].quantile(0.25)) & (df["day_diff"] <= df["day_diff"].quantile(0.5)), "overall"].mean()
df.loc[(df["day_diff"] > df["day_diff"].quantile(0.5)) & (df["day_diff"] <= df["day_diff"].quantile(0.75)), "overall"].mean()
df.loc[(df["day_diff"] > df["day_diff"].quantile(0.75)), "overall"].mean()

df.loc[df["day_diff"] <= df["day_diff"].quantile(0.25), "overall"].mean() * 28/100 +\
    df.loc[(df["day_diff"] > df["day_diff"].quantile(0.25)) & (df["day_diff"] <= df["day_diff"].quantile(0.5)), "overall"].mean() * 26/100 +\
    df.loc[(df["day_diff"] > df["day_diff"].quantile(0.5)) & (df["day_diff"] <= df["day_diff"].quantile(0.75)), "overall"].mean() * 24/100 +\
    df.loc[(df["day_diff"] > df["day_diff"].quantile(0.75)), "overall"].mean() * 22/100

# üstteki islmeleri bir fonk. a cevirdik

def time_based_weighted_average(dataframe, w1=28, w2=26, w3=24, w4=22):
    return dataframe.loc[df["day_diff"] <= df["day_diff"].quantile(0.25), "overall"].mean() * w1 / 100 + \
        dataframe.loc[(dataframe["day_diff"] > df["day_diff"].quantile(0.25)) & (dataframe["day_diff"] <= df["day_diff"].quantile(0.5)), "overall"].mean() * w2 / 100 + \
        dataframe.loc[(dataframe["day_diff"] > df["day_diff"].quantile(0.5)) & (dataframe["day_diff"] <= df["day_diff"].quantile(0.75)), "overall"].mean() * w3 / 100 +\
        dataframe.loc[(df["day_diff"] > df["day_diff"].quantile(0.75)), "overall"].mean() * w4 / 100


# fonks. cagirarak df ye yeniden göz atiyoruz.

time_based_weighted_average(df, w1 = 38, w2 = 26, w3 = 24, w4 = 22)

df["overall"].mean()

df.head()


###################################################
# Görev 2: Ürün için Ürün Detay Sayfasında Görüntülenecek 20 Review'i Belirleyiniz.
###################################################


###################################################
# Adım 1. helpful_no Değişkenini Üretiniz
###################################################
df.head()
df.tail()

df['helpful_no']=df['total_vote']-df['helpful_yes']
df.head()
df.tail()

df=df[['reviewerName','summary','overall','helpful_no', 'helpful_yes', 'total_vote', 'reviewTime']]
df.head()


# Not:
# total_vote bir yoruma verilen toplam up-down sayısıdır.
# up, helpful demektir.
# veri setinde helpful_no değişkeni yoktur, var olan değişkenler üzerinden üretilmesi gerekmektedir.


###################################################
# Adım 2. score_pos_neg_diff, score_average_rating ve wilson_lower_bound Skorlarını Hesaplayıp Veriye Ekleyiniz
###################################################

def wilson_lower_bound(up,down,confidence=0.95):
    '''
    Wilson lower bound skoru hesaplama pozitif ve negatifleri de dahil eder.

    '''
    n = up + down
    if n == 0:
        return 0
    z = st.norm.ppf(1 - (1 - confidence) / 2)
    phat = 1.0 * up / n
    return (phat + z * z / (2 * n) - z * math.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n)) / (1 + z * z / n)

def score_up_down_diff(up,down):
    return up-down

def score_average_rating(up,down):
    if up + down == 0:
        return 0
    else:
        return up/(up+down)



# 'score_pos_neg_diff' df'i ekleme

df.head(20)
df['score_pos_neg_diff']=df.apply(lambda x: score_up_down_diff(x['helpful_yes'],x['helpful_no']), axis=1)
df.sort_values('score_pos_neg_diff', ascending = False).head(20)

# 'score_average_rating' df'e ekle
df['score_average_rating']=df.apply(lambda x: score_average_rating(x['helpful_yes'],x['helpful_no']), axis=1)
df.sort_values('sorting_average_rating', ascending=False).head(20)

# 'wilson_lower_bound' df'e ekleme
df['wilson_lower_bound']=df.apply(lambda x: wilson_lower_bound(x['helpful_yes'],x['helpful_no']), axis=1)
df.sort_values('wilson_lower_bound', ascending=False).head(20)

##################################################
# Adım 3. 20 Yorumu Belirleyiniz ve Sonuçları Yorumlayınız.
###################################################

df.sort_values('wilson_lower_bound', ascending=False).head(20)
