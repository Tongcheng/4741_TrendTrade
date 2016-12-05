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

def list2str(L):
    outS = ""
    for i in L:
        outS+=`i`+","
    return outS

#same length    
def MeanAbsError(Y_pred,Y_true):
    Y_diff = np.array(Y_pred) - np.array(Y_true)
    Y_absDiff = map(lambda x:abs(x),Y_diff)
    return np.mean(Y_absDiff)

#Only work on LongName dataset
def buildMats(symbolFile,infoDir):
    longSymbolList = open(symbolFile,"r").readlines()[0].split(",")[:-1]
    for symbol in longSymbolList:
        #build Matrices
        #1,3,7-Day X (Google Trend)
        X_3day= []
        #Y: Normalized Volume = volume/avgVolume_in_3Month
        Y_normalizedVolume = []
        #Y: max-min ratio = (max-min)/avgPrice_in_3Month
        Y_maxminRatio = []
        #Y: close open ratio = (close - open)/avgPrice_in_3Month
        Y_closeopenRatio = []
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
        Y_predicted_V = np.dot(X_3day,weight_Volume)
        Y_predicted_MM = np.dot(X_3day,weight_MaxMin)
        Y_predicted_CO = np.dot(X_3day,weight_CloseOpen)
        score_V = MeanAbsError(Y_predicted_V,Y_normalizedVolume)
        score_MM = MeanAbsError(Y_predicted_MM,Y_maxminRatio)
        score_CO = MeanAbsError(Y_predicted_CO,Y_closeopenRatio)
        with open(".\individualScores.csv",'a') as wFile:
            localStr = symbol+","+`score_V`+","+`score_MM`+","+`score_CO`+"\n"
            wFile.write(localStr)

                
