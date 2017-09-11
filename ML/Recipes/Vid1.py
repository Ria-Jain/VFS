from sklearn import tree

features = [[140,0],[180,1],[170,1],[110,0],[130,0],[190,1],[200,1]]		#	0->smooth	1->bumpy
labels = [['A'],['O'],['O'],['A'],['A'],['O'],['O']]

clf = tree.DecisionTreeClassifier()
clf.fit(features,labels)

find = [[111,0],[200,1],[115,0],[101,0],[160,1]]

ans = clf.predict(find)

print(ans)
