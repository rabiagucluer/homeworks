x = 8
y = 3.2
z = 8j+18
a = "Hello world"
b = True
c = 23<22
l = [1,2,3,4]
d = {
    "Name": "Jake",
    "Age": 27,
    "Adress": "Downtown"
}
t = ("Machine Learning", "Data Science")
s = ("Python", "Machine Learning", "Data Science")

# Görev 1: veri yapılarını öğrenme
print(type(x))
print(type(y))
print(type(z))
print(type(a))
print(type(b))
print(type(l))
print(type(d))
print(type(t))
print(type(s))

#Görev 2 : stringin harflerini büyük yap noktalamaları kaldır space koy ve kelime kelime ayır

text = "The goal is turn data into information, and information into insight."


# 1: büyük harf için upper() methodu
text=text.upper()
print(text.upper())

# 2 :noktolamaların yerine space koymak için replace() methodu

text = text.replace("," ," ")
text = text.replace("." ," ")
print(text)

# 3 : kelimeleri ayırmak için split()
new_text = str(text)
print(new_text.split())

##Tek satırda olursa
text.upper().replace(","," ").replace("."," ").split()

# Görev 3 : listeye işlemler yap

lst=["D","A","T","A","S","C","I","E","N","C","E"]

# 1: Listenin eleman sayısı len()
print(len(lst))

# 2: lst[0] ve lst[10] elemanları çağır
print(lst[0], lst[10])


# 3:["D","A","T","A"] YI OLUŞTUR
del lst[4:11]
print(lst)


# 4: lst[8] i sil
lst.pop(8)
print(lst)

# 5: Yeni bir eleman ekle insert()
lst.append("P")
print(lst)


# 6: lst[8]="N"  i ata
lst.insert(8, "N")
print(lst)

# Görev 4: dictionary e işlemler yapa

dict={ 'Christian' : ["America", 18],
       'Daisy' : ["England", 12],
       'Antonio' : ["Spain", 22],
       'Dante' :  ["Italy",25]
}

# 1: key değerlerine eriş
dict.keys()

# 2: value'lara eriş
dict.values()

# 3: Daisy key'inin değerini 13 ile değiştir
dict["Daisy"] = ["America",13]
print(dict)

# 4: key= Ahmet value= ["turkey", 24] elemanını ekle
dict.update({"Ahmet" : ["Turkey",24]})
print(dict)

# 5: Antonio yu sil
dict.pop("Antonio")
print(dict)

# Görev 5: Argümanı liste olan, listedeki tekleri ve çiftleri ayrı listelere atayan ve bu listeleri return eden fonksiyonu yaz

l=[2,13,18,93,22]

def func(l):
    even_list = []
    odd_list = []
    for eleman in l:
        if eleman % 2 == 0:
            even_list.append(eleman)
        else:
            odd_list.append(eleman)

    return even_list, odd_list

even_list, odd_list= func(l)
print("Çift Sayılar", even_list)
print("Tek Sayılar", odd_list)


# Görev 6: verilen listedeki ilk üçün mühendislik son üçün tıp olduğunu ennumarete kullarak yazdır

ogrenciler= ["Ali","Veli","Ayşe","Talat","Zeynep","Ece"]

A = []
B = []

for index, student in enumerate(ogrenciler):
    if index<3:
        A.append(student)
        print("Mühendislik öğrencileri",index+1,". öğrenci :", ogrenciler[index])

    else:
        B.append(student)
        print("Tıp öğrencileri",index,". öğrenci :", ogrenciler[index])

#kısa yol
"""
for index, student in enumerate(ogrenciler[3:],1): // [:3] listenin diğer geri kalanını verir
    print(f" Mühendislik öğrencileri"{index}.ogrenci: "{ogrenci})
"""

# Görev 7: Zip ile verilen listeleri birleştir

ders_kodu=["CMP1005","PSY1001","HUK1005","SEN2204"]
kredi=[3,4,2,4]
kontenjan=[30,75,150,25]

#list(zip(ders_kodu,kredi,kontenjan))
for ders_kodu, kredi, kontenjan in zip (ders_kodu, kredi, kontenjan):
    print(f"Kredisi {kredi} olan {ders_kodu} kodlu dersin kontenjanı {kontenjan} kişidir.")

# Görev 8: verilen kümelerden 1. 2. kapsıyor ise ortakları, kapsamıyorsa 2. nin 1. den farkını yazdır

kume1= {"data", "python"}
kume2 = {"data", "function","qcut","lambda","python","miuul"}

def subsets(kume1, kume2):
    set1=set(kume1)
    set2=set(kume2)
    if set1.issuperset(set2):
        var =set1.intersection(set2)
        print(var)
    else:
        var=set2.difference(set1)
        print(var)

print(subsets(kume1, kume2))

