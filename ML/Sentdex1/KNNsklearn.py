import numpy as np
from sklearn import cross_validation, neighbors, preprocessing
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import pickle

style.use('fivethirtyeight')
df = pd.read_csv('breast_cancer.txt')
df.replace('?', -99999, inplace=True)
df.drop(['id'], 1, inplace=True)

X = np.array(df.drop(['class'],1))
y = np.array(df['class'])

X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, y, test_size=0.2)

clf = neighbors.KNeighborsClassifier()

clf.fit(X_train, y_train)

accuracy = clf.score(X_test, y_test)

example_measures = np.array([4,2,1,1,1,2,3,2,1])
example_measures = example_measures.reshape(1,-1)

print(accuracy)

pred = clf.predict(example_measures)

plt.xlabel('Data')
plt.ylabel('Class')
plt.scatter(X, y)
plt.plot(X , pred, color='g', s=100)
plt.show()
print(pred)
 