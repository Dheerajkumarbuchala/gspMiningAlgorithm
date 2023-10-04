import copy


def flatten(s):
    return sum(s,[]) if type(s[0]) is list else copy.deepcopy(s)

def seqLength(s):
    return len(flatten(s))

def seqSize(s):
    return len(s) if type(s[0]) is list else 1

def getMinMISValue(s, MS):
    s = flatten(s)
    minMIS = MS[s[0]]
    for item in s[1:]:
        if(MS[item] < minMIS):
            minMIS = MS[item]
    return minMIS

def firstItemValid(s, MS):
    seq = copy.deepcopy(s)
    if(type(seq[0]) is list):
        seq = sum(seq, [])
    
    firstItemMIS = MS[seq[0]]
    for item in seq[1:]:
        if(firstItemMIS >= MS[item]):
            return False
    return True

def firstItemJoin(s1, s2, MS, count, SDC, n):
    C = []
    flatS1 = flatten(s1)
    flatS2 = flatten(s2)
    flatS1Rem = copy.deepcopy(flatS1)
    flatS1Rem.pop(1)
    flatS2Rem = flatS2[:-1]
    
    if flatS1Rem == flatS2Rem and abs(count[f"[{flatS2[-1]}]"]/n- count[f"[{flatS1[1]}]"]/n) <= SDC and MS[flatS2[-1]]>= MS[flatS1[0]]:    
        if (type(s2[-1]) is list) and seqLength(s2[-1]) == 1: 
            if (type(s1[-1]) is int): 
                c1=[copy.deepcopy(s1), copy.deepcopy(s2[-1])]
                C.append(c1)    
            else: 
                c1=copy.deepcopy(s1)+[copy.deepcopy(s2[-1])]
                C.append(c1)  
            if seqLength(s1) == 2 and seqSize(s1) == 2 and flatS2[-1] > flatS1[-1]: 
                c2=copy.deepcopy(s1)
                c2[-1].extend(copy.deepcopy(s2[-1]))
                C.append(c2)
        elif (seqSize(s1) == 1 and seqLength(s1) == 2 and flatS2[-1] > flatS1[-1]) or seqLength(s1) > 2:               
            if type(s1[-1]) is int:
                c2=copy.deepcopy(s1)
                c2.append(s2[-1])
                C.append(c2)                   
            else:
                last=copy.deepcopy(s2[-1])
                item = last[-1] if type(last) is list else last
                c2=copy.deepcopy(s1)
                c2[-1].append(item)                    
                C.append(c2)

    return C

def lastItemValid(s, MS):
    seq = copy.deepcopy(s)
    if(type(seq[0]) is list):
        seq = sum(seq, [])
    
    lastItemMIS = MS[seq[-1]]
    for item in seq[:-1]:
        if(lastItemMIS >= MS[item]):
            return False
    return True

def lastItemJoin(s1, s2, MS, count, SDC, n):
    C = []
    flatS1=flatten(s1)
    flatS2=flatten(s2)
    firstS1 = flatS1[0]
    firstS2 = flatS2[0]
    firstS1MIS = MS[firstS1]
    lastS2MIS = MS[flatS2[-1]]
    popped = flatS1.pop(0)
    secondLastS2=flatS2.pop(-2)
    if flatS1 == flatS2 and abs(float(count[f"[{popped}]"]/n)-float((count[f"[{secondLastS2}]"]/n))) <= SDC and lastS2MIS < firstS1MIS :
        if type(s1[0]) is list and len(s1[0]) == 1:
                if type(s2[0]) is int: 
                    c1=[copy.deepcopy(s1[0]), copy.deepcopy(s2)]
                    C.append(c1)                                     
                else:
                    c1 = copy.deepcopy(s2)
                    c1.insert(0, copy.deepcopy(s1[0]))
                    C.append(c1)                  
                if seqLength(s2)==2 and seqSize(s2)==2 and firstS1<firstS2:
                    c1=copy.deepcopy(s2)
                    c1[0].insert(0,copy.deepcopy(s1[0][0]))
                    C.append(c1)             
        elif (seqLength(s2) == 2 and seqSize(s2) == 1 and firstS1<firstS2) or seqLength(s2)>2:
            if type(s2[0]) is int:
                c1=copy.deepcopy(s2)
                c1.insert(0,copy.deepcopy(s1[0]))
                C.append(c1)                
            else:
                item = copy.deepcopy(s1[0][0]) if type(s1[0]) is list else copy.deepcopy(s1[0])                 
                c1=copy.deepcopy(s2)
                c1[0].insert(0,item)
                C.append(c1)
    return C




def GSPJoinStep(s1, s2, MS, count, SDC, n):
    C = []
    flatS1 = flatten(s1)
    flatS2 = flatten(s2)
    flatS1Rem = flatS1[1:]
    flatS2Rem = flatS2[:-1]
    if flatS1Rem == flatS2Rem and abs(float(count[f"[{flatS1[0]}]"]/n)-float((count[f"[{flatS2[-1]}]"]/n)))<=SDC:
        lastItem=copy.deepcopy(s2[-1])
        if type(lastItem) is list and len(lastItem)==1:
            if type(s1[0]) is int:                    
                C.append([copy.deepcopy(s1), copy.deepcopy(s2[-1])])
            else:                    
                c1=copy.deepcopy(s1)
                c1.append(copy.deepcopy(s2[-1]))
                C.append(c1)                    
        else:
            if type(s1[0]) is int:
                item = lastItem[-1] if type(lastItem) is list else lastItem
                c2=copy.deepcopy(s1)
                c2.append(item)
                C.append(c2)                                        
            else:
                item = lastItem[-1] if type(lastItem) is list else lastItem
                c2=copy.deepcopy(s1)
                c2[-1].append(item)
                C.append(c2)
    return C

    

def pruneCandidates(C, MS, F):
    C = copy.deepcopy(C)
    for k in C:
        kMinMIS = getMinMISValue(k, MS)
        if(type(k[0]) is list):
            for idx1 in range(len(k)):
                for idx2 in range(len(k[idx1])):
                    c = copy.deepcopy(k)
                    if len(k[idx1]) == 1:
                        c.remove(k[idx1])
                        if len(c) == 1:
                            c = c[0]
                    else:
                        c[idx1].remove(k[idx1][idx2])
                    cMIS = getMinMISValue(c, MS)
                    if(cMIS == kMinMIS):
                        if(c not in F):
                            try:
                                C.remove(k)
                            except:
                                pass
        else:
            for idx in range(len(k)):
                c = copy.deepcopy(k)
                c.remove(c[idx])
                cMIS = getMinMISValue(c, MS)
                if(cMIS == kMinMIS):
                    if(c not in F):
                        try:
                            C.remove(k)
                        except:
                            pass


    return C