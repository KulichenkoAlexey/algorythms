from random import random
import numpy as np

''' 
A - матрица расстояний между городами
alpha и beta - некоторые веса, показывающие что важнее: феромон или дистанция
p - коэффициент высыхания феромона
Изначально положим, что на каждой грани лежит f феромона
'''


def ant_alg(A, alpha=1, beta=1, p=0.6, f=0.2, q=3, iters=100):
    n = A.shape[0]
    ants = n

    F = np.ones([n, n]) * f - np.eye(n) * f

    best_path = None
    best_length = float('inf')
    
    for i in range(iters):
        paths = []
        for ant in range(ants):
            path = ant_path(A, F, alpha, beta, ant)
            paths.append(path)
        
        F = F_new(A, F, p, q, paths)
        
        # Находим лучший путь на этой итерации
        for path in paths:
            length = path_len(A, path)
            if length < best_length:
                best_length = length
                best_path = path.copy()

    best_path_ints = np.array([ int( city )  for city in best_path ]) 
    return best_path_ints, best_length

# Функция вероятностей
def P_i(A, F, i, available, alpha, beta):
    n = A.shape[0]
    nums = np.array([(F[i,j]**alpha) * ((1/A[i,j])**beta) if j in available else 0 for j in range(n)])
    denominator = sum(nums)
    if denominator == 0:  # Защита от деления на ноль
        return np.ones(n) / n
    return nums/denominator

def ant_path(A, F, alpha, beta, ant=0):
    n = A.shape[0]
    cities = np.array(list(range(n)))
    available = list(cities)
    path = [ant]  # Начинаем с заданного города
    current = ant
    available.remove(current)
    
    while available:
        probs = P_i(A, F, current, available, alpha, beta)
        # Выбираем только из доступных городов
        current = np.random.choice(available, p=probs[available])
        path.append(current)
        available.remove(current)
    
    # Возвращаемся в начальный город
    path.append(path[0])
    return path

def F_new(A, F, p, q, paths):
    F = F * p  # Испарение
    for path in paths:
        L = path_len(A, path)
        if L == 0:  # не считаем переход в город, где уже находится нужный муравей
            continue
            
        previous = path[0]
        for current in path[1:]:
            F[previous, current] += q/L
            F[current, previous] += q/L
            previous = current
    return F

def path_len(A, path):
    L = 0 
    previous = path[0]
    for current in path[1:]:
        L += A[previous, current]
        previous = current
    return L

if __name__ == "__main__":
    
   
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

    path, len_path = ant_alg(B, iters=50)
    print("Best path:", path)
    print("Path length:", len_path)

    


