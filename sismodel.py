import matplotlib.pyplot as plt
import numpy as np

# 感染者有概率gama恢复健康，但仍可能再次感染

N = 10000
I = 1
S = N - I

r = 10
beta = 0.01
gama = 0.02

I_vec = [I]
S_vec = [S]
x = []

for i in range(200):
	x.append(i)
	I_vec.append(I_vec[i] + I_vec[i] * r * beta * S_vec[i] / N - gama * I_vec[i]) 
	S_vec.append(S_vec[i] - I_vec[i] * r * beta * S_vec[i] / N + gama * I_vec[i]) 

x.append(201)

plt.plot(x, I_vec, color = 'r', label = 'Infectious')
plt.plot(x, S_vec, color = 'b', label = 'Susceptible')
plt.legend(loc = 'upper left')
plt.show()