import numpy as np
from sklearn import linear_model
import os.path

def localProcess(symbol,Index,infoDir):
    fileName = infoDir+"\\"+symbol+"_"+`Index`+".csv"
    if not os.path.isfile(fileName):
        return ([],[],[],[])
    L = map(lambda x:x.rstrip(),open(fileName,'r').readlines())
    local_X3= []
    local_Y_volume,local_Y_maxmin,local_Y_closeopen = [],[],[]
    allX = []
    #Normalizers
    allY_Volume = []
    allY_Price = []
    for line in L:
        localLine = line.rstrip()[:-1].split(",")
        #print localLine
        localNumList = map(lambda x:float(x),localLine)
        allX.append(localNumList[1])
        #include all days, need to not include first 2 day
        local_Y_volume.append(localNumList[6])
        local_Y_maxmin.append(localNumList[3]-localNumList[4])
        local_Y_closeopen.append(localNumList[5]-localNumList[2])
    local_Y_volume = local_Y_volume[3:]
    local_Y_maxmin = local_Y_maxmin[3:]
    local_Y_closeopen = local_Y_closeopen[3:]
    mean_X,std_X = np.mean(allX),np.std(allX)
    
    for i in range(3,len(allX)):
        tmpXList = [allX[i-3],allX[i-2],allX[i-1]]
        tmpXList = list((np.array(tmpXList) - mean_X)/std_X)
        local_X3.append(tmpXList+[1.0])
    
    local_Y_volume = list((np.array(local_Y_volume) - np.mean(local_Y_volume))/np.std(local_Y_volume))
    local_Y_maxmin = list((np.array(local_Y_maxmin) - np.mean(local_Y_maxmin))/np.std(local_Y_maxmin))
    local_Y_closeopen = list((np.array(local_Y_closeopen) - np.mean(local_Y_closeopen))/np.std(local_Y_closeopen))
    
    return (local_X3,local_Y_volume,local_Y_maxmin,local_Y_closeopen)

#Only work on LongName dataset
def buildMats(symbolFile,infoDir):
    #build Matrices
    #1,3,7-Day X (Google Trend)
    X_3day= []
    #Y: Normalized Volume = volume/avgVolume_in_3Month
    Y_normalizedVolume = []
    #Y: max-min ratio = (max-min)/avgPrice_in_3Month
    Y_maxminRatio = []
    #Y: close open ratio = (close - open)/avgPrice_in_3Month
    Y_closeopenRatio = []
    
    longSymbolList = open(symbolFile,"r").readlines()[0].split(",")[:-1]
    for symbol in longSymbolList:
        for timeIdx in range(12):
            #print symbol
            #print timeIdx
            #print infoDir
            local_X3,local_Y_volume,local_Y_maxmin,local_Y_closeopen = localProcess(symbol,timeIdx,infoDir)
            X_3day += (local_X3) 
            Y_normalizedVolume += local_Y_volume
            Y_maxminRatio += local_Y_maxmin
            Y_closeopenRatio += local_Y_closeopen
    X_3day = np.array(X_3day)
    Y_normalizedVolume = np.array(Y_normalizedVolume)
    Y_maxminRatio = np.array(Y_maxminRatio)
    Y_closeopenRatio = np.array(Y_closeopenRatio)
    
    weight_Volume = np.dot(np.dot(np.linalg.inv(np.dot(np.transpose(X_3day) , X_3day)) , np.transpose(X_3day)),Y_normalizedVolume)
    weight_MaxMin = np.dot(np.dot(np.linalg.inv(np.dot(np.transpose(X_3day) , X_3day)) , np.transpose(X_3day)),Y_maxminRatio)
    weight_CloseOpen = np.dot(np.dot(np.linalg.inv(np.dot(np.transpose(X_3day) , X_3day)) , np.transpose(X_3day)),Y_closeopenRatio)
    return (weight_Volume,weight_MaxMin,weight_CloseOpen,X_3day,Y_normalizedVolume,Y_maxminRatio,Y_closeopenRatio)

def list2str(L):
    outS = ""
    for i in L:
        outS+=`i`+","
    return outS
#same length    
def MeanAbsError(Y_pred,Y_true,fileName):
    Y_diff = np.array(Y_pred) - np.array(Y_true)
    with open(fileName,"a") as errorLog:
        errorLog.write(list2str(Y_diff))
    Y_absDiff = map(lambda x:abs(x),Y_diff)
    return np.mean(Y_absDiff)
    
weight_V,weight_MM,weight_CO,X,Y_V,Y_MM,Y_CO = buildMats("","")

print "weightV"+`weight_V`
print "weightMM"+`weight_MM`
print "weightCO"+`weight_CO`
import matplotlib.pyplot as plt
SelectedIndices = range(1,200000,200)
X_3Vec,Y_V_selected,Y_MM_selected,Y_CO_selected = X[SelectedIndices,:],Y_V[SelectedIndices],Y_MM[SelectedIndices],Y_CO[SelectedIndices]

Y_predicted_V = np.dot(X_3Vec,weight_V)
Y_predicted_MM = np.dot(X_3Vec,weight_MM)
Y_predicted_CO = np.dot(X_3Vec,weight_CO)

print MeanAbsError(Y_predicted_V,Y_V_selected,"./LR_error_V.txt")
print MeanAbsError(Y_predicted_MM,Y_MM_selected,"./LR_error_MM.txt")
print MeanAbsError(Y_predicted_CO,Y_CO_selected,"./LR_error_CO.txt")

X_selected = X_3Vec[:,2]
X_indexList = [i[0] for i in sorted(enumerate(X_selected), key=lambda x_tmp:x_tmp[1])]
X_sorted,Y_V_sorted,Y_MM_sorted,Y_CO_sorted = X_selected[X_indexList],Y_predicted_V[X_indexList],Y_predicted_MM[X_indexList],Y_predicted_CO[X_indexList]
