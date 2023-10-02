import re
import copy

def read_data_file(data_file):
    sequences = [] # List to store the sequences
    file = open(data_file, 'r')
    for i in file:
        sequence = re.findall(r'\d+', i)
        sequences.append([int(num) for num in sequence])
    return sequences

def read_parameter_file(parameter_file):
    # Dictionary to store items and respective MIS values
    mis_values_dict = {}
    # Variable to store SDC value for other items
    sdc = 0

    file = open(parameter_file, 'r')

    for i in file:
        # Code to extract the MIS values of the items
        if i.startswith('MIS'):
            # Regex pattern to extract the numbers from the String
            pattern = r'[-+]?\d*\.\d+|\d+' 
            res = re.findall(pattern, i) # res -> is a list of two numbers
            # res[0] = item
            # res[1] = value
            mis_values_dict[int(res[0])] = float(res[1])
        # Code to extract the SDC value form the file
        elif i.startswith('SDC'):
            # Regex pattern to extract the SDC value from the String
            pattern = "\d+\.\d+"
            sdc = re.findall(pattern, i) # sdc -> is a list of string type elements
            print("SDC before transformation : ", sdc)
            # Transforming the type string to float
            for j in range(len(sdc)):
                sdc[j] = float(sdc[j])
            
            print("SDC after transformation : ", sdc)

    return mis_values_dict, sdc


def data_extraction(data_file, parameter_file, output_file):
    # read the raw data provided in the file and transform into usable data
    data = read_data_file(data_file)
    # print(data)
    data_mis , sdc_value = read_parameter_file(parameter_file)
    print("MIS Values : ", data_mis)
    print("SDC Value : ", sdc_value)

    gsp(data, data_mis, sdc_value, output_file)

def init_pass(data, M, MIS):
    count = {}
    for sequence in data:
        for item in sequence:
            if item not in count:
                count[item] = 1
            else:
                count[item] += 1
    print("[DEBUG] Init pass count: ",count)
   
    master_data = {}
    M1 = list(map(lambda itemset: itemset[0], M))
    print("[DEBUG] Init Pass Items: ", M1)
    master_MIS = MIS[M1[0]]
    l = [[M1[0]]]
    for m in M1[1:]:
        try:
            if(count[m]/len(data) >= master_MIS):
                l.append([m])
        except:
            pass
    return l, count

def level2CandGen(L):
    pairs = []
    for idx1 in range(len(L)):
        for idx2 in range(idx1+1, len(L)):
                pairs.append([L[idx1][0], L[idx2][0]])

    return pairs

#Checks if the C is subset of S
def isSubset(S,C):
    result = True # Assuming its a subset
    for c in C:
        if(not (c in S)):
            result = False # If the element is not preset in the S we change the value to False and break
            break
    return result

# Find the index of the element with least MIS value
def find_min_mis_idx(C, MIS):
    min_idx = 0
    for i in range(len(C)):
        if(MIS[C[i]] < MIS[C[min_idx]]):
            min_idx = i
    
    return min_idx
        

def gsp(data, data_mis, sdc_value, output_file):
    # Checking the recieved Data.
    # print("Data : ", data)
    # print("MIS Data : ", data_mis)
    # print("SDC : ", sdc_value)

    n = len(data)
    print("Length of the data : ", n)

    # M <- sort(I, MS)
    M =  sorted(data_mis.items(), key = lambda x : x[1])
    print("Sorted keys according to the MIS values : ", M)

    # L <- init-pass(M, S)
    print("\n#### Start INIT PASS #######")
    L, count = init_pass(data, M, data_mis)
    print("L: ", L)
    print("#### End INIT PASS #######")

    # F1
    print("\n#### Start F1 Calculation #######")
    f1 = []
    for item in L:

        print(f"[DEBUG] item: {item} count: {count[item[0]]} ratio:{count[item[0]]/n} mis:{data_mis[item[0]]}")
        if(count[item[0]]/n >= data_mis[item[0]]):
            f1.append(item)
    print("F-1 : ", f1)
    print("#### End F1 Calculation #######")
    F = [f1]
    k = 2
    Ck = None
    c_counts = {} # Dict to keep track of candidate counts
    min_mis = {} # Dict to keep track of min mis for each candidate
    #Main Loop
    while(len(F[k-2])>0):
        print(f"\n### Running K={k} ###")
        if(k==2):
            #Level 2 Candidate Generation
            Ck = level2CandGen(L)
            
        else:
            break
            #MS Candidate Generation
            pass
        print("Cand Gen Result: ", Ck)
        for s in data:
            for c in Ck:
                # Check is C is subset of S
                if(not (tuple(c) in c_counts.keys())):
                        c_counts[tuple(c)] = 0 #If candidate not found, intialize
                if(isSubset(s,c)):
                    c_counts[tuple(c)] += 1
                
                # Check is C(removed minMISItem) is a subset of S
                # print("[DEBUG] c: ",c)
                min_idx = find_min_mis_idx(c, data_mis) # Gets the index of min MIS Item
                # print("[DEBUG] min_idx: ", min_idx)
                min_mis[tuple(c)] = data_mis[c[min_idx]]
                # print("[DEBUG] min_mis value: ", min_mis[tuple(c)])
                c_w = copy.deepcopy(c) #C without min mis element
                c_w.pop(min_idx) # Remove the item form the list
                if(isSubset(s, c_w)):
                    if(not (tuple(c_w) in c_counts.keys())):
                        c_counts[tuple(c_w)] = 0 #If candidate not found, intialize
                    c_counts[tuple(c_w)] += 1
                
        print("[DEBUG] c_counts: ", c_counts)
        print("[DEBUG] min_mis: ", min_mis)

        #Create new entry for F for current K value
        F.append([])
        for c in Ck:
            if(c_counts[tuple(c)]/n >= min_mis[tuple(c)]):
                F[k-1].append(tuple(c))
        
        k+=1


if __name__ == "__main__":

    # Storing the data-file and parameter-file
    data_file = 'data/data-1.txt'
    parameter_file = 'data/para1-1.txt'
    
    # Checking the path 
    print("Data File : ")
    f1 = open(data_file,'r')
    print(f1.read())
    print()

    print("Parameter File : ")
    f2 = open(parameter_file,'r')
    print(f2.read())
    print()

    print("######## End Of Input File ########")

    # File to store the output
    output_file = 'data/output.txt'

    data_extraction(data_file, parameter_file, output_file)