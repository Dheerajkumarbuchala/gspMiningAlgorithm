import copy

def getDataFromFile(dataFilePath, misFilePath):
    sequences = {}
    MIS = {}
    SDC = None;
    #Extracting sequences from the data file
    with open(dataFilePath) as dataFile:
        rawFileData = dataFile.read()
        rowIdx = 1
        for row in rawFileData.split("\n"):
            sequences[rowIdx] = []
            row = row[1:-1]
            fileSequences = row.split("{")
            for seq in fileSequences:
                if(seq != ""):
                    if("}" in seq):
                        seq = seq[:-1]
                    seqArr = list(map(int, seq.split(',')))
                    sequences[rowIdx].append(seqArr)
            rowIdx+=1
        

    #Extracting MIS values from MIS file
    with open(misFilePath) as misFile:
        rawFileData = misFile.read()
        for row in rawFileData.split("\n"):
            misString, misValueString = row.split("=")
            misString = misString.strip()
            misValueString = misValueString.strip()
            key = None
            if(misString == "SDC"):
                key = 'SDC'
            else:
                key = int(misString[4:-1])
            value = float(misValueString)
            if(key == "SDC"):
                SDC = value
            else:
                MIS[key] = value

    return sequences, MIS, SDC

def isCandidateSubsequence(c,s):
    #Converting to list of list for consistency
    seq = copy.deepcopy(s)
    if type(c[0]) is int:
      c=[c]
    ignoreIdx = []
    successCounter = 0
    startFrom = 0
    for item in c:
        if len(item)== len(set(item)):
            for i in range(startFrom, len(seq)):
                if(i not in ignoreIdx):
                    if set(item).issubset(set(seq[i])):
                        ignoreIdx.append(i)
                        successCounter+=1
                        startFrom = i+1
                        break
    return successCounter == len(c)
    

        
def displayCounts(F, count, k):
    print(f"**** k = {k} *******")
    for f in F:
        print(f"{f} = {count[str(f)]}")

    print(f"Total Count: {len(F)}")
    