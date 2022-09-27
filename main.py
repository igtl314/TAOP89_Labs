import scipy.io

print("enter file name: ", end="")
fileName = input()  

fileName= fileName +".mat"
print("Reading data from file '" + fileName + "'")

filedata = scipy.io.loadmat(fileName)
print((filedata['zcheat']))