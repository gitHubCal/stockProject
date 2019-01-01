#!../bin/python3
#Invoke interpreter directly from miniconda env in directory i.e. /home/calvin/python_projects/stockProject

import numpy as np

def checkEqual(input_array):
    input_array = np.nditer(input_array)
    try:
        first = next(input_array)
    except StopIteration:
        return True
    return all(first == rest for rest in input_array)

def checkIfAnyArrayEqual(input_matrix):
    for arr in input_matrix:
        if checkEqual(arr) is True:
            return True
        elif np.allclose(arr,input_matrix[-1]) and checkEqual(arr) is False:
            return False
        else:
            continue

#Checks if input matrix's correlation coefficient is computable (i.e. returns a NON-nan matrix)
#NOTE: If ALL the arrays are multiples of each other (i.e. their columns), 
#then the arrays (variables) are directly correlated and thus the correlation coefficient is 1.
#e.g. [1,2,3], [2,4,6], [4,8,12]
#NOTE: IF not all the arrays are multiples of each other (i.e. only two or three out of four are multiples) then normalized autocorrelation can be calculated
def checkIfCorrelationCoefficientComputable(input_matrix):
    #There is no input matrix. Either None or something. 
    if input_matrix is not None:
        #Input matrix will never be length 0. Sanity check. 
        if len(input_matrix) == 0:
            print("No correlation coefficient matrix can be calculated from length zero matrix.\n")
            return False
        else:  
            print("Checking.\n")
            #Checking if any array is all zeroes and/or constant values
            #e.g. [1,2,3], [1,1,1], [1,2,3] OR [0,0,0], [1,4,5], [2,3,6]
            if checkIfAnyArrayEqual(input_matrix) is True:
                print("Pearson's r is not defined for constant timeseries, as their standard deviation is zero.\n")
                return False
            else:
                #Check if ALL arrays are the same
                #Two arrays can be the same, as long as ALL the arrays are NOT the same. Correlation is not defined if all arrays are the same.
                #e.g. [1,2,3], [1,2,3], [1,2,3]
                if all(np.allclose(arr, input_matrix[0]) for arr in input_matrix) is True:
                    print("Arrays are all the same. Variance is zero. Cannot compute ccorrelation.\n")
                    return False
                else:
                    #Input matrix has no array that is constant AND no arrays that are all the same 
                    #Input matrix with arrays that are ALL multiples of each other (i.e. their columns) are acceptable
                    print("Input matrix is acceptable.\n")
                    return True
    else:
        print("No input matrix.\n")
        return False

#Autocorrelation: +1 == strong positive association, -1 == strong negative association, and 0 to no association
def calculateAutocorrelationMatrix(input_matrix):
    #Gurantees that input corrcoeff_matrix will not be a NaN matrix
    if checkIfCorrelationCoefficientComputable(input_matrix) is False:
        print("Autocorrelation cannot be computed. No correlation coefficient matrix.\n")
        return None
    else:
        #Special case of input matrix being length 1
        if len(input_matrix) == 1:
            print("Length of input matrix is 1.\n")
            #Check if elements in single array are same
            if checkEqual(input_matrix) is True:
                print("Pearson's r is not defined for constant timeseries, as their standard deviation is zero.\n")
                return None
            else:
                #Return autocorrelation matrix of zero i.e. [0]
                return np.array([0])
        else: 
            print("corrcoeff_matrix:\n")
            corrcoeff_matrix = np.corrcoef(input_matrix)
            print(corrcoeff_matrix)
            #NOTE: Values of correlation coefficient matrix do not matter now. 
            row_column_tuple = corrcoeff_matrix.shape #rows, columns
            print("Row_column_tuple:\n")
            print(row_column_tuple)
            #sizeOfUpperTriangleArray = (row_column_tuple[0]*(row_column_tuple[0]-1))/2 #For m x m matrix
            #k=1 diagonal to the right, does not include diagonal
            data_numpyArray = corrcoeff_matrix[np.triu_indices(row_column_tuple[1],k=1)]
            print("data_numpyArray: \n")
            print(data_numpyArray)
            n = len(data_numpyArray)
            print("length n: \n")
            print(str(n))
            variance = np.var(data_numpyArray)
            #The variance of constant variable is zero i.e. [1] or [1,1,1]
            print("variance: \n")
            print(str(variance))
            data_numpyArray = data_numpyArray - np.mean(data_numpyArray)
            print("data_numpyArray with mean subtracted: \n")
            print(data_numpyArray)
            r = np.correlate(data_numpyArray, data_numpyArray, mode = 'full')[-n:]
            print("autocorrelation result: \n")
            if variance == 0:
                print("Returning Non-normalized autocorrelation result matrix.\n")
                return r
            else:
                print("Returning normalized autocorrelation result matrix.\n")
                result = r/(variance*(np.arange(n, 0, -1)))
                return result