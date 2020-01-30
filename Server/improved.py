from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.externals.six import StringIO 
import pandas as pd
import numpy as np
data = pd.read_csv("cropDB.csv") 
print(data.head)