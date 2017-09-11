from sklearn.metrics import accuracy_score
from sklearn import datasets
import random
from sklearn.cross_validation import train_test_split
from scipy.spatial import distance

def euc(a, b):
	return distance.euclidean(a,b)

class ScrappyKNN():
	def fit(self, X_train, Y_train) : 
		self.X_train = X_train
		self.Y_train = Y_train

	def closest(self,row):
		best_dist = euc(row, self.X_train[0])
		best_index = 0
		for i in range(1,len(self.X_train)):
			dist = euc(row,self.X_train[i])
			if dist < best_dist:
				best_dist = dist
				best_index = i
		return self.Y_train[best_index]

	def predict(self, X_test):
		predictions = []
		for row in X_test:
			label = self.closest(row)
			predictions.append(label)
		return predictions

iris = datasets.load_iris()
X = iris.data
Y = iris.target

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.5)
clf = ScrappyKNN()
clf.fit(X_train, Y_train)
p = clf.predict(X_test)
a = accuracy_score(Y_test, p)
print("Accuracy = " + str(a*100))



