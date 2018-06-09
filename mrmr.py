from __future__ import division
import math
import copy
from classification import classifyData
from numpy import array, shape, where, in1d


# This definition is for calculating pearson coefficient correlation
def pearson_coefficient( n1, x, y ):
    sum_x = sum_y = sum_sq_dif_x = sum_sq_dif_y = upper = 0.0
    for i in range(n1):
        sum_x += x[i]
        sum_y += y[i]

    mean_x = float(sum_x/n1)
    mean_y = float(sum_y/n1)
    for i in range(n1):
        sum_sq_dif_x += ((x[i] - mean_x)**2)
        sum_sq_dif_y += ((y[i] - mean_y)**2)
        upper += ((x[i] - mean_x) * (y[i] - mean_y))

    lower = float(math.sqrt(sum_sq_dif_x * sum_sq_dif_y))
    if lower == 0:
        corr_coef = 0.0
    else:
        corr_coef = float(upper/lower)
    return abs(corr_coef)

def mrmrFTestPearson(data, reqFeatures, app = None):
    # h = classification variable
    # gi = gene variable
    # klist = list of classes available(k), ksize = size of kth class(is not nk, no of rows having k)
    # n = sum of all nk, ksum = sum of all gi of some particular k
    # kvar = variance of kth class, var = overall variance
    # gbar = mean of all gi for each i(col), gkbar = mean of all gi for each k(class)
    # ftestval = value of ftest function for each gi
    # mrmrCProgress = gives the progress of this task to animation app
    mrmrCProgress = 0.0
    if app is not None:
        app.updateProgress('mRMR with FCD started')

    klist = []; ksize = {}; ksum = {}; kvar = {}
    gbar = []; gkbar = []; ftestval = {}
    # first row of data list has meta-data, not actual data
    # row = no of samples, col = no of features
    row = int(data[0][0])
    col = int(data[0][1])

    for si in data[1:]:
        # si[-1] is the class and has to be in klist, if not, then include it, also update ksize
        # if it is there then update the size
        if si[-1] not in klist:
            klist.append(si[-1])
            ksize[si[-1]] = 1
        else:
            if ksize.has_key(si[-1]):
                ksize[si[-1]] += 1
            else:
                print "Error : class in klist, not found in dict(ksize)"
                exit()
        # ksum stores the sum of all features of each class
        if not ksum.has_key(si[-1]):
            ksum[si[-1]] = 0
        for j in si[:-1]:
            ksum[si[-1]] += float(j)
    mrmrCProgress += 2.0
    if app is not None:
        app.updateProgress('%.1f %%' % mrmrCProgress)

    # find each kvar for each class
    for ki in klist:
        # tmean is the mean and tsum is the sum of squared differences
        tmean = float(ksum[ki]/(ksize[ki]*col))
        tsum = 0
        # Here we are going down row wise and checking if this row is of the ki class
        for di in data[1:]:
            if di[-1] == ki:
                for num in di[:-1]:
                    tsum += (tmean - float(num))**2
        if not kvar.has_key(ki):
            kvar[ki] = float(tsum/(ksize[ki]*col))
            # will not do kvar[i] = kvar[i]**2, as variance is denoted by sigma^2
        else:
            print "some error occurred in calculating var(k).."
    mrmrCProgress += 2.0
    if app is not None:
        app.updateProgress('%.1f %%' % mrmrCProgress)

    # find the pooled variance = var (for all classes)
    # nk = size of each class x features in each col( = col)
    var = 0
    for i in klist:
        var += float((ksize[i]-1)*kvar[i])
    var /= float(row - len(klist))
    mrmrCProgress += 1.0
    if app is not None:
        app.updateProgress('%.1f %%' % mrmrCProgress)

    # Now after calculating the pooled variance, we move on to find the F-Test values
    # of all the gene variables(gi), but first find gbar and gkbar
    for gi in xrange(col):
        gbar.append(0)
        for si in xrange(1, row+1, 1):
            gbar[gi] += float(data[si][gi])
            if len(gkbar) <= gi:
                # This means that no entry has been made in gkbar for this value of gi
                # make an entry to increase the list index, else it will cause exception
                gkbar.append({data[si][-1]: float(data[si][gi])})
            else:
                # Means some entry has been made, if the class for this row is present then
                # simple add the value, else add this class as a key and initialize with this si value
                if gkbar[gi].has_key(data[si][-1]):
                    gkbar[gi][data[si][-1]] += float(data[si][gi])
                else:
                    gkbar[gi][data[si][-1]] = float(data[si][gi])
        # Divide the sum by the number of samples(rows) to actually get the mean
        gbar[gi] = float(gbar[gi]/row)
        for ki in klist:
            if gkbar[gi].has_key(ki):
                # Sum of gi for each class/size of the class, correspondingly
                gkbar[gi][ki] = float(gkbar[gi][ki]/ksize[ki])
        mrmrCProgress += 20.0/col
        if app is not None:
            app.updateProgress('%.1f %%' % mrmrCProgress)

    # For F-Test function calculation
    for gi in xrange(col):
        tsum = float(0.0)
        # print '\n\ngi : ', gi
        for ki in klist:
            tsum += (((ksize[ki])*(gkbar[gi][ki]-gbar[gi])**2)/(row-1))
        ftestval[gi] = float(tsum/var)
        mrmrCProgress += 5.0/col
        if app is not None:
            app.updateProgress('%.1f %%' % mrmrCProgress)

    # maxftestval stores the feature with maxvalue of f-Test which starts the algo as first
    # selected feature
    # selectedfeatures stores the list of features selected as set of reduced features
    # nonselectedfeatures stores the list of features not selected yet
    # sigmacorval stores the value of sig(corr-coeff) for any (gi) with all other gj's in incremental way
    # import operator
    # print 'sortedftestval : ',sorted(ftestval.items(), key=operator.itemgetter(1))
    maxftestval = max(ftestval, key=lambda k: ftestval[k])
    selectedfeatures = []

    selectedfeatures.append(maxftestval)
    nonselectedfeatures = list(set(ftestval.keys())-{maxftestval})
    # print 'nonselectedfeaturelist : ',nonselectedfeatures
    # data matrix is transposed to align it feature wise not sample wise
    transdata = [list(float(n) for n in x) for x in zip(*data[1:])]
    sigmacorval = {}
    reduceDataSet = [[0,0,0]]
    featureCount = 1
    # These variables help in optimal selection
    # tempRedData = []
    # classAcc = {'knn': 0.0, 'svm': 0.0}
    oldClassAcc = {'knn': 0.0, 'nb': 0.0}
    while True:
        funcval = -10.0; gi = -2
        prevFeature = selectedfeatures[-1]
        for giNs in nonselectedfeatures:
            if sigmacorval.has_key(giNs):
                sigmacorval[giNs] += pearson_coefficient(row,transdata[giNs],transdata[prevFeature])
            else:
                sigmacorval[giNs] = pearson_coefficient(row,transdata[giNs],transdata[prevFeature])
            # print "g(%d,%d)" % (giNs, prevFeature), pearson_coefficient(row, transdata[giNs], transdata[prevFeature])
            if (ftestval[giNs] - (sigmacorval[giNs]/len(selectedfeatures))) > funcval:
                funcval = ftestval[giNs] - (sigmacorval[giNs]/len(selectedfeatures))
                gi = giNs
        if gi != -2:
            selectedfeatures.append(gi)
            featureCount +=1
            nonselectedfeatures.remove(gi)
            del sigmacorval[gi]
        # Saving the current DataSet Making the next reducedDataSet
        tempRedData = copy.deepcopy(reduceDataSet)
        reduceDataSet[0] = [row, featureCount, len(klist)]
        if len(reduceDataSet) == 1:
            for si in range(row):
                # To insert the first feature(maxfTest)
                reduceDataSet.append([transdata[selectedfeatures[0]][si], int(transdata[-1][si])])
        # print transdata
        # print reduceDataSet
        for si in range(1, row + 1):
            # print selectedfeatures
            # print transdata
            reduceDataSet[si].insert(-1,float(transdata[selectedfeatures[-1]][si-1]))
            # print reduceDataSet
        if reqFeatures == 0:
            # print featureCount, '---'
            # print 'tData : ', tempRedData
            # print 'rData : ', reduceDataSet
            classAcc = classifyData(reduceDataSet,0.7,None,True)
            # print classAcc, ' : ', oldClassAcc
            # print '--------------------------'
            if classAcc['knn'] > oldClassAcc['knn'] or classAcc['nb'] > oldClassAcc['nb']:
                # print reduceDataSet
                oldClassAcc['knn'] = classAcc['knn']
                oldClassAcc['nb'] = classAcc['nb']
                # pass
            elif classAcc['knn'] > 90.0 and classAcc['nb'] > 90.0:
                oldClassAcc['knn'] = classAcc['knn']
                oldClassAcc['nb'] = classAcc['nb']
            else:
                # print classAcc,' : ', oldClassAcc,' : ',selectedfeatures[-1],' rejected'
                featureCount -= 1
                reduceDataSet = tempRedData
            if len(selectedfeatures) == col:
                break
        if app is not None:
            if reqFeatures > 0:
                mrmrCProgress += 70.0 / (reqFeatures - 1)
                app.updateProgress('%.1f %%' % mrmrCProgress)
            else:
                app.updateProgress('%d Features added' % featureCount)
        # else:
        #     print 'wtf'
        if reqFeatures != 0 and featureCount == reqFeatures:
            break

    # print 'selectedfeatures : ',selectedfeatures, len(selectedfeatures)
    # print 'nonselectedfeaturelist : ',nonselectedfeatures, len(nonselectedfeatures)
    # if reqFeatures == 1: # This is to help in optimal Data Reduction
    #     return selectedfeatures
    # if reqFeatures > 0:
    #     for si in selectedfeatures:
    #         reduceDataSet.append(transdata[si])
    #     # reduceDataSet.append(transdata[-1])
    #     reduceDataSet = [list(float(n) for n in x) for x in zip(*reduceDataSet)]
    #     for eachrow in range(len(reduceDataSet)):
    #         reduceDataSet[eachrow].append(int(transdata[-1][eachrow]))
    #     reduceDataSet.insert(0,[row,reqFeatures,len(klist)])

    if mrmrCProgress < 100.0:
        mrmrCProgress = 100.0
        if app is not None:
            app.updateProgress('%.1f %%' % mrmrCProgress)
    return reduceDataSet



# Calculate and return Mutual information between two random variables
def mutual_information(x_arr, y_arr, log_base=2):
    if len(x_arr) != len(y_arr):
        print "Data for MI cannot have irregular dimensions"
    # Variable to return MI
    mi_value = 0.0
    # Get uniques values of random variables
    values_x = set(x_arr)
    values_y = set(y_arr)
    # For each random
    for value_x in values_x:
        for value_y in values_y:
            px = shape(where(x_arr == value_x))[1] / len(x_arr)
            py = shape(where(y_arr == value_y))[1] / len(y_arr)
            pxy = len(where(in1d(where(x_arr == value_x)[0],
                                 where(y_arr == value_y)[0]) == True)[0]) / len(y_arr)
            if pxy > 0.0:
                mi_value += pxy * math.log((pxy / (px * py)), log_base)
            # print '(%d,%d) px:%f py:%f pxy:%f' % (value_x, value_y, px, py, pxy)
    return mi_value


def mrmrMutualInformation(data, reqFeatures = -1, app=None):
    mrmrDProgress = 0.0
    if app is not None:
        app.updateProgress('mRMR with MID started')
    dataSet = []  # For a local copy of data
    for eachrow in data[1:]:
        dataSet.append([int(elem) for elem in eachrow])
    row = int(data[0][0])
    dataSet = [list(x) for x in zip(*dataSet)]  # Transposing data
    dataSet =array(dataSet)  # Taking to vector form
    mrmrDProgress += 5.0
    if app is not  None:
        app.updateProgress('%.1f %%' % mrmrDProgress)

    miScoreOfeachG = {}
    # Calculate the mutual Info score for each attribute with the class
    for gi in range(len(data[1])-1):
        miScoreOfeachG[gi] = mutual_information(dataSet[gi], dataSet[-1], 2)
        mrmrDProgress += 35.0/(len(data[1])-1)
        if app is not None:
            app.updateProgress('%.1f %%' % mrmrDProgress)

    maxMIScore = max(miScoreOfeachG, key=lambda k: miScoreOfeachG[k])
    # print 'maxMIScore : ',maxMIScore
    selectedfeatures = []
    selectedfeatures.append(maxMIScore)
    nonselectedfeatures = list(set(miScoreOfeachG.keys())-{maxMIScore})
    # print miScoreOfeachG
    # print nonselectedfeatures
    transdata = [list (float(n) for n in x) for x in zip(*data[1:])]
    # sigmaMIval stores the value of sig(mutual Info) for any (gi) with all other gj's in incremental way
    sigmaMIval ={}
    reduceDataSet = [[0, 0, 0]]
    featureCount = 1
    # These variables help in optimal selection
    # tempRedData = []
    # classAcc = {'knn': 0.0, 'svm': 0.0}
    oldClassAcc = {'knn': 0.0, 'nb': 0.0}
    while True:
        funcval = -10.0; gi = -2
        prevFeature = selectedfeatures[-1]
        for giNs in nonselectedfeatures:
            if sigmaMIval.has_key(giNs):
                sigmaMIval[giNs] += mutual_information(dataSet[giNs], dataSet[prevFeature])
            else:
                sigmaMIval[giNs] = mutual_information(dataSet[giNs], dataSet[prevFeature])
            # print fcount,' : ',sigmaMIval

            if (miScoreOfeachG[giNs] - (sigmaMIval[giNs] / len(selectedfeatures))) > funcval:
                funcval = miScoreOfeachG[giNs] - (sigmaMIval[giNs] / len(selectedfeatures))
                gi = giNs
        if gi != -2:
            selectedfeatures.append(gi)
            featureCount += 1
            nonselectedfeatures.remove(gi)
            del sigmaMIval[gi]
        # Saving the current DataSet Making the next reducedDataSet
        tempRedData = copy.deepcopy(reduceDataSet)
        reduceDataSet[0] = [row, featureCount, int(data[0][2])]
        if len(reduceDataSet) == 1:
            for si in range(row):
                # To insert the first feature(maxfTest)
                reduceDataSet.append([transdata[selectedfeatures[0]][si], int(transdata[-1][si])])
        # print transdata
        # print reduceDataSet
        for si in range(1, row + 1):
            # print selectedfeatures
            # print transdata
            reduceDataSet[si].insert(-1, float(transdata[selectedfeatures[-1]][si - 1]))
            # print reduceDataSet
        if reqFeatures == 0:
            # print featureCount, '---'
            # print 'tData : ', tempRedData
            # print 'rData : ', reduceDataSet
            classAcc = classifyData(reduceDataSet, 0.7, None, True)
            # print classAcc, ' : ', oldClassAcc
            # print '--------------------------'
            if classAcc['knn'] > oldClassAcc['knn'] or classAcc['nb'] > oldClassAcc['nb']:
                # print reduceDataSet
                oldClassAcc['knn'] = classAcc['knn']
                oldClassAcc['nb'] = classAcc['nb']
                # pass
            elif classAcc['knn'] > 90.0 and classAcc['nb'] > 90.0:
                oldClassAcc['knn'] = classAcc['knn']
                oldClassAcc['nb'] = classAcc['nb']
            else:
                # print classAcc,' : ', oldClassAcc,' : ',selectedfeatures[-1],' rejected'
                featureCount -= 1
                reduceDataSet = tempRedData
            if len(selectedfeatures) == int(data[0][1]):
                break
        if app is not None:
            if reqFeatures > 0:
                mrmrDProgress += 60.0 / (reqFeatures - 1)
                app.updateProgress('%.1f %%' % mrmrDProgress)
            else:
                app.updateProgress('%d Features Added' % featureCount)
        # else:
        #     print 'wtf'
        if reqFeatures != 0 and featureCount == reqFeatures:
            break

    # print 'selectedfeatures : ', selectedfeatures, len(selectedfeatures)
    # print 'nonselectedfeaturelist : ',nonselectedfeatures, len(nonselectedfeatures)
    # reduceDataSet = []
    # for si in selectedfeatures:
    #     reduceDataSet.append(dataSet[si])
    # reduceDataSet.append(dataSet[-1])
    # reduceDataSet = [list(n for n in x) for x in zip(*reduceDataSet)]
    # reduceDataSet.insert(0, [int(data[0][0]), reqFeatures, int(data[0][2])])
    if mrmrDProgress < 100.0:
        mrmrDProgress = 100.0
        if app is not None:
            app.updateProgress('%.1f %%' % mrmrDProgress)
    # print reduceDataSet
    return reduceDataSet



# myList = [[0, 0, -2, -2, -2, 2, 0, -2, 2, -2, -2],
#           [0, 0, 2, 2, 4, 4, 0, 0, 4, 2, 0, 4],
#           [7, 8, 8, 8, 7, 7, 0, 8, 0, 0, 8, 7]]
# alist = [myList[1],
#          myList[2]]
# data = array(alist)
# print mutual_information(data[0], data[-1],2)