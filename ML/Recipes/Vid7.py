from sklearn import metrics,cross_validation
import tensorflow as tf
from tensorflow.contrib import learn

def main(unused_argv):
	#Load dataset.
	iris = learn.datasets.load_dataset('iris')
	X = iris.data
	Y = iris.target
	X_train, X_test, Y_train, Y_test = cross_validation.train_test_split(X, Y, test_size=0.5)

	clf = learn.DNNClassifier(hidden_units=[10,20,30], n_classes=3)

	clf.fit(X_train, Y_train, steps=200)
	score = metrics.accuracy_score(Y_test,clf.predict(X_test))
	print("ACCURACY : {0:f}".format(score))


