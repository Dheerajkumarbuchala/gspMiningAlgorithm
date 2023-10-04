from utils import getDataFromFile, isCandidateSubsequence, displayCounts, writeResultToFile
from generators import level2CandGen, MSCandGen
import copy

DISPLAY_CONSOLE_OUTPUT = False

def initPass(S, MS, M):
    n = len(S)
    count = {}
    formatedCount = {}
    for item in M:
        count[item] = 0
        for seqList in S.values():
            searchSeq = []
            for seq in seqList:
                searchSeq.extend(seq)
            if(item in searchSeq):
                count[item]+=1

    masterMIS = None
    masterIdx = None
    for idx in range(len(M)):
        item = M[idx]
        if(count[item]/n >= MS[item]):
            masterMIS = MS[item]
            masterIdx = idx
            break
    L = []
    for item in M[masterIdx:]:
        
        if(item not in count.keys()):
            continue
        if(count[item]/n >= masterMIS):
            formatedCount[f"[{item}]"] = count[item]
            L.append(item)

    return L, formatedCount


def MSGSP(S, MS, SDC):
    n = len(S)
    #Sorting items according MIS value
    M = sorted(MS.keys(), key=lambda item: MS[item])
    #print("M:", M)

    #Init Pass
    L, count = initPass(S, MS, M)
    #print("L:", L)
    F = {}
    F[1] = [[l] for l in L if count[f"[{l}]"]/n >= MS[l]]
    displayCounts(F[1], count, 1) if DISPLAY_CONSOLE_OUTPUT else None
    writeResultToFile(F[1], count, 1, "w")
    k=2
    while(len(F[k-1]) > 0):
        if(k == 2):
            #Level 2 Candidate Generation
            Ck = level2CandGen(L, MS, count, SDC, n)

        else:
            #MS Candidate Generation Function
            Ck = MSCandGen(F[k-1], count, SDC, MS, n)
        
        for s in S.values():
            for c in Ck:
                key = str(c)
                if(not(key in count.keys())):
                        count[key]=0
                if(isCandidateSubsequence(c,s)):
                    count[key]+=1
        
        F[k] = []
        for c in Ck:
            cand = copy.deepcopy(c)
            if(type(c[0]) is list):
                c = sum(c,[])

            minMISValue = MS[c[0]]
            for item in c:
                if(MS[item] < minMISValue):
                    minMISValue = MS[item]

            if(count[str(cand)]/n)>=minMISValue:
                F[k].append(cand)
            
        displayCounts(F[k], count, k) if DISPLAY_CONSOLE_OUTPUT else None
        writeResultToFile(F[k], count, k, "a")
        k+=1
    
    

    

if __name__ == "__main__":
    sequences, MIS, SDC = getDataFromFile("data/data-1.txt", "data/para1-1.txt")
    MSGSP(sequences, MIS, SDC)
    print("Done")
