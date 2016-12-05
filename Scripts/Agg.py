import os

#extractAllSymbol from GoogleTrend files, and write it to a txt
def extractAllSymbol(dirGTrend):
    ListNames = os.listdir(dirGTrend)
    
    def extractName(s):
        for i in range(len(s)):
            if s[i]<='9' and s[i]>='0':
                return s[:i]
        return s
    ListSymbols = map(lambda x:extractName(x),ListNames)
    M = {}
    for sym in ListSymbols:
        M[sym] = 1
    return sorted(list(M))

def listToStr(L):
    outS = ""
    for a in L:
        outS = outS+a+","
    return outS

#For a given symbol, loop over its trade days in [2010,2012],
#grab corresponding trading information and google trend info
def symbolCompile(symbol,timeIdx,dirGTrend,dirSP500,outDir):
    SP500Filename = dirSP500+"\\table_"+symbol+".csv"
    SP500Lines = map(lambda x:x.rstrip(),open(SP500Filename,'r').readlines())

    GTrendFilename = dirGTrend+"/" + symbol + `timeIdx` +".csv"
    GTrendLines = map(lambda x:x.rstrip(),open(GTrendFilename,'r').readlines()[3:])

    outFileName = outDir+"/"+symbol+"_"+`timeIdx`+".csv"

    SPIdx,GTrendIdx = 0,0
    while (SPIdx < len(SP500Lines) and GTrendIdx < len(GTrendLines)):
        curSP500List = SP500Lines[SPIdx].split(",")
        curGTrendList = GTrendLines[GTrendIdx].split(",")
        curGTrendList[0] = curGTrendList[0].replace("-","")
        if curSP500List[0]<curGTrendList[0]:
            SPIdx+=1
        elif curSP500List[0]>curGTrendList[0]:
            GTrendIdx+=1
        else:
            #they are equal, try to merge information
            mergeInfoList = curGTrendList + curSP500List[2:]
            with open(outFileName,'a') as wFile:
                wFile.write(listToStr(mergeInfoList))
                wFile.write("\n")
            SPIdx+=1
            GTrendIdx+=1

def allSymbolMerge(symbolFileName,dirGTrend,dirSP500,outDir):
    SymbolList = open(symbolFileName,'r').readlines()[0].split(',')[:-1]
    for symbol in SymbolList:
        for timeIdx in range(12):
            symbolCompile(symbol,timeIdx,dirGTrend,dirSP500,outDir)

    
    
