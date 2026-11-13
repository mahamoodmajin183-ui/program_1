from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn import datasets

RANDOM_STATE = 497

iris = datasets.load_iris()

x = iris.data
y = iris.target

print('sepal-length', 'sepal-width', 'petal-length', 'petal-width')
print(x)
print('class: 0-Iris-Setosa, 1- Iris-Versicolour, 2- Iris-Virginica')
print(y)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=RANDOM_STATE)

classifier = KNeighborsClassifier(n_neighbors=5)
classifier.fit(x_train, y_train)

y_pred = classifier.predict(x_test)

print('Confusion Matrix')
print(confusion_matrix(y_test, y_pred))
print('Accuracy Metrics')
print(classification_report(y_test, y_pred))

names = iris.target_names
correct = [(i, t, p) for i, (t, p) in enumerate(zip(y_test, y_pred)) if t == p]
wrong = [(i, t, p) for i, (t, p) in enumerate(zip(y_test, y_pred)) if t != p]

print(f'\nCorrect predictions: {len(correct)}')
for i, t, p in correct:
    print(f'  sample {i:2d}  features={x_test[i]}  actual={names[t]:<10} predicted={names[p]}')

print(f'\nWrong predictions: {len(wrong)}')
for i, t, p in wrong:
    print(f'  sample {i:2d}  features={x_test[i]}  actual={names[t]:<10} predicted={names[p]}')
