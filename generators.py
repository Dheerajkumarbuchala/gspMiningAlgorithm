import copy
from genUtils import firstItemValid, firstItemJoin, lastItemValid, lastItemJoin, GSPJoinStep, pruneCandidates

def level2CandGen(L, MS, count, SDC, n):
    C = []
    freqItems = copy.deepcopy(L)
    for idx1 in range(len(freqItems)):
        if(count[f"[{L[idx1]}]"] >= MS[L[idx1]]):
            for idx2 in range(len(freqItems)):
                item1 = freqItems[idx1]
                item2 = freqItems[idx2]
                item1Support = count[f"[{item1}]"]/n
                item2Support = count[f"[{item2}]"]/n
                isSatifySupport = (count[f"[{item2}]"] >= MS[item1])
                absDiff = abs(item1Support - item2Support) <= SDC
                if(isSatifySupport and absDiff):
                    if(item1 != item2) and (item1 < item2):
                        C.append([item1, item2])
                    C.append([[item1], [item2]])
    return C

def MSCandGen(F, MS, SDC, count, n):
    # Join Step
    for s1 in F:
        for s2 in F:
            if(firstItemValid(s1, MS)):
                firstItemJoin(s1, s2, MS)
            #If
            #ElseIf
            #Else
            break

    #Pruning 
    return []

# Line 7 - MS_Candidate-gen-SPM function
def MS_Candidate_gen_SPM(F,Count_L,SDC,MS,n):
    count = Count_L
    C=[]   
    for s1 in F:
        for s2 in F:            
            if firstItemValid(s1, MS):
                C.extend(firstItemJoin(s1, s2, MS, count, SDC, n))
            elif lastItemValid(s2,MS):
                C.extend(lastItemJoin(s1, s2, MS, count, SDC, n))
            else:
                C.extend(GSPJoinStep(s1, s2, MS, count, SDC, n))  
    duplicateIdx=[]
    for i in range(0, len(C)-1):
        for j in range(i+1, len(C)-2):
            if C[i] == C[j]:
                duplicateIdx.append(i)
    for i in duplicateIdx:
        C.pop(i)               
    # for k in C:
    #     if not prune(k,MS,F):
    #         C.remove(k)
    C = pruneCandidates(C, MS, F)
    return C

