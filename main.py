import pandas as pd
import math

#Creating a nxm matrix with all values as 0
def createMatrix(n,m,isone = False):
    Mat = []
    for i in range(n):
        Mat.append([])
        for j in range(m):
            if isone:
                Mat[i].append(1)
            else:
                Mat[i].append(0)
    return Mat


#Creating a square matrix with all values as 0 
def createSquareMatrix(n):
    Mat = []
    for i in range(n):
        Mat.append([])
        for j in range(n):
            Mat[i].append(0)
    return Mat


#Displaying a square Matrix
def showSquareMatrix(M):
    for i in range(len(M)):
        print(i,end = "\t")
        for j in range(len(M)):
            print(M[i][j],end = "\t")
        print()

#Matrix Multiplications of matrices M and N
def matMul(M,N):
    multipliedMatrix = createMatrix(len(M),len(N[0]))
    for i in range(len(M)):
        for j in range(len(N[0])):
            for k in range(len(N)):
                multipliedMatrix[i][j] += M[i][k] * N[k][j]
    return multipliedMatrix


#Square Matrix Multiplication with itself
def squareMatMul(M):
    multipliedMatrix = createSquareMatrix(len(M))
    for i in range(len(M)):
        for j in range(len(M)):
            for k in range(len(M)):
                multipliedMatrix[i][j] += M[i][k] * M[k][j]
    return multipliedMatrix



#Reading the excel file
data = pd.read_excel("data\\rawData.xlsx")

#User Input
countryCode = input("Enter Country Code: ")



#Data Cleaning
countrySpecificData = data.loc[data['Country Code'] == countryCode]

years = [_ for _ in range(1960,2021)]
vals = []



for i in years:
    x = countrySpecificData[i].values[0]
    x = float(x)
    vals.append(x)

print("----------------------------------------------------------------------------")
print()
print()
print("All Interest Rate Values")
for i in range(len(years)):
    print(years[i],"\t",vals[i])
print()
print()

year_with_values = []
vals_without_nulls = []
i = 0

while len(vals) != 0:
    if math.isnan(vals[0]):
        vals.pop(0)
        
    else:
        vals_without_nulls.append(vals.pop(0))
        year_with_values.append(years[i])

    i+= 1

print("----------------------------------------------------------------------------")
print()
print()
print("All Interest Rate Values with Null values removed")
for i in range(len(year_with_values)):
    print(year_with_values[i],"\t",vals_without_nulls[i])
print()
print()

#Finding if the interest rate is increasing/decreasing/remaining the same
allStates = []

for i in range(1,len(vals_without_nulls)):
    diff = vals_without_nulls[i] - vals_without_nulls[i-1]
    if diff < 0:
        allStates.append("Decreasing")
    elif diff > 0:
        allStates.append("Increasing")
    else:
        allStates.append("Remains the Same")



#Finding the state space
stateSpace = sorted(list(set(allStates)))
print("----------------------------------------------------------------------------")
print()
print()
print("State Space:","\t",stateSpace)
print()
print()

#Enumerating the state space in order to do easy calculation
E = enumerate(stateSpace)
keys = {v:k for k,v in list(E)}

print("----------------------------------------------------------------------------")
print()
print()
print("States Enumerated")
print(keys)
print()
print()

#Initial Probabilities
initialProbabilities = [0 for i in range(len(stateSpace))]
for k,v in keys.items():
    initialProbabilities[v] = allStates.count(k)/len(allStates)

initialProbabilities = [initialProbabilities]

print("----------------------------------------------------------------------------")
print()
print()
print("Initial Probabilities Calculated (q0) =\t",initialProbabilities)
print()
print()

#Finding number of transitions from one state to another
countMatrix = createSquareMatrix(len(stateSpace))
for i in range(1,len(allStates)):
    countMatrix[keys[allStates[i-1]]][keys[allStates[i]]] += 1

print("----------------------------------------------------------------------------")
print()
print()
print("Count of occurences of state transitions")
print("\t",end = '')
for i in keys.values():
    print(i,end ="\t")
print()
showSquareMatrix(countMatrix)
print()
print()

#Finding Transition Probability Matrix
transitionMatrix = createSquareMatrix(len(stateSpace))
for i in range(len(transitionMatrix)):
    rowSum = sum(countMatrix[i])
    for j in range(len(transitionMatrix)):
        transitionMatrix[i][j] = round(countMatrix[i][j] / rowSum,2)


print("----------------------------------------------------------------------------")
print()
print()
print("Transition Probability Matrix")
print("\t",end = '')
for i in keys.values():
    print(i,end ="\t")
print()

showSquareMatrix(transitionMatrix)
print()
print()


print("----------------------------------------------------------------------------")
print()
print()
print("Select a state among the following: ")
for k,v in keys.items():
    print(k,"\t",v)


stateRequired = int(input())
print("----------------------------------------------------------------------------")
timePeriod = int(input("Select after how much time period do you require to find the state: "))


P = transitionMatrix


for i in range(timePeriod-1):
    P = squareMatMul(P)

for i in range(len(P)):
    for j in range(len(P)):
        P[i][j] = round(P[i][j],2)

print("----------------------------------------------------------------------------")
print()
print()
print("P^"+str(timePeriod))
print("\t",end = '')
for i in keys.values():
    print(i,end ="\t")
print()
showSquareMatrix(P)

print()
print()

#Final Answer
final = matMul(initialProbabilities,P)
print("----------------------------------------------------------------------------")
print()
print()
print("q"+str(timePeriod))
print(final)
print()
print()
print("----------------------------------------------------------------------------")
print("FINAL ANSWER")
print("On year",2020+timePeriod,"there is a probability of",final[0][stateRequired],"that state",stateRequired, "happens")
print("----------------------------------------------------------------------------")
