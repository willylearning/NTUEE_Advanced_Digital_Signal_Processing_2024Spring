import numpy as np
import matplotlib.pyplot as plt

k = input('Please enter k = ')
k = int(k)
# k = 8
N = 2*k+1

def Hd(F): # F is in range 0~1
    if(0 < F <= 0.5): 
        return -1j
    elif(0.5 < F <= 1):
        return 1j
    else:
        return 0

def H(F): # F is in range 0~1
    if(F == 1/N):
        return -0.9j
    elif(F == k/N):
        return -0.7j
    elif(F == (k+1)/N):
        return 0.7j   
    elif(F == (N-1)/N):
        return 0.9j 
    elif(0 < F <= 0.5): # F=0 need to set to 0
        return -1j
    elif(0.5 < F <= 1):
        return 1j
    else:
        return 0
    
def R(F, r):
    x = 0
    for i in range(len(r)): # i = 0 ~ N-1 (N=len(r))
        x += r[i]*np.exp(-2j*(np.pi)*F*(i-k))
    return x

H_arr = []
for m in range(N):
    H_arr.append(H(m/N))

r1 = np.fft.ifft(H_arr) # r1: n = 0~N-1

r = np.zeros_like(r1) # r: n = -k~k
for i in range(k):
    r[i] = r1[i+k+1]
for j in range(k+1):
    r[j+k] = r1[j]


F = np.linspace(0, 1, 10001)

Hd_arr = []
for f in F:
    Hd_arr.append(Hd(f))
Hd_arr = np.array(Hd_arr)
# print(Hd_arr)

R_arr = []
for f in F:
    R_arr.append(R(f, r))
R_arr = np.array(R_arr)
# R_arr = R_arr.reshape(-1)
# print(R_arr)

# impulse response
# we want h[n] = r[n-k]
n = np.arange(N) # n = 0~N-1
plt.stem(n, r)
plt.xlabel('n')
plt.ylabel('h[n]')
plt.title('impulse response')
plt.show()

# frequency response
plt.plot(F, Hd_arr.imag)
plt.plot(F, R_arr.imag)
plt.xlabel('F')
plt.legend(['Hd(F)','R(F)'])
plt.title('frequency response')
plt.show()
