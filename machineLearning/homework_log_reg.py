import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from sklearn.metrics import (roc_auc_score, roc_curve, accuracy_score, confusion_matrix,classification_report, precision_score,recall_score, f1_score)

##########################################################################
# GÖREV 1 :
# Müşterinin churn olup olmama durumunu tahminleyen
# bir sınıflandırma modeli oluşturulmuştur. 10 test verisi gözleminin
# gerçek değerleri ve modelin tahmin ettiği olasılık değerleri verilmiştir:
###########################################################################

# Gercek Degerler
y = [1,1,1,1,1,1,0,0,0,0]

# Model Tahmini Olan Degerler
y_pred = [0.7, 0.8, 0.65, 0.9, 0.45, 0.5, 0.55, 0.35, 0.4, 0.25]

# Sürekli degerler ile binary olan degerlerin karsiltirilmasi sonucunda value error alacagimizdan binary e cevirelim.
# Ve ayrica y_pred bir list ve threshold ise bir float deger oldugundan bunlarin karsilastirmasini yapmak icin y_pred'i bir np array'e dönüstürelim

threshold = 0.5  # Eşik değeri
y_pred_binary = (np.array(y_pred) >= threshold).astype(int)

print(y_pred_binary)

#y_pred_binary = [1 if prob >= 0.5 else 0 for prob in y_pred]


#########################################################
# Model Evaluation
# Confusion matrix oluşturunuz.
#########################################################

def plot_confusion_matrix(y, y_pred_binary):
    acc = round(accuracy_score(y, y_pred_binary), 2)
    cm = confusion_matrix(y, y_pred_binary)
    sns.heatmap(cm, annot=True, fmt=".0f")
    plt.xlabel('y_pred')
    plt.ylabel('y')
    plt.title('Accuracy Score: {0}'.format(acc), size=10)
    plt.show(block=True)

plot_confusion_matrix(y, y_pred_binary)

print(classification_report(y, y_pred_binary))

#########################################################
# Model Validation
# Accuracy,Recall,Precision,F1 Skorlarını hesaplayınız.
#########################################################

# Gercek Degerler
y = [1,1,1,1,1,1,0,0,0,0]
# Model Tahmini Olan Degerler
y_pred = [0.7, 0.8, 0.65, 0.9, 0.45, 0.5, 0.55, 0.35, 0.4, 0.25]

# bu da ikinci yöntem
y_pred_binary = [1 if prob >= 0.5 else 0 for prob in y_pred]

# Metrikleri hesaplaarken elimde tahmin edilmis degerler oldugu icin bu sekilde dogrudan hesaplama yapabilirim.

accuracy = accuracy_score(y, y_pred_binary)
precision = precision_score(y, y_pred_binary)
recall = recall_score(y, y_pred_binary)
f1 = f1_score(y, y_pred_binary)


print(f"Accuracy: {accuracy:.3f}")
print(f"Precision: {precision:.3f}")
print(f"Recall: {recall:.3f}")
print(f"F1 Score: {f1:.3f}")

###########################################################################################
# GÖREV 2 :
# Banka üzerinden yapılan işlemler sırasında dolandırıcılık işlemlerinin yakalanması
# amacıyla sınıflandırma modeli oluşturulmuştur. %90.5 doğruluk oranı elde edilen modelin
# başarısı yeterli bulunup model canlıya alınmıştır. Ancak canlıya alındıktan sonra modelin
# çıktıları beklendiği gibi olmamış,iş birimi modelin başarısız olduğunu iletmiştir.
# Aşağıda modelin tahmin sonuçlarının karmaşıklık matriksi verilmiştir. Buna göre;
###########################################################################################

# Karışıklık matrisi (Confusion Matrix)
conf_matrix = np.array([[5, 5],
                        [90, 900]])

# Etiketler
labels = ["Fraud (1)", "Non-Fraud (0)"]

plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Reds", xticklabels=labels, yticklabels=labels)

plt.title("Confusion Matrix")
plt.xlabel("Model Tahmini")
plt.ylabel("Gerçek Değer")
plt.show(block=True)

###########################################################################################
# Accuracy, Recall, Precision, F1 Skorlarını hesaplayınız.
###########################################################################################
# gercek degerler ve tahmin degerleri verilmediginden bu sekilde bir hesaplama yapabiliriz.

# Karışıklık matrisindeki değerler
TP = 5   # True Positive
FP = 90  # False Positive
TN = 900 # True Negative
FN = 5   # False Negative

# Accuracy (Doğruluk)
accuracy = (TP + TN) / (TP + TN + FP + FN)

# Precision (Kesinlik)
precision = TP / (TP + FP)

# Recall (Duyarlılık)
recall = TP / (TP + FN)

# F1 Score
f1_score = 2 * (precision * recall) / (precision + recall)

print(f"Accuracy: {accuracy:.3f}")
print(f"Precision: {precision:.3f}")
print(f"Recall: {recall:.3f}")
print(f"F1 Score: {f1_score:.3f}")

###########################################################################################
# Veri Bilimi ekibinin gözden kaçırdığı durum ne olabilir yorumlayınız.
###########################################################################################