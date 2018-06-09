import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn import svm
from classification import read_DataFile

# digits = datasets.load_digits()
# print digits.data, len(digits.data)
# print digits.target, len(digits.data)
# clf = svm.SVC(gamma=0.00001, C=100)
# X,y = digits.data[:-10], digits.target[:-10]
# clf.fit(X,y)
# plt.imshow(digits.images[-5], cmap=plt.cm.gray_r, interpolation='nearest')
# plt.show()

#Assumed you have, X (predictor) and Y (target) for training data set and x_test(predictor) of test_dataset
# Create SVM classification object  'C': 100.0, 'gamma': 0.0001
model = svm.SVC(kernel='linear', gamma=0.0001, C=10.0)
# there is various option associated with it, like changing kernel, gamma and C value. Will discuss more10.0
# about it in next section.Train the model using the training sets and check score0.0005
myData = read_DataFile("data\\colonData.csv")
myData.pop(0)
trainX = []; trainY = []
testX = []; testY = []
size = int(len(myData) * 0.7)
index = 1
while len(trainX) < size:
    trainX.append([float(num) for num in myData[index][:-1]])
    trainY.append(int(myData[index][-1]))
    myData.pop(index)
    index = (index+6)%len(myData)
while len(myData) != 0:
    testX.append([float(num) for num in myData[0][:-1]])
    testY.append(int(myData[0][-1]))
    myData.pop(0)

# opfile = open('trainSet_leukemia.csv', 'w+')
#     for r in trainSet:
#         c = 0
#         for el in r:
#             opfile.write(str(el))
#             c += 1
#             if c == len(r):
#                 opfile.write('\n')
#             else:
#                 opfile.write(',')
#     opfile.close()
model.fit(trainX, trainY)
# model.score(testX, testY)
#Predict Output
accuracy =0.0
predicted= model.predict(testX)
for i in range(len(predicted)):
    if predicted[i]==testY[i]:
        accuracy +=1.0
print 'Accuracy : ', (accuracy*100)/len(predicted)