import matplotlib.pyplot as plt
import numpy as np

N = 10000
I = 1
S = N - I # susceptible, 易感染人数

r = 10 # 感染者接触易感染人数
beta = 0.01 # 传染概率

I_vec = [I]
S_vec = [S]
x = []

for i in range(200):
	x.append(i)
	I_vec.append(I_vec[i] + I_vec[i] * r * beta * S_vec[i] / N)
	S_vec.append(S_vec[i] - I_vec[i] * r * beta * S_vec[i] / N)

x.append(201)

plt.plot(x, I_vec, color = 'r', label = 'Infectious')
plt.plot(x, S_vec, color = 'b', label = 'Susceptible')
plt.legend(loc = 'upper left')
plt.show()