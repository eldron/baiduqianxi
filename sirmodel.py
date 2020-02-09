# susceptible, infectious, recovered
# 恢复者不会再次感染
# 感染者有gama概率变成恢复者


import matplotlib.pyplot as plt
import numpy as np


N = 10000
I = 1
S = N - I
R = 0

r = 10
beta = 0.05
gama = 0.1

I_vec = [I]
S_vec = [S]
R_vec = [R]
x = []

for i in range(200):
	x.append(i)
	I_vec.append(I_vec[i] + I_vec[i] * r * beta * S_vec[i] / N - gama * I_vec[i])
	S_vec.append(S_vec[i] - I_vec[i] * r * beta * S_vec[i] / N)
	R_vec.append(R_vec[i] + gama * I_vec[i])

x.append(201)

plt.plot(x, I_vec, color = 'r', label = 'Infectious')
plt.plot(x, S_vec, color = 'b', label = 'Susceptible')
plt.plot(x, R_vec, color = 'y', label = 'Recovered')
plt.legend(loc = 'upper left')
plt.show()