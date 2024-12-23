'''
Özellikleri belirtildiğinde kişilerin diyabet hastası olup olmadıklarını tahmin
edebilecek bir makine öğrenmesi modeli geliştirilmesi istenmektedir. Modeli
geliştirmeden önce gerekli olan veri analizi ve özellik mühendisliği adımlarını
gerçekleştirmeniz beklenmektedir.
'''

from IPython.core.pylabtools import figsize

'''
Veri seti ABD'deki Ulusal Diyabet-Sindirim-Böbrek Hastalıkları Enstitüleri'nde tutulan büyük veri setinin parçasıdır. ABD'deki
Arizona Eyaleti'nin en büyük 5. şehri olan Phoenix şehrinde yaşayan 21 yaş ve üzerinde olan Pima Indian kadınları üzerinde
yapılan diyabet araştırması için kullanılan verilerdir.
Hedef değişken "outcome" olarak belirtilmiş olup; 1 diyabet test sonucunun pozitif oluşunu, 0 ise negatif oluşunu belirtmektedir.
'''

################################
# GÖREV 1 : KESIFCI VERI ANALIZI
################################

# 1: Genel resmi inceleyiniz.

import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

import missingno as msno
from datetime import date
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import LocalOutlierFactor
from sklearn.preprocessing import MinMaxScaler, LabelEncoder, StandardScaler, RobustScaler


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.float_format', lambda x: '%.3f' %x )
pd.set_option('display.width', 500)

def load_diabetes():
    data=pd.read_csv('datasets/diabetes-230423-212053.csv')
    return data

df=load_diabetes()
df.head()

def check_dataframe(dataframe , head=5):
    print("----------- Shape ---------------")
    print(dataframe.shape)
    print("----------- Types ---------------")
    print(dataframe.dtypes)
    print("----------- Head ----------------")
    print(dataframe.head(head))
    print("----------- Tail ----------------")
    print(dataframe.tail(head))
    print("----------- NA ------------------")
    print(dataframe.isnull().sum())
    print("----------- Quantiles -----------")
    print(dataframe.quantile([0,0.05,0.50, 0.95, 0.99, 1]).T)

check_dataframe(df,head=5)

# 2: Numerik ve kategorik degiskenleri yakalayiniz.

df=load_diabetes()
df.head()

def outlier_thresholds(dataframe, col_name, q1=0.25, q3=0.75):
    quartile1 = dataframe[col_name].quantile(q1)
    quartile3 = dataframe[col_name].quantile(q3)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit

outlier_thresholds(df, "Age")
outlier_thresholds(df, "Glucose")

low, up = outlier_thresholds(df, "Outcome")


def check_outlier(dataframe, col_name):
    low_limit, up_limit = outlier_thresholds(dataframe, col_name)
    if dataframe[(dataframe[col_name] > up_limit) | (dataframe[col_name] < low_limit)].any(axis=None):
        return True
    else:
        return False



def grab_col_names(dataframe, cat_th=10, car_th=20):
    """

    Veri setindeki kategorik, numerik ve kategorik fakat kardinal değişkenlerin isimlerini verir.
    Not: Kategorik değişkenlerin içerisine numerik görünümlü kategorik değişkenler de dahildir.

    Parameters
    ------
        dataframe: dataframe
                Değişken isimleri alınmak istenilen dataframe
        cat_th: int, optional
                numerik fakat kategorik olan değişkenler için sınıf eşik değeri
        car_th: int, optinal
                kategorik fakat kardinal değişkenler için sınıf eşik değeri

    Returns
    ------
        cat_cols: list
                Kategorik değişken listesi
        num_cols: list
                Numerik değişken listesi
        cat_but_car: list
                Kategorik görünümlü kardinal değişken listesi

    Examples
    ------
        import seaborn as sns
        df = sns.load_dataset("iris")
        print(grab_col_names(df))


    Notes
    ------
        cat_cols + num_cols + cat_but_car = toplam değişken sayısı
        num_but_cat cat_cols'un içerisinde.
        Return olan 3 liste toplamı toplam değişken sayısına eşittir: cat_cols + num_cols + cat_but_car = değişken sayısı

    """

    #cat_cols, cat_but_car

    '''
    Kategorik sütunlar, veri tipine göre ve eşik değerlere bakılarak belirlenir:

    cat_cols: String türünde (dtype == "O") olan sütunlar doğrudan kategorik sütunlar listesine eklenir.
    num_but_cat: Nümerik görünümlü ama benzersiz sınıf sayısı (nunique) eşik değerinden küçük olan sütunlar da kategorik sütunlar listesine eklenir.
    cat_but_car: Benzersiz sınıf sayısı (nunique) eşik değerinden büyük (car_th) olan kategorik sütunlar, kategorik ama kardinal sütunlar listesine alınır.
    cat_but_car sütunları, cat_cols listesinden çıkarılır.

    Nümerik sütunlar, dtype != "O" (string olmayan) olan sütunlardan oluşur. Ayrıca:

    Eğer bu sütunlar num_but_cat içinde yer alıyorsa, nümerik sütunlar listesinden çıkarılır
    '''

    cat_cols = [col for col in dataframe.columns if dataframe[col].dtypes == "O"]
    num_but_cat = [col for col in dataframe.columns if dataframe[col].nunique() < cat_th and
                   dataframe[col].dtypes != "O"]
    cat_but_car = [col for col in dataframe.columns if dataframe[col].nunique() > car_th and
                   dataframe[col].dtypes == "O"]
    cat_cols = cat_cols + num_but_cat
    cat_cols = [col for col in cat_cols if col not in cat_but_car]

    # num_cols
    num_cols = [col for col in dataframe.columns if dataframe[col].dtypes != "O"]
    num_cols = [col for col in num_cols if col not in num_but_cat]

    print(f"Observations: {dataframe.shape[0]}")
    print(f"Variables: {dataframe.shape[1]}")
    print(f'cat_cols: {len(cat_cols)}')
    print(f'num_cols: {len(num_cols)}')
    print(f'cat_but_car: {len(cat_but_car)}')
    print(f'num_but_cat: {len(num_but_cat)}')
    return cat_cols, num_cols, cat_but_car

cat_cols, num_cols, cat_but_car = grab_col_names(df)


for col in num_cols:
    print(col, check_outlier(df, col))


cat_cols, num_cols, cat_but_car = grab_col_names(df)

num_cols = [col for col in num_cols if col not in "SK_ID_CURR"]

for col in num_cols:
    print(col, check_outlier(df, col))

# 3: Adım 3: Numerik ve kategorik değişkenlerin analizini yapınız.

# Numerik degisken analizi

def num_summary(dataframe, num_cols, plot = False):
    for col_name in num_cols:
        # Temel istatistiksel özet
        print(f"Column: {col_name}")
        print(dataframe[col_name].describe( ))
        print("----------------------------------------------------------------------")

        # Grafikleri çiz
        if plot:
            dataframe[num_cols].hist(bin=20)
            # Kutu grafiği
            plt.xlabel(num_cols)
            plt.title(f"Graph of {col_name}")
            plt.show(block=True)

# Örnek kullanım
for col in num_cols:
    num_summary(df, num_cols)


# Kategorik degisken analizi

def cat_summary(dataframe, cat_cols, plot = True):
    for col_name in cat_cols:

        # Kategorik değişkenin frekans ve oranlarını yazdır
        summary = pd.DataFrame({col_name: dataframe[col_name].value_counts( ),
                                "Ratio": 100 * dataframe[col_name].value_counts( ) / len(dataframe)})
        print(summary)
        print("----------------------------------------------------------------------")

        # Grafiği çiz
        if plot:
            sns.countplot(x = dataframe[col_name])
            plt.title(f"Distribution of {col_name}")
            plt.show(block=True)


# Örnek kullanım
for col in num_cols:
    cat_summary(df, cat_cols)


# 4: Hedef değişken analizi yapınız. (Kategorik değişkenlere göre hedef değişkenin ortalaması, hedef değişkene göre
# numerik değişkenlerin ortalaması)

def target_summary_with_num(dataframe, target, num_cols, plot=False):
    print(dataframe.groupby(target).agg({num_cols:"mean"}), end = "\n\n")

    if plot:
        mean_values=dataframe.groupby(target)[num_cols].mean()
        mean_values.plot(kind='bar')
        plt.xlabel(target)
        plt.ylabel(f"Mean of {num_cols}")
        plt.title(f"Mean of {num_cols} for each {target}")
        plt.show(block=True)
for col in num_cols:
    target_summary_with_num(df, "Outcome", col)

# 5: Aykırı gözlem analizi yapınız.


def outlier_thresholds(dataframe, col_name, q1=0.05, q3=0.95):
    quartile1 = dataframe[col_name].quantile(q1)
    quartile3 = dataframe[col_name].quantile(q3)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit

outlier_limits={}
for col in num_cols:
    low_limit, up_limit= outlier_thresholds(df,col)
    outlier_limits[col]={'low_limit': low_limit, 'up_limit': up_limit}

print(outlier_limits)



def check_outlier(dataframe, col_name):
    low_limit, up_limit = outlier_thresholds(dataframe, col_name)
    if dataframe[(dataframe[col_name] > up_limit) | (dataframe[col_name] < low_limit)].any(axis=None):
        return True
    else:
        return False



def replace_with_thresholds(dataframe, variable, q=0.05, q3=0.95):
    low_limit, up_limit = outlier_thresholds(dataframe, variable, q=0.05, q3=0.95)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit


# BASKILAMA
# az bir verimiz oldugundan silme olsaydi analizimiz cokca etkilenirdi. bu nedenle baskilama yaptik.

for col in df.columns:
    print(col, check_outlier(df, col))

for col in df.columns:
    print(col, check_outlier(df, col))
    if check_outlier(df,col):
        replace_with_thresholds(df,col)

for col in df.columns:
    replace_with_thresholds(df, col)


# 6: Eksik gözlem analizi yapınız.

# eksik gozlem var mı yok mu sorgusu
df.isnull().values.any()

# degiskenlerdeki eksik deger sayisi
df.isnull().sum()

# degiskenlerdeki tam deger sayisi
df.notnull().sum()

# veri setindeki toplam eksik deger sayisi
df.isnull().sum().sum()

zero_columns=[col for cool in df.columns if (df[col].min()==0 and col not in ['Pregnancies', 'Outcome'])]

# burda o degerleri NaN ile degistirdik.
zero_columns

for col in zero_columns :
    df[col]=np.where(df[col]==0, np.nan,df[col])


# eksik gözlemleri analiz edelim
df.isnull().sum()

def missing_values_table(dataframe, na_name=False):
    n_columns = [col for col in dataframe.columns if dataframe[col].isnull().sum() > 0]
    n_miss = dataframe[n_columns].isnull().sum().sort_values(ascending=False)
    ratio = (dataframe[n_columns].isnull().sum() / dataframe.shape[0] * 100).sort_values(ascending=False)
    missing_df = pd.concat([n_miss, np.round(ratio, 2)], axis=1, keys=['n_miss', 'ratio'])
    print(missing_df, end="\n")

    if na_name:
        return n_columns

n_columns= missing_values_table(df, na_name=True)

# Eksik değerleri görselleştirme
plt.figure(figsize=(8, 6))
sns.heatmap(df.isnull(), cbar=False, cmap='viridis', yticklabels=False)
plt.title("Eksik Değerlerin Görselleştirilmesi")
plt.show()

# bu eksik degerleri dolduralim.
for col in zero_columns:
    df.loc[df[col].isnull(), col]=df[col].median()

df[col].isnull().sum()

# 7: Korelasyon analizi yapınız.

f,ax=plt.subplots(figsize=[18,13])
sns.heatmap(df.corr(), annot = True, fmt= ".2f", ax=ax, cmap="magma")
ax.set_title("Correlation Matrix", fontsize=20)
plt.show(block=True)


diabetic=df[df.Outcome==1]
healthy=df[df.Outcome==0]

plt.scatter(healthy.Age, healthy.Glucose, color="green", label="Healthy", alpha=0.4)
plt.scatter(diabetic.Age, diabetic.Glucose, color="yellow", label="Diabetic", alpha=0.4)
plt.xlabel("Age")
plt.ylabel("Glucose")
plt.legend()
plt.show(block=True)