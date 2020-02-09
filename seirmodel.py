# susceptible, exposed, infectious, recovered
# susceptibel(通过接触infectious) 有概率 beta 变为exposed
# susceptible 接触exposed无事
# exposed 有概率 alpha 变为infectious
# infectious 有概率 gama 变为 recovered

import matplotlib.pyplot as plt
import numpy as np

N = 10000
E = 0
I = 1
S = N - I
R = 0

r = 20
beta = 0.03
alpha = 0.1
gama = 0.1

I_vec = [I]
S_vec = [S]
R_vec = [R]
E_vec = [E]
x = []

for i in range(200):
	x.append(i)
	I_vec.append(I_vec[i] + alpha * E_vec[i] - gama * I_vec[i])
	S_vec.append(S_vec[i] - I_vec[i] * r * beta * S_vec[i] / N)
	R_vec.append(R_vec[i] + gama * I_vec[i])
	E_vec.append(E_vec[i] - alpha * E_vec[i] + I_vec[i] * r * beta * S_vec[i] / N)

x.append(201)

plt.plot(x, I_vec, color = 'r', label = 'Infectious')
plt.plot(x, S_vec, color = 'b', label = 'Susceptible')
plt.plot(x, R_vec, color = 'g', label = 'Recovered')
plt.plot(x, E_vec, color = 'y', label = 'Exposed')
plt.legend(loc = 'upper left')
plt.show()