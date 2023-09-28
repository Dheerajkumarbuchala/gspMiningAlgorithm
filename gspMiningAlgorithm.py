def ms_gsp(data_file, parameter_file, output_file):
    print()

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

    ms_gsp(data_file, parameter_file, output_file)