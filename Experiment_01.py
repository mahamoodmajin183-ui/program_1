import csv
from pathlib import Path

try:
    BASE_DIR = Path(__file__).resolve().parent
except NameError:
    BASE_DIR = Path.cwd()
DATA_DIR = BASE_DIR / "datasets"

a = []
with open(DATA_DIR / "enjoysport.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        a.append(row)

print("The Given Training Data Set")
for row in a:
    print(row)

print("\n The total number of training instances are : ", len(a))

num_attribute = len(a[0]) - 1

print("\n The initial hypothesis is : ")
hypothesis = ['0'] * num_attribute
print(hypothesis)

for i in range(0, len(a)):
    if a[i][num_attribute] == 'yes':
        for j in range(0, num_attribute):
            if hypothesis[j] == '0' or hypothesis[j] == a[i][j]:
                hypothesis[j] = a[i][j]
            else:
                hypothesis[j] = '?'
    print("\n The hypothesis for the training instance {} is : \n".format(i + 1), hypothesis)

print("\n The Maximally specific hypothesis for the training instance is ")
print(hypothesis)
