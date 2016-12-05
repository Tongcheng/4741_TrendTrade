import os
from shutil import copyfile

def filterLen(srcDir,dstDir):
    csvNameList = os.listdir(srcDir)
    for csvName in csvNameList:
        contentLen = len(open(srcDir+"\\"+csvName,'r').readlines())
        if contentLen > 55 and contentLen < 70:
            
            copyfile(srcDir+"\\"+csvName,dstDir+"\\"+csvName)
            
def filterToLongname(srcDir,dstDir):
    csvNameList = os.listdir(srcDir)
    for csvName in csvNameList:
        symbolName = csvName.split("_")[0]
        if len(symbolName)>=3:
            copyfile(srcDir+"\\"+csvName,dstDir+"\\"+csvName)

