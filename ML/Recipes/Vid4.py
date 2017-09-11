from sklearn import datasets
from sklearn.cross_validation import train_test_split
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn import neighbors

iris = datasets.load_iris()

X = iris.data
Y = iris.target

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.5 )

clf1 = tree.DecisionTreeClassifier()
clf1.fit(X_train, Y_train)
pred1 = clf1.predict(X_test)
accuracy1 = accuracy_score(Y_test, pred1)
print("accuracy = " + str(accuracy1*100))

clf2 = neighbors.KNeighborsClassifier()
clf2.fit(X_train, Y_train)
pred2 = clf2.predict(X_test)
accuracy2 = accuracy_score(Y_test, pred2)
print("accuracy = " + str(accuracy2*100))


