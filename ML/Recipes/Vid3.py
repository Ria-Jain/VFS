from sklearn import tree
from matplotlib import pyplot as plt
import numpy as np


greyhounds = 500
labrador = 500

gray_height = 28 + 4 * np.random.randn(greyhounds)
lab_height = 24 + 4 * np.random.randn(labrador)

plt.hist([gray_height, lab_height], stacked=True, color=['r','b'])
plt.show()