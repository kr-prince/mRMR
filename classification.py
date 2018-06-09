import math
import operator
#from pybrain.datasets import ClassificationDataSet
#from pybrain.utilities import percentError
#from pybrain.tools.shortcuts import buildNetwork
#from pybrain.supervised.trainers import BackpropTrainer
#from pybrain.structure.modules import SoftmaxLayer
# from sklearn import datasets
from sklearn import svm
from myUtilities import read_DataFile


def splitDataset(dataSet, splitRatio):
    trainSize = int(len(dataSet) * splitRatio)
    trainSet = []; copy = []
    copy += dataSet  # This is for having a local copy of dataSet to work on
    index = 1
    while len(trainSet) < trainSize:
        # index = random.randrange(len(copy))
        trainSet.append(copy.pop(index))
        index = (index+6)%len(copy)
        # globals()['classifProgress'] += 5.0/trainSize
    return [trainSet, copy]

def getAccuracy(testSet, predictions):
    correct = 0
    for i in range(len(testSet)):
        if testSet[i][-1] == predictions[i]:
            correct += 1
            # globals()['classifProgress'] += 20.0/len(testSet)
    return (correct/float(len(testSet))) * 100.0


# NAIVE BAYES FUNCTIONS
def separateByClass(dataSet):
    separated = {}
    for i in range(len(dataSet)):
        vector = dataSet[i]
        if (vector[-1] not in separated):
            separated[vector[-1]] = []
        separated[vector[-1]].append(vector)
    return separated

def mean(numbers):
    return sum(numbers)/float(len(numbers))

def stdev(numbers):
    avg = mean(numbers)
    # variance = sum([pow(x-avg,2) for x in numbers])/float(len(numbers)-1)
    variance = sum([pow(x-avg,2) for x in numbers])/float(len(numbers))
    return math.sqrt(variance)

def summarize(dataSet):
    try:
        summaries = [(mean(attribute), stdev(attribute)) for attribute in zip(*dataSet)]
        del summaries[-1]
        return summaries
    except:
        print "Error in summarize for ", dataSet

def summarizeByClass(dataSet):
    separated = separateByClass(dataSet)
    summaries = {}
    for classValue, instances in separated.iteritems():
        try:
            summaries[classValue] = summarize(instances)
        except:
            print "Error in summarizeByClass for ",classValue
        # globals()['classifProgress'] += 25.0/len(separated)
    return summaries

def calculateProbability(x, mean, stdev):
    try:
        # This is to do away from the error arising if stdev is becoming 0
        if stdev == 0:
            stdev = 1.0e-15
        exponent = math.exp(-(math.pow(x-mean,2)/(2*math.pow(stdev,2))))
        return (1 / (math.sqrt(2*math.pi) * stdev)) * exponent
    except:
        print "Some error in calculateProbability for x:",x," mean:",mean," stdev:",stdev

def calculateClassProbabilities(summaries, inputVector):
    probabilities = {}
    for classValue, classSummaries in summaries.iteritems():
        probabilities[classValue] = 1.0
        for i in range(len(classSummaries)):
            mean, stdev = classSummaries[i]
            x = inputVector[i]
            probabilities[classValue] *= calculateProbability(x, mean, stdev)
    return probabilities

def predict(summaries, inputVector):
    probabilities = calculateClassProbabilities(summaries, inputVector)
    bestLabel, bestProb = None, -1
    for classValue, probability in probabilities.iteritems():
        if bestLabel is None or probability > bestProb:
            bestProb = probability
            bestLabel = classValue
    return bestLabel

def getPredictions(summaries, testSet):
    predictions = []
    for i in range(len(testSet)):
        result = predict(summaries, testSet[i])
        predictions.append(result)
        # globals()['classifProgress'] += 50.0/len(testSet)
    return predictions

def naiveBayes(trainingSet, testSet):
    trSet = trainingSet; teSet = testSet
    # prepare model
    summaries = summarizeByClass(trSet)
    # test model
    predictions = getPredictions(summaries, teSet)
    # if classifProgress < 100.0:
    #     globals()['classifProgress'] = 100.0
    return predictions


# SVM FUNCTIONS
def svmClassifier(trainingSet, testSet):
    trainX = []; trainY = []
    testX = []; testY = []
    # Preprocess Data
    for eachrow in trainingSet:
        trainX.append(eachrow[:-1])
        trainY.append(eachrow[-1])
    for eachrow in testSet:
        testX.append(eachrow[:-1])
        testY.append(eachrow[-1])

    # Create SVM classification object  'C': 10.0, 'gamma': 0.0001
    # model = svm.SVC(kernel='linear', C=10.0, gamma=0.0001)
    model = svm.LinearSVC()
    # Train the SVM model
    model.fit(trainX, trainY)
    # Predict Output
    predictions = model.predict(testX)
    return predictions


# KNN CLASSIFIER
def euclideanDistance(instance1, instance2):
    distance = 0.0
    for x in range(len(instance1)):
        distance += pow((instance1[x] - instance2[x]), 2)
    return math.sqrt(distance)

def getNeighbors(trainingSet, testInstance, k):
    distances = []
    for x in range(len(trainingSet)):
        dist = euclideanDistance(testInstance, trainingSet[x])
        distances.append((trainingSet[x], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors

def getResponse(neighbors):
    classVotes = {}
    for x in range(len(neighbors)):
        response = neighbors[x][-1]
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1
    sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]

def knnClassifier(trainingSet, testSet):
    trainSet = []; teSet = []
    trainSet += trainingSet
    teSet += testSet
    # generate predictions
    predictions = []
    k = 2
    for x in range(len(testSet)):
        neighbors = getNeighbors(trainSet, teSet[x], k)
        result = getResponse(neighbors)
        predictions.append(result)
    return predictions


# NEURAL NETWORKS

#def nnClassifier(trainingSet,testSet,nofclasses,layers=2):
#    inDim = len(trainingSet[1])-1
#    outDim = 1
#    trainSet = []; teSet = []
#    trainSet += trainingSet
#    teSet += testSet

    # ClassificationDataSet(no. of gene attributes, dim of output, no of classes)
#    trndata =ClassificationDataSet(inDim, outDim, nb_classes=nofclasses)
#    tstdata =ClassificationDataSet(inDim, outDim, nb_classes=nofclasses)
#
#    while len(trainSet) > 0:
#        trndata.addSample(trainSet[0][:-1],trainSet[0][-1])
#        trainSet.pop(0)
#    while len(teSet) > 0:
#        tstdata.addSample(teSet[0][:-1], teSet[0][-1])
#        teSet.pop(0)
    # print tstdata['input']
    # print tstdata['target']
    # print len(tstdata), len(tstdata['input']), len(tstdata['target'])
#    trndata._convertToOneOfMany()
#    tstdata._convertToOneOfMany()

 #   net = buildNetwork(inDim, int(inDim*0.7), nofclasses, outclass=SoftmaxLayer)
 #   trainer = BackpropTrainer(net, dataset=trndata, momentum=0.01, verbose=False, weightdecay=0.1)
#    trainer.trainOnDataset(trndata, 500)
#    out = net.activateOnDataset(tstdata)
    # Returns the indices of the maximum values along an axis
#    out = out.argmax(axis=1)
#    print percentError(out, tstdata['class'])
    # weights = []
    # for i in range(1, len(layers) - 1):
    #     self.weights.append((2 * np.random.random((layers[i - 1] + 1, layers[i]
    #                                                + 1)) - 1) * 0.25)
    # self.weights.append((2 * np.random.random((layers[i] + 1, layers[i +
    #                                                                  1])) - 1) * 0.25)



def classifyData(data, splitRatio=0.67, app=None, hybrid=False):
    if app is not None:
        app.updateProgress('Classification Started..')
    dataset = []
    accResults = {}
    for row in data[1:]:
        dataset.append([float(elem) for elem in row])
    trainingSet, testSet = splitDataset(dataset, splitRatio)
    if app is not None:
        app.updateProgress('Naive Bayes at Work..')
    # print nnClassifier(trainingSet, testSet, int(data[0][2]))
    # return
    nbpredictions = naiveBayes(trainingSet, testSet)
    accResults['nb'] = round(getAccuracy(testSet, nbpredictions),3)
    # print 'Naive Bayes : ', accResults['nb']
    if app is not None:
        app.updateProgress('SVM at Work..')
    # print len(trainingSet)
    # print len(testSet)
    if not hybrid:
        svmpredictions = svmClassifier(trainingSet, testSet)
        accResults['svm'] = round(getAccuracy(testSet, svmpredictions), 3)
    # print 'Support Vector Machine : ', accResults['svm']
    if app is not None:
        app.updateProgress('kNN at Work..')
    knnpredictions = knnClassifier(trainingSet, testSet)
    accResults['knn'] = round(getAccuracy(testSet, knnpredictions), 3)
    # print 'k Nearest Neighbour : ', accResults['knn']
    if not hybrid:
        if app is not None:
            app.updateProgress('Hybrid Classifier at Work..')
        sigmaPredictions = []
        for pred in range(len(testSet)):
            value = ((nbpredictions[pred]*accResults['nb'])+(svmpredictions[pred]*accResults['svm'])+
                     (knnpredictions[pred]*accResults['knn']))/(accResults['nb']+accResults['svm']+accResults['knn'])
            n = abs(value - nbpredictions[pred])
            s = abs(value - svmpredictions[pred])
            k = abs(value - knnpredictions[pred])
            if n < s:
                if n < k:
                    sigmaPredictions.append(nbpredictions[pred])
                elif n == k:
                    if accResults['nb'] > accResults['knn']:
                        sigmaPredictions.append(nbpredictions[pred])
                    else:
                        sigmaPredictions.append(knnpredictions[pred])
                else:
                    sigmaPredictions.append(knnpredictions[pred])
            elif n == s:
                if n < k:
                    sigmaPredictions.append(nbpredictions[pred])
                elif n ==k:
                    sigmaPredictions.append(knnpredictions[pred])
                else:
                    sigmaPredictions.append(knnpredictions[pred])
            else:
                if s < k:
                    sigmaPredictions.append(svmpredictions[pred])
                elif s == k:
                    if accResults['svm'] > accResults['knn']:
                        sigmaPredictions.append(svmpredictions[pred])
                    else:
                        sigmaPredictions.append(knnpredictions[pred])
                else:
                    sigmaPredictions.append(knnpredictions[pred])

            # if nbpredictions[pred]==svmpredictions[pred]:
            #     sigmaPredictions.append(nbpredictions[pred])
            # elif svmpredictions[pred]==knnpredictions[pred]:
            #     sigmaPredictions.append(knnpredictions[pred])
            # elif nbpredictions[pred]==knnpredictions[pred]:
            #     sigmaPredictions.append(nbpredictions[pred])
            # else:
            #     sigmaPredictions.append(knnpredictions[pred])
        accResults['hy'] = round(getAccuracy(testSet, sigmaPredictions), 3)
        # print 'Hybrid Classifier : ', accResults['ec']
    return accResults
    # nnClassifier(trainingSet, testSet, int(data[0][2]))

# myData = read_DataFile('data\\breastCancerData.csv')
# myData = read_DataFile('data\\leukemiaData.csv')
# myData = read_DataFile('data\\colonData2.csv')
# myData = read_DataFile('data\\iris.csv')
# myData = read_DataFile('data\\wine.csv')
# myData = read_DataFile('data\\myRandomData.csv')
# print classifyData(myData,0.7)
