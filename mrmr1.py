import re
from pearson_coeff import *

# Open the data file
fid = open("colon", "r+")
# fid = open("file.txt", "r+")
# Read the data line wise and store in 2-D list
data = []
while True :
    line = fid.readline().strip()
    if line == '':
        break
    else:
        data.append(re.findall(r"[-]?\d*\.\d+|[-]?\d+", line))
# Close opened file
fid.close()

# h = classification variable
# gi = gene variable
# klist = list of classes available(k), ksize = size of kth class(is not nk, no of rows having k)
# n = sum of all nk, ksum = sum of all gi of some particular k
# kvar = variance of kth class, var = overall variance
# gbar = mean of all gi for each i(col), gkbar = mean of all gi for each k(class)
# ftestval = value of ftest function for each gi

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

# find the pooled variance = var (for all classes)
# nk = size of each class x features in each col( = col)
var = 0
for i in klist:
    var += float((ksize[i]-1)*kvar[i])
var /= float(row - len(klist))

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

# For F-Test function calculation
for gi in xrange(col):
    tsum = float(0.0)
    # print '\n\ngi : ', gi
    for ki in klist:
        tsum += (((ksize[ki])*(gkbar[gi][ki]-gbar[gi])**2)/(row-1))
    #     print (((ksize[ki])*(gkbar[gi][ki]-gbar[gi])**2)/(row-1))
    #     print 'ki : ', ki
    #     print 'ksize[ki] : ', ksize[ki]
    #     print 'gkbar[gi][ki] : ', gkbar[gi][ki]
    #     print 'gbar[gi] : ', gbar[gi]
    #     #print 'ksize[ki] : ', ksize[ki]
    #     print 'tsum : %f' % tsum
    # print 'var : ', var
    ftestval[gi] = float(tsum/var)


# print 'gbar : ', gbar
# print 'gkbar :', gkbar
# print 'klist : ', klist
# print 'ksize : ', ksize
# print 'ksum : ', ksum
# print 'kvar : ', kvar
# print 'var : ', var
print 'ftestval : ', ftestval

# maxftestval stores the feature with maxvalue of f-Test which starts the algo as first
# selected feature
# selectedfeatures stores the list of features selected as set of reduced features
# nonselectedfeatures stores the list of features not selected yet
# corr_coef stores the value of correlation coefficient for any (gi,gj) pair in dictionary way
maxftestval = max(ftestval, key=lambda k: ftestval[k])
print 'maxftestval : ',maxftestval
selectedfeatures = []
selectedfeatures.append(maxftestval)
nonselectedfeatures = list(set(ftestval.keys())-{maxftestval})
print 'nonselectedfeaturelist : ',nonselectedfeatures
# data matrix is transposed to align it feature wise not sample wise
transdata = [list(float(n) for n in x) for x in zip(*data[1:])]
corr_coef = {}
reqFeatures = 500
counter = 1
# for fcount in range(1,reqFeatures):
#     # funcval and gi store the maximum value to select the best suitable gi every cycle
#     funcval = -10.0; gi = -2
#     for giNs in nonselectedfeatures:
#         sigmacorval = 0.0
#         for gjS in selectedfeatures:
#             counter += 1
#             if corr_coef.has_key('%d+%d' % (giNs, gjS)):
#                 sigmacorval += corr_coef['%d+%d' % (giNs, gjS)]
#             elif corr_coef.has_key('%d+%d' % (gjS, giNs)):
#                 sigmacorval += corr_coef['%d+%d' % (gjS, giNs)]
#             else:
#                 corr_coef['%d+%d'%(giNs,gjS)] = pearson_coefficient(row, transdata[giNs], transdata[gjS])
#                 sigmacorval += corr_coef['%d+%d'%(giNs,gjS)]
#             #print 'giNs:',giNs,'  gjS:',gjS,
#         sigmacorval /= len(selectedfeatures)
#         #print ''
#         #print '  sigmaCorr:',sigmacorval,
#         #print 'decide:', ftestval[giNs] - sigmacorval
#         if (ftestval[giNs] - sigmacorval) > funcval:
#             funcval = ftestval[giNs] - sigmacorval
#             gi = giNs
#     if gi != -2:
#         selectedfeatures.append(gi)
#         nonselectedfeatures.remove(gi)

sigmacorval = {}
for fcount in range(1,reqFeatures):
    funcval = -10.0; gi = -2
    prevFeature = selectedfeatures[-1]
    for giNs in nonselectedfeatures:
        if sigmacorval.has_key(giNs):
            sigmacorval[giNs] += pearson_coefficient(row,transdata[giNs],transdata[prevFeature])
        else:
            sigmacorval[giNs] = pearson_coefficient(row,transdata[giNs],transdata[prevFeature])
        if (ftestval[giNs] - (sigmacorval[giNs]/len(selectedfeatures))) > funcval:
            funcval = ftestval[giNs] - (sigmacorval[giNs]/len(selectedfeatures))
            gi = giNs
        counter += 1
    if gi != -2:
        selectedfeatures.append(gi)
        nonselectedfeatures.remove(gi)
        del sigmacorval[gi]

print 'selectedfeatures : ',selectedfeatures, len(selectedfeatures)
print 'nonselectedfeaturelist : ',nonselectedfeatures, len(nonselectedfeatures)
print counter