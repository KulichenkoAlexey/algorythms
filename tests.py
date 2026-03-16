import numpy as np
from numpy import random
from ants import ant_alg
from branches_and_boundaries import branch_and_bound_tsp as bnb
import timeit
import matplotlib.pyplot as plt
 

# n - количество узлов
def generate_test_graph(n):
    coords = random.rand( n,2 )

    # Строим матрицу расстояний между рандомными координатами
    A = np.zeros([n,n])
    for i in range(n):
        for j in range(n):
            if i == j:
                A[i,j] = np.inf
            else:
                A[i,j] = (coords[i,0] - coords[j,0])**2 + (coords[i,1] - coords[j,1])**2
    
    # И все
    return A


B = np.array([
    [np.inf, 0.612, 0.301, 0.866, 0.563, 0.327, 0.245, 0.447, 0.327, 0.248],
    [0.612, np.inf, 0.552, 0.439, 0.739, 0.491, 0.334, 0.350, 0.352, 0.303],
    [0.301, 0.552, np.inf, 0.282, 0.506, 0.823, 0.619, 0.282, 0.368, 0.420],
    [0.866, 0.439, 0.282, np.inf, 0.643, 0.347, 0.261, 0.844, 0.431, 0.286],
    [0.563, 0.739, 0.506, 0.643, np.inf, 0.755, 0.428, 0.601, 0.651, 0.441],
    [0.327, 0.491, 0.823, 0.347, 0.755, np.inf, 0.976, 0.391, 0.658, 0.758],
    [0.245, 0.334, 0.619, 0.261, 0.428, 0.976, np.inf, 0.302, 0.501, 1.010],
    [0.447, 0.350, 0.282, 0.844, 0.601, 0.391, 0.302, np.inf, 0.699, 0.368],
    [0.327, 0.352, 0.368, 0.431, 0.651, 0.658, 0.501, 0.699, np.inf, 0.775],
    [0.248, 0.303, 0.420, 0.286, 0.441, 0.758, 1.010, 0.368, 0.775, np.inf]
])



if __name__ == "__main__":
    time_per_nod_ant = []
    time_per_nod_bnb = []
    iters = 20
    for i in range(3,12):
        continue # Убрать эту строку, если хочется подождать 2-3 минуты, и увидеть график, который уже есть
        print(i, "узлов, 1 измерение, ветви")
        time_ant = 0
        for j in range(iters):
            random_matrix = generate_test_graph(i)
            time_ant += timeit.timeit(lambda: ant_alg(random_matrix), number=1)
        time_ant /= iters
        print(i, "узлов, 1 измерение, муравьи")
        time_bnb = 0
        for j in range(iters):
            random_matrix = generate_test_graph(i)
            time_bnb += timeit.timeit(lambda: bnb(random_matrix), number=1)
        time_bnb /= iters

        time_per_nod_ant.append(time_ant)
        time_per_nod_bnb.append(time_bnb)
"""
    x = list(range(3,12))
    
    plt.plot(x, time_per_nod_ant, 'o-', linewidth=2)
    plt.plot(x, time_per_nod_bnb, 'o-', linewidth=2)


    plt.show()
"""
    
    time_per_nod = []
    for i in range(10, 30):
        continue # Убрать эту строку, если хочется подождать 15-20 минут, и увидеть график, который уже есть
        print(i, "узлов, 2 измерение")
        time = 0
        iters = 10
        for j in range(iters):

            random_matrix = generate_test_graph(i)
            time += timeit.timeit(lambda: ant_alg(random_matrix), number=1)
        time /= iters
        time_per_nod.append(time) 
    
    """
    x = list(range(10,30))
    
    plt.plot(x, time_per_nod, 'o-', linewidth=2)


    plt.show()
"""

