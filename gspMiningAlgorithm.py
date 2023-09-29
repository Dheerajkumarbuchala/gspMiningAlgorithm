import re

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
    print("Init pass count: ",count)
   
    master_data = {}
    M1 = list(map(lambda itemset: itemset[0], M))
    print("Init Pass Items: ", M1)
    master_MIS = MIS[M1[0]]
    print(M1)
    l = [M1[0]]
    for m in M1[1:]:
        try:
            if(count[m]/len(data) >= master_MIS):
                l.append(m)
        except:
            pass
    return l, count

def level2CandGen(L):
    pairs = []
    for idx1 in range(len(L)):
        for idx2 in range(idx1+1, len(L)):
                pairs.append([L[idx1], L[idx2]])

    return pairs



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
    L, count = init_pass(data, M, data_mis)
    print("List after initial pass : ", L)

    # F1
    f1 = []
    for item in L:
        print(f"item: {item} count: {count[item]} ratio:{count[item]/n} mis:{data_mis[item]}")
        if(count[item]/n >= data_mis[item]):
            f1.append(item)
    print("F-1 : ", f1)

    F = [f1]
    k = 2
    Ck = None
    #Main Loop
    while(len(F[k-2])>0):
        if(k==2):
            #Level 2 Candidate Generation
            Ck = level2CandGen(L)
        else:
            #MS Candidate Generation
            pass


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