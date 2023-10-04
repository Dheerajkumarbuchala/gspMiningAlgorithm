from utils import getDataFromFile, isCandidateSubsequence, displayCounts
from generators import level2CandGen, MSCandGen
import copy

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
    print("M:", M)

    #Init Pass
    L, count = initPass(S, MS, M)
    print("L:", L)
    F = {}
    F[1] = [[l] for l in L if count[f"[{l}]"]/n >= MS[l]]
    displayCounts(F[1], count, 1)
    k=2
    while(len(F[k-1]) > 0):
        if(k == 2):
            #Level 2 Candidate Generation
            Ck = level2CandGen(L, MS, count, SDC, n)
            pass

        else:
            #MS Candidate Generation Function
            Ck = []
            pass
        #print(f"C{k}:", Ck)
        #SubSequence Check
        #print(f"Count for 20,20", count["[[20], [20]]"])
        for s in S.values():
            for c in Ck:
                key = str(c)
                #print(key)
                if(not(key in count.keys())):
                        count[key]=0
                if(isCandidateSubsequence(c,s)):
                    if(key == '[[40], [40]]'):
                        print("Found in ", s)
                    count[key]+=1
        # print(f"Count after k={k}:", count)
        
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
            
        displayCounts(F[k], count, k)    
        
        
        k+=1
    
    

    

if __name__ == "__main__":
    #Read the file and get the data
    #GSP

    sequences, MIS, SDC = getDataFromFile("data/data-1.txt", "data/para1-1.txt")
    # print("Sequences:", sequences)
    # print("Length: ", len(sequences))
    # print("MIS Values:",MIS)
    MSGSP(sequences, MIS, SDC)
