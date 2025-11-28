import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

dataset = pd.read_csv('MatType.csv')

X = dataset.iloc[:, [0,1]].values  
y = dataset.iloc[:, 2].values  

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 1/3)

from sklearn.tree import DecisionTreeClassifier 
model = DecisionTreeClassifier(max_depth=3) 

model.fit(X_train, y_train)

# ============================================
# método 2
# ============================================
from pympler import asizeof

tamanho_bytes = asizeof.asizeof(model)
tamanho_mb = tamanho_bytes / (1024 * 1024)

print(f"Tamanho total do modelo na memória: {tamanho_bytes:.2f} MB")