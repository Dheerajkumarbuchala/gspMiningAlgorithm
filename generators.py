def level2CandGen(L, MS, count, SDC, n):
    C = []
    freqItems = [l for l in L if count[f"[{l}]"]/n >= MS[l]]
    freqItems.sort()

    for idx1 in range(len(freqItems)):
        for idx2 in range(len(freqItems)):
            item1 = freqItems[idx1]
            item2 = freqItems[idx2]
            item1Support = count[f"[{item1}]"]/n
            item2Support = count[f"[{item2}]"]/n
            isSatifySupport = (item2Support >= MS[item1])
            absDiff = abs(item1Support - item2Support) <= SDC
            if(isSatifySupport and absDiff):
                if (item1!=item2) and (item2 < item1):
                    C.append([item1, item2])
                C.append([[item1], [item2]])
    print("Level 2 generated: ", len(C))   
    return C
    


def MSCandGen():
    pass