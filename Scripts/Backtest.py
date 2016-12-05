import numpy as np
import os.path

def localProcess_NoZ(symbol,Index,infoDir):
    fileName = infoDir+"\\"+symbol+"_"+`Index`+".csv"
    if not os.path.isfile(fileName):
        return ([],[],[],[],[])
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
    
    raw_CO = []
    for i in local_Y_closeopen:
        raw_CO.append(i)
    
    
    #print local_Y_closeopen
    return (local_X3,local_Y_volume,local_Y_maxmin,local_Y_closeopen,raw_CO)

def localProcess(symbol,Index,infoDir):
    fileName = infoDir+"\\"+symbol+"_"+`Index`+".csv"
    if not os.path.isfile(fileName):
        return ([],[],[],[],[])
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
    
    raw_CO = []
    for i in local_Y_closeopen:
        raw_CO.append(i)
    
    local_Y_volume = list((np.array(local_Y_volume) - np.mean(local_Y_volume))/np.std(local_Y_volume))
    local_Y_maxmin = list((np.array(local_Y_maxmin) - np.mean(local_Y_maxmin))/np.std(local_Y_maxmin))
    local_Y_closeopen = list((np.array(local_Y_closeopen) - np.mean(local_Y_closeopen))/np.std(local_Y_closeopen))
    
    return (local_X3,local_Y_volume,local_Y_maxmin,local_Y_closeopen,raw_CO)
    
#train regression using index [0,7]
def trainWeight(symbol,infoDir):
    trainX = []
    train_Y_V,train_Y_MM,train_Y_CO = [],[],[]
    for i in range(8):
        local_X3,local_Y_V,local_Y_MM,local_Y_CO,raw_CO = localProcess(symbol,i,infoDir)
        trainX += local_X3
        train_Y_V+=local_Y_V
        train_Y_MM+= local_Y_MM
        train_Y_CO+= local_Y_CO
    trainX,train_Y_MM,train_Y_CO= np.array(trainX),np.array(train_Y_MM),np.array(train_Y_CO)
    weight_V = np.dot(np.dot(np.linalg.inv(np.dot(np.transpose(trainX) , trainX)) , np.transpose(trainX)),train_Y_V)
    weight_MaxMin = np.dot(np.dot(np.linalg.inv(np.dot(np.transpose(trainX) , trainX)) , np.transpose(trainX)),train_Y_MM)
    weight_CloseOpen = np.dot(np.dot(np.linalg.inv(np.dot(np.transpose(trainX) , trainX)) , np.transpose(trainX)),train_Y_CO)
        
    return (weight_V,weight_MaxMin, weight_CloseOpen)
    
def testWeight(symbol,infoDir,weight):
    curMoney = 1000
    moneyList = [curMoney]
    signalList = []
    resultList = []
    for i in range(8,12):
        local_X3,local_Y_V,local_Y_MM,local_Y_CO,raw_CO = localProcess(symbol,i,infoDir)
        for localTrade in range(len(local_Y_CO)):
            #localSignal = genSignal(...), use appropriate genSignal function
            localSignal = 0
            signalList.append(localSignal)
            tradeQuantity = localSignal
            profit = tradeQuantity * raw_CO[localTrade]
            resultList.append(raw_CO)
            #print profit
            curMoney += profit
            moneyList.append(curMoney)
    return moneyList,raw_CO

def WinRatio(moneyTrajectory):
    win,n = 0,0
    for i in range(1,len(moneyTrajectory)):
        if moneyTrajectory[i]>moneyTrajectory[i-1]:
            win+=1
        n+=1
    return float(win)/n

def sharpeRatio(moneyTrajectory,initMoney):
    return (moneyTrajectory[-1] - initMoney)/np.std(moneyTrajectory)

import matplotlib.pyplot as plt
def Backtest(symbol,infoDir):
    weight_V, weight_MM , weight_CO = trainWeight(symbol,infoDir)
    moneyTrajectory,raw_CO = testWeight(symbol,infoDir,weight_CO)
    
    return moneyTrajectory,raw_CO

def batchBacktest(allSymbolFilename,infoDir):
    A = open(allSymbolFilename,'r').readlines()[0].split(",")[:-1]
    allMoneyList,allSharpeList = [],[]
    goodSymbolList = []
    goodSharpeList = []
    goodWinProb = []
    minLen = 200
    
    traj_superposition = [0.0] * minLen
    for symbolName in A:
        localMoney,local_raw_CO = Backtest(symbolName,infoDir)
        localSharpe = sharpeRatio(localMoney,1000)
        allMoneyList.append(localMoney[-1])
        allSharpeList.append(localSharpe)
        if localSharpe > 2.0 and len(localMoney)>=minLen:
            goodSymbolList.append(symbolName)
            goodSharpeList.append(localSharpe)
            goodWinProb.append(WinRatio(localMoney))
            
            for i in range(minLen):
                traj_superposition[i] += localMoney[i]
    
    print traj_superposition
    print "superposed sharpe ratio"+`(traj_superposition[-1] - traj_superposition[0])/np.std(traj_superposition)`
    
    plt.plot(range(minLen),traj_superposition)
    plt.xlabel("time")
    plt.ylabel("money")
    plt.show()            
