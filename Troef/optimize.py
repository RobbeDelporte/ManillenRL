from hashlib import new
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import itertools

data = pd.read_csv("troef.csv",header=None)

suits = ["SPADES","DIAMONDS","CLUBS","HEARTS"]

#preproccessing
data[8] = data.apply(lambda row: suits.index(row[8]),axis=1)
for i in range(0,32):
    data[f"c{i}"] = data.apply(lambda row: (i in list(row[0:8]))*1,axis=1)
data["y"] = data[8]
data = data.drop([0,1,2,3,4,5,6,7,8],axis=1)


#augmenting
extradata = []
for l,row in data.iterrows():
    x = row[:32]
    y = row[-1:]
    parts = np.array([x[0:8],x[8:16],x[16:24],x[24:32]])
    troefpart = parts[y][0]
    for p in itertools.permutations(parts):
        newparts = np.array([p[0],p[1],p[2],p[3]])
        r = np.concatenate((p[0],p[1],p[2],p[3],[np.where(np.all(newparts==troefpart,axis=1))[0][0]]))
        extradata.append(r)
extradata = pd.DataFrame(extradata)

print(data.head())
print(extradata.head())

#splitting data
train,test = train_test_split(extradata,test_size=0.2)
x_train = np.array(train.iloc[:, 0:32])
x_test = np.array(test.iloc[:, 0:32])
y_train = np.array(train.iloc[:, -1:])
y_test = np.array(test.iloc[:,-1:])

correct = 0
wrong = 0

def algorithm(hand):
    best = np.inf
    best_x = 0
    best_y = 0
    for x,y in zip(x_train,y_train):
        dist = np.linalg.norm(x-hand)
        if dist < best:
            best = dist
            best_x = x
            best_y = y

    return best_y

i = 0
for x,y in zip(x_test,y_test):
    i += 1
    if i%100 == 0:
        print(i)
    r = algorithm(x)
    if r == y:
        correct += 1
    else:
        wrong += 1

print(correct,wrong)
print(f"{correct/(correct+wrong)*100}%")
