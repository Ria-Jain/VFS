from sklearn.datasets import load_iris
import numpy as np
from sklearn import tree

iris = load_iris()
test_idx = [0,50,100]


#Training Data
train_target = np.delete(iris.target, test_idx)
train_data = np.delete(iris.data, test_idx, axis=0)

#Testing Data
test_target = iris.target[test_idx]
test_data = iris.data[test_idx]


#FITTING:
clf = tree.DecisionTreeClassifier()
clf.fit(train_data, train_target)

print(test_target)
#PREDICTING:
print(clf.predict(test_data))






######################################################
from sklearn.externals.six import StringIO
import pydot

dot_data = StringIO()
tree.export_graphviz(clf,
						out_file=dot_data,
						feature_names=iris.feature_names,
						class_names=iris.class_names,
						filled=True, rounded=True,
						impurity=False)
graph = pydot.graph_from_dot_data(dot_data.getvalue())
graph.write_pdf("iris.pdf")
