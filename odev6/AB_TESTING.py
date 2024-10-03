#####################################################
# AB Testi ile BiddingYöntemlerinin Dönüşümünün Karşılaştırılması
#####################################################

#####################################################
# İş Problemi
#####################################################

# Facebook kısa süre önce mevcut "maximumbidding" adı verilen teklif verme türüne alternatif
# olarak yeni bir teklif türü olan "average bidding"’i tanıttı. Müşterilerimizden biri olan bombabomba.com,
# bu yeni özelliği test etmeye karar verdi veaveragebidding'in maximumbidding'den daha fazla dönüşüm
# getirip getirmediğini anlamak için bir A/B testi yapmak istiyor.A/B testi 1 aydır devam ediyor ve
# bombabomba.com şimdi sizden bu A/B testinin sonuçlarını analiz etmenizi bekliyor.Bombabomba.com için
# nihai başarı ölçütü Purchase'dır. Bu nedenle, istatistiksel testler için Purchasemetriğine odaklanılmalıdır.




#####################################################
# Veri Seti Hikayesi
#####################################################

# Bir firmanın web site bilgilerini içeren bu veri setinde kullanıcıların gördükleri ve tıkladıkları
# reklam sayıları gibi bilgilerin yanı sıra buradan gelen kazanç bilgileri yer almaktadır.Kontrol ve Test
# grubu olmak üzere iki ayrı veri seti vardır. Bu veri setleriab_testing.xlsxexcel’ininayrı sayfalarında yer
# almaktadır. Kontrol grubuna Maximum Bidding, test grubuna AverageBiddinguygulanmıştır.

# impression: Reklam görüntüleme sayısı
# Click: Görüntülenen reklama tıklama sayısı
# Purchase: Tıklanan reklamlar sonrası satın alınan ürün sayısı
# Earning: Satın alınan ürünler sonrası elde edilen kazanç



#####################################################
# Proje Görevleri
#####################################################

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
import scipy.stats as st
from scipy.stats import (ttest_1samp, shapiro, levene, mannwhitneyu, ttest_ind,
                         pearsonr, spearmanr, kendalltau, f_oneway,kruskal)
import statsmodels.api as sm
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################

# 1. Hipotezleri Kur
# 2. Varsayım Kontrolü
#   - 1. Normallik Varsayımı (shapiro)
#   - 2. Varyans Homojenliği (levene)
# 3. Hipotezin Uygulanması
#   - 1. Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi
#   - 2. Varsayımlar sağlanmıyorsa mannwhitneyu testi
# 4. p-value değerine göre sonuçları yorumla
# Not:
# - Normallik sağlanmıyorsa direkt 2 numara. Varyans homojenliği sağlanmıyorsa 1 numaraya arguman girilir.
# - Normallik incelemesi öncesi aykırı değer incelemesi ve düzeltmesi yapmak faydalı olabilir.




#####################################################
# Görev 1:  Veriyi Hazırlama ve Analiz Etme
#####################################################


###### Adım 1:  ab_testing_data.xlsx adlı kontrol ve test grubu verilerinden oluşan veri setini okutunuz. Kontrol ve test grubu verilerini ayrı değişkenlere atayınız. ####

# df = pd.read_excel("C:/Users/User/git/homeworks/odev6/ab_testing.xlsx")
test_df = pd.read_excel("C:/Users/User/git/homeworks/odev6/ab_testing.xlsx", sheet_name='Test Group')

control_df = pd.read_excel("C:/Users/User/git/homeworks/odev6/ab_testing.xlsx", sheet_name='Control Group')



##### Adım 2: Kontrol ve test grubu verilerini analiz ediniz. #####

# control group analysis
control_df.head()
control_df.info()
control_df.describe().T
control_df.nunique()
control_df.isnull().sum()


# Test group analysis
test_df.head()
test_df.info()
test_df.describe().T
test_df.nunique()
test_df.isnull().sum()


##### Adım 3: Analiz işleminden sonra concat metodunu kullanarak kontrol ve test grubu verilerini birleştiriniz. ####

test_df['Group'] = 'Test'
control_df['Group'] = 'Control'

# ignore_index=True ile indekslerin sıfırdan başlamasını sağlar.

combined_df = pd.concat([test_df, control_df], ignore_index = True)

combined_df.head(10)
combined_df.tail(10)


#####################################################
# Görev 2:  A/B Testinin Hipotezinin Tanımlanması
#####################################################

####### Adım 1: Hipotezi tanımlayınız. #####


# H0: M1 == M2 (Test ve Kontrol Gruplarinin purchase Ortalamaları Arasında İstatistiksel Olarak Anl. Fark. Yoktur)
# H1: M1 != M2 (... İstatistiksel Olarak Anl. Farki Vardir)


##### Adım 2: Kontrol ve test grubu için purchase (kazanç) ortalamalarını analiz ediniz #####

combined_df.groupby('Group')['Purchase'].mean()
#combined_df.groupby('Group').agg({"Purchase": "mean"})

#cikti: Group
# Control   550.89406
# Test      582.10610

#####################################################
# GÖREV 3: Hipotez Testinin Gerçekleştirilmesi
#####################################################

######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################


##### Adım 1: Hipotez testi yapılmadan önce varsayım kontrollerini yapınız. Bunlar Normallik Varsayımı ve Varyans Homojenliğidir.####

# 2. Varsayımları İnceleme
# Normallik varsayımı
# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1:..sağlanmamaktadır.

# p-value < ise 0.05 'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ



###### Kontrol ve test grubunun normallik varsayımına uyup uymadığını Purchase değişkeni üzerinden ayrı ayrı test ediniz.####


# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1:..sağlanmamaktadır.

test_stat, pvalue = shapiro(combined_df.loc[combined_df["Group"] == "Control", "Purchase"].dropna())
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

test_stat, pvalue = shapiro(combined_df.loc[combined_df["Group"] == "Test", "Purchase"].dropna())
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Test Stat = 0.9773, p-value = 0.5891 ---> H0 reddedilemez (control)
# Test Stat = 0.9589, p-value = 0.1541 ---> H0 red (test)
# Normallik varsayımının tümüyle sağlanması için her iki grubun da normal dağılıma uygun olması gerekir. Bu nedenle H0 : red
# Normallik varsayimi saglanmadi bu nedenle varyans homojenligine bakmaya gerek bile yoktur.


####### Adım 2: Normallik Varsayımı ve Varyans Homojenliği sonuçlarına göre uygun testi seçiniz.

# Varyans Homojenligi Varsayımı
# H0: Varyanslar Homojendir
# H1: Varyanslar Homojen Değildir

# p-value < ise 0.05 'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.

test_stat, pvalue = levene(combined_df.loc[combined_df["Group"] == "Control", "Purchase"],
                           combined_df.loc[combined_df["Group"] == "Test", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# Test Stat = 2.6393, p-value = 0.1083 ----> H0 REDDEDILEMEZ.
# Varyanslar Homojendir.

## Normallik saglanmayip varsayim homojenligi saglandigi icin non-prametric yani mannwhitneyu testi veya t testi  uygulanmalidir.


####### Adım 3: Test sonucunda elde edilen p_value değerini göz önünde bulundurarak kontrol ve test grubu satın alma
####### ortalamaları arasında istatistiki olarak anlamlı bir fark olup olmadığını yorumlayınız.

test_stat, pvalue = mannwhitneyu(combined_df.loc[combined_df["Group"] == "Control", "Purchase"],
                                 combined_df.loc[combined_df["Group"] == "Test", "Purchase"])

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))


# Test Stat = 723.0000, p-value = 0.4617

# p-value > 0.05 oldugundan H0 reddedilemez. Bu demek oluyor ki purchase ortalamalari arasinda istatiki olarak anlamli bir fark yoktur.

##############################################################
# GÖREV 4 : Sonuçların Analizi
##############################################################

####### Adım 1: Hangi testi kullandınız, sebeplerini belirtiniz.

## Normallik saglanmayip varsayim homojenligi saglandigi icin non-prametric bir test olan mannwhitneyu testini uyguladim.
## Sebebi varsayimlarin saglanmamasidir.


####### Adım 2: Elde ettiğiniz test sonuçlarına göre müşteriye tavsiyede bulununuz.
# --1---
# Test sonucunda anlamlı bir fark bulunmadığından, şu anda uyguladıkları stratejiyi değiştirmek için
# istatistiksel bir gerekçe yoktur. Mevcut kampanya, web tasarımı veya pazarlama stratejisi etkin şekilde devam edebilir.
# Çünkü, yapılan testte yeni uygulanan stratejinin (test grubunun) performansının, mevcut uygulamalardan (kontrol grubundan)
# anlamlı derecede daha iyi olmadığı sonucuna varılmıştır.

# --2--
# Test yapilan grubun degistirilmesi belki de farkli sonuclar elde etmemizi saglayabilir.

# --3--
# Örneklem sayisi arttirilabilir. Farkli test yöntemleri uygulanabilir.
# Bir degiskene odaklanmak yerine iki veya daha fayla degiskene ayni anda odaklanilabilir.
