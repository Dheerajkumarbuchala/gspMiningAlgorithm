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