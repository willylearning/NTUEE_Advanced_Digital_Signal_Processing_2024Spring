import numpy as np
from math import cos, pi
import matplotlib.pyplot as plt

N = 17
k = (N-1)//2 # 8 -> k+2 = 10 extreme points
delta = 0.0001
# f = np.linspace(0, 0,5, delta) # 5001 points(plus 0)

# function define
def W(F):
    if(0 <= F <= 0.2):
        return 1
    elif(0.25 <= F <= 0.5):
        return 0.6
    else:
        return 0
    
def Hd(F): 
    if( 0 <= F <= 0.225): 
        return 1
    else:
        return 0

def R(F, S):
    x = 0
    for i in range(k+1): # only k+1
        x += S[i]*(cos(2*pi*F*i))
    return x

def err(F, S):
    return (R(F, S) - Hd(F))*W(F)

E1 = 10000000 # should be infinity

# Step 1
Fm = [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45]
# A = np.zeros((len(Fm), len(Fm)))
# H = np.zeros((len(Fm), 1))
iteration_cnt = 1

while(True):
    A = np.zeros((k+2, k+2)) # AS = H
    H = np.zeros((k+2, 1))
    # Step 2
    for i in range(k+2): # i = 0~9
        for j in range(k+2): # j = 0~9
            if(j == 0):
                A[i][j] = 1
            elif(j == k+1):
                A[i][j] = ((-1)**i)/W(Fm[i])
            else:
                A[i][j] = cos(2*(pi)*j*Fm[i])    
    for i in range(k+2): # i = 0~9
        H[i][0] = Hd(Fm[i])

    S = np.dot(np.linalg.inv(A),H) # (k+2)*1 array

    # Step 3 : Compute err(F) for 0 <= F <= 0.5, exclude the transition band
    # Step 4 : extreme points
    extreme = []
    for j in range(5001): # 0~5000, consider boundary
        j0 = j/10000 # delta = 0.0001
        if(j0 == 0): # leftmost boundary
            if(err(j0, S) > 0 and err(j0, S) > err(j0+delta, S)):
                extreme.append(j0)
            elif(err(j0, S) < 0 and err(j0, S) < err(j0+delta, S)):
                extreme.append(j0)
        elif(j0 == 0.2): # transition left boundary
            if(err(j0, S) > err(j0+delta, S) and err(j0, S) > err(j0-delta, S)): # > transition band
                extreme.append(j0)
            elif(err(j0, S) < err(j0+delta, S) and err(j0, S) < err(j0-delta, S)): # < transition band
                extreme.append(j0)
        elif(j0 == 0.25): # transition right boundary
            if(err(j0, S) > err(j0-delta, S) and err(j0, S) > err(j0+delta, S)): # > transition band
                extreme.append(j0)
            elif(err(j0, S) < err(j0-delta, S) and err(j0, S) < err(j0+delta, S)): # < transition band
                extreme.append(j0)    
        elif(j0 == 0.5): # rightmost boundary
            if(err(j0, S) > 0 and err(j0, S) > err(j0-delta, S)):
                extreme.append(j0)
            elif(err(j0, S) < 0 and err(j0, S) < err(j0-delta, S)):
                extreme.append(j0)
        elif((err(j0, S) > err(j0-delta, S)) and (err(j0, S) > err(j0+delta, S))):
            extreme.append(j0)
        elif((err(j0, S) < err(j0-delta, S)) and (err(j0, S) < err(j0+delta, S))):
            extreme.append(j0)

    err_max = 0
    for j in range(5001): # 0~5000, consider boundary
        j0 = j/10000 # delta = 0.0001
        if(abs(err(j0, S)) > err_max):
            err_max = abs(err(j0, S))
    E0 = err_max
    # print(type(E0))
    print("iteration ", iteration_cnt, " max error = ", E0)
    # print("iteration ", iteration_cnt, " extreme = ", extreme)
    iteration_cnt += 1

    if((E1-E0 > delta) or (E1-E0 < 0)):
        Fm = extreme
        E1 = E0
    else:
        break

f = np.linspace(0, 0.5, 5001) # 5001 points(plus 0)
# print(f.shape)
R_arr = np.zeros(5001)
Hd_arr = np.zeros(5001)
# print(R_arr.shape)
for u in range(5001):
    u0 = u/10000
    R_arr[u] = R(u0,S)

for u in range(5001):
    u0 = u/10000
    Hd_arr[u] = Hd(u0)

plt.plot(f,R_arr)
plt.plot(f,Hd_arr)
plt.xlabel('F')
plt.legend(['R(F)','Hd(F)'])
plt.title('frequency response')
plt.show()

h = np.zeros((N)) # 17 points
h[k] = S[0]
for i in range(1,k+1):
    h[k-i] = S[i]/2
    h[k+i] = S[i]/2

n = np.arange(17) # 0~16

plt.stem(n,h)
plt.xlabel('n')
plt.ylabel('h[n]')
plt.title('impulse response')
plt.show()