import re

def read_data_file(data_file):
    sequences = [] # List to store the sequences
    file = open(data_file, 'r')
    for i in file:
        sequence = re.findall(r'\d+', i)
        sequences.append([int(num) for num in sequence])
    return sequences

def read_parameter_file(parameter_file):
    mis_values_dict = {}
    sdc = 0
    file = open(parameter_file, 'r')
    for i in file:
        if i.startswith('MIS'):
            pattern = r'[-+]?\d*\.\d+|\d+'
            res = re.findall(pattern, i)
            mis_values_dict[int(res[0])] = float(res[1])
        elif i.startswith('SDC'):
            pattern = "\d+\.\d+"
            sdc = re.findall(pattern, i)
            print("SDC before transformation : ", sdc)
            for j in range(len(sdc)):
                sdc[j] = float(sdc[j])
            print("SDC after transformation : ", sdc)
    return mis_values_dict, sdc


def data_extraction(data_file, parameter_file, output_file):
    # read the raw data provided in the file and transform into usable data
    data = read_data_file(data_file)
    #print(data)
    data_mis , sdc_value = read_parameter_file(parameter_file)
    print("MIS Values : ", data_mis)
    print("SDC Value : ", sdc_value)

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