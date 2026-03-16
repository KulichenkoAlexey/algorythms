import timeit
import matplotlib.pyplot as plt
import numpy as np





x = list(range(10,30))
data = []
def fun():
    j = 10
    for i in range(10,30):
        j+=i
        data.append(j)
        print(data)
    return j
fun()
plt.plot(x, data, 'o-', label='O(n) - Линейный', linewidth=2)
plt.show()


