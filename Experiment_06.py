import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics

try:
    BASE_DIR = Path(__file__).resolve().parent
except NameError:
    BASE_DIR = Path.cwd()
DATA_DIR = BASE_DIR / "datasets"

TEST_SIZE = 0.25
RANDOM_STATE = 81

msg = pd.read_csv(DATA_DIR / 'naivetext.csv', names=['message', 'label'])
print('The dimensions of the dataset', msg.shape)

msg['labelnum'] = msg.label.map({'pos': 1, 'neg': 0})
X = msg.message
y = msg.labelnum
print(X)
print(y)

xtrain, xtest, ytrain, ytest = train_test_split(X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE)
print('\nThe total number of Training Data :', ytrain.shape)
print('The total number of Test Data :', ytest.shape)

count_vect = CountVectorizer()
xtrain_dtm = count_vect.fit_transform(xtrain)
xtest_dtm = count_vect.transform(xtest)
print('\nThe words or Tokens in the text documents\n')
print(count_vect.get_feature_names_out())

df = pd.DataFrame(xtrain_dtm.toarray(), columns=count_vect.get_feature_names_out())
print('\nSample Bag-of-Words representation (first rows):')
print(df.head())

clf = MultinomialNB().fit(xtrain_dtm, ytrain)
predicted = clf.predict(xtest_dtm)

print('\nAccuracy of the classifier is', metrics.accuracy_score(ytest, predicted))
print('\nConfusion matrix')
print(metrics.confusion_matrix(ytest, predicted))
print('\nThe value of Precision', metrics.precision_score(ytest, predicted))
print('\nThe value of Recall', metrics.recall_score(ytest, predicted))
