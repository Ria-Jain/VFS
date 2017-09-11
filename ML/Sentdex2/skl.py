import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn import svm

digits = datasets.load_digits()

clf = svm.SVC(gamma=0.0000000000000000000000000001, C=100)

#print(len(digits.data))

x,y = digits.data[:-10], digits.target[:-10]         #training Computer for N-10 elements

clf.fit(x,y)										 #Fitting it to the graph

#print(digits.data)

#print(len(digits.target))

#print(digits.target)

print('Prediction : ', clf.predict(digits.data[-9]))			#predict the TARGET for the given DATA
print('Actual digit :  ', digits.target[-9])
plt.imshow(digits.images[-9],cmap=plt.cm.gray_r, interpolation="nearest")
plt.show()