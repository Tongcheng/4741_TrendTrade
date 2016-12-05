import numpy as np
from sklearn import linear_model
import os.path
from statsmodels.regression.quantile_regression import QuantReg

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
    
    return (X_3day,Y_normalizedVolume,Y_maxminRatio,Y_closeopenRatio)

def QuantileRegression(X,Y,quantile):
    mod = QuantReg(Y,X)
    res = mod.fit(q=quantile)
    return res.params

X,Y_V,Y_MM,Y_CO = buildMats("","")

SelectedIndices = range(1,200000,200)
X_3Vec,Y_V_selected,Y_MM_selected,Y_CO_selected = X[SelectedIndices,:],Y_V[SelectedIndices],Y_MM[SelectedIndices],Y_CO[SelectedIndices]

import matplotlib.pyplot as plt

def plotQuantile_V(q,X,Y_V):
    weight_Q_V = QuantileRegression(X,Y_V,q)
    Y_predicted_V= np.dot(X_3Vec,weight_Q_V)
    X_selected = X_3Vec[:,2]
    X_indexList = [i[0] for i in sorted(enumerate(X_selected), key=lambda x_tmp:x_tmp[1])]
    X_sorted,Y_V_sorted= X_selected[X_indexList],Y_predicted_V[X_indexList]
    plt.plot(X_sorted,Y_V_sorted)
    
def plotQuantile_MM(q,X,Y_MM):
    weight_Q_MM = QuantileRegression(X,Y_MM,q)
    Y_predicted_MM= np.dot(X_3Vec,weight_Q_MM)
    X_selected = X_3Vec[:,2]
    X_indexList = [i[0] for i in sorted(enumerate(X_selected), key=lambda x_tmp:x_tmp[1])]
    X_sorted,Y_MM_sorted= X_selected[X_indexList],Y_predicted_MM[X_indexList]
    plt.plot(X_sorted,Y_MM_sorted)
    
def plotQuantile_CO(q,X,Y_CO):
    weight_Q_CO = QuantileRegression(X,Y_CO,q)
    Y_predicted_CO= np.dot(X_3Vec,weight_Q_CO)
    X_selected = X_3Vec[:,2]
    X_indexList = [i[0] for i in sorted(enumerate(X_selected), key=lambda x_tmp:x_tmp[1])]
    X_sorted,Y_CO_sorted= X_selected[X_indexList],Y_predicted_CO[X_indexList]
    plt.plot(X_sorted,Y_CO_sorted)
    
  
def plotQuantile(qList):   
    for q in qList:
        plotQuantile_V(q,X_3Vec,Y_V_selected)
    #plt.scatter(X_sorted,Y_V_sorted)
    plt.title("Volume Quantile Lines "+`qList[0]`+","+`qList[-1]`)
    plt.xlabel("Google Trend Z-score for 1 day before")
    plt.ylabel("Volume Traded Z-score")
    plt.show()
    
    for q in qList:
        plotQuantile_MM(q,X_3Vec,Y_MM_selected)
    #plt.scatter(X_sorted,Y_MM_sorted)
    plt.title("Max - Min daily price Quantile Lines "+`qList[0]`+","+`qList[-1]`)
    plt.xlabel("Google Trend Z-score for 1 day before")
    plt.ylabel("Max - Min daily price Traded Z-score")
    plt.show()
    
    for q in qList:
        plotQuantile_CO(q,X_3Vec,Y_CO_selected)
    #plt.scatter(X_sorted,Y_CO_sorted)
    plt.title("Close - Open daily price Quantile Lines "+`qList[0]`+","+`qList[-1]`)
    plt.xlabel("Google Trend Z-score for 1 day before")
    plt.ylabel("Close - Open daily price Traded Z-score")
    plt.show()
    
    
    
