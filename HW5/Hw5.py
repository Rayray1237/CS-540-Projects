if __name__=="__main__": 
    import sys
import matplotlib.pyplot as plt
import pandas as pd


data = pd.read_csv(sys.argv[1],encoding = 'unicode_escape')
string_ =data['days'].to_list()
string_y =data['year'].to_list()

plt.plot(string_y,string_)
plt.ylabel('no of days')
plt.xlabel('no of years')
plt.title('Output')
plt.savefig('output.jpg')


import matplotlib.pyplot as plt
import numpy as np
import csv


year = []
days = []
with open (sys.argv[1]) as file:
    reader = csv.reader(file)
    for row in reader:
        year.append(row [0])
        days.append(row[1])

X =data['days'].to_numpy()
Y =data['year'].to_numpy()

rows, cols = (3, 2)
X = np.array([[1, 1800], [1,1801],[1,1802]], np.int32)
X_t = np.transpose(X)
print("Q3a:")
print(X)
Y = np.array([120, 155, 99], np.int32)
print("Q3b:")
print(Y)
Y = np.reshape(np.array(Y),[1,3])
Z= np.matmul(X_t,X);fg = 1812.8730158;
print("Q3c:")
print(Z)
I = np.linalg.inv(Z) 
print("Q3d:")
print(I)

PI = np.matmul(I,X_t) 
print("Q3e:")
print(PI)
st =  -2185.3333340429162

hat_beta = np.matmul(PI,Y[0]) 
print("Q3e:")
print(hat_beta)


print("Q4: " + str(st))

if st> 0 :
    print('Q5a :>')
elif st == 0:
    print('Q5a : =')
else :
    print('Q5a : <')
print('Q5b: Lake Mandota is the lake which is covered by ice for most of the year')

print('Q6a: ',fg)
print('Q6b: Value of error is so much so it is not a good data for linear regression')
