import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

dataset = pd.read_csv('MatType.csv')

X = dataset.iloc[:, [0,1]].values  
y = dataset.iloc[:, 2].values  

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 1/3)

from sklearn.tree import DecisionTreeClassifier 
model = DecisionTreeClassifier(max_depth=8) 

model.fit(X_train, y_train)

# ================================================================
# perf_counter
# 
# Return the value (in fractional seconds) of a performance counter, i.e. a clock with the highest 
# available resolution to measure a short duration. It does include time elapsed during sleep. The 
# clock is the same for all processes. The reference point of the returned value is undefined, 
# so that only the difference between the results of two calls is valid.
# 
# https://docs.python.org/3/library/time.html
# ================================================================

import time
import random

start = time.perf_counter()

run = 1000
i = 0
while i < run:
    a1 = random.random()
    a2 = random.random()
    y_pred = model.predict([[a1, a2]])
    i = i + 1

# Ponto final da medição
finish = time.perf_counter()

# Cálculo do tempo total
tempo_total =  finish - start

print(f"Tempo pelo perf_counter: {tempo_total:.4f} segundos")

# ================================================================
# process_time
# 
# Return the value (in fractional seconds) of the sum of the system and user CPU time of the current process. 
# It does not include time elapsed during sleep. It is process-wide by definition. The reference point of the 
# returned value is undefined, so that only the difference between the results of two calls is valid.
# 
# https://docs.python.org/3/library/time.html
# ================================================================

# Ponto inicial da medição
start = time.process_time()

run = 1000
i = 0
while i < run:
    a1 = random.random()
    a2 = random.random()
    y_pred = model.predict([[a1, a2]])
    i = i + 1

# Ponto final da medição
finish = time.process_time()

# Cálculo do tempo total
tempo_total = finish - start

print(f"Tempo pelo process_time: {tempo_total:.4f} segundos")