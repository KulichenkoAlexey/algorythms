import numpy as np
import heapq
import copy

def reduce_matrix(matrix):
    """Редукция матрицы стоимостей"""
    n = matrix.shape[0]
    reduced_matrix = matrix.copy()
    reduction_cost = 0
    
    # Редукция по строкам
    for i in range(n):
        # Ищем минимальный элемент в строке (исключая бесконечности)
        min_val = np.inf
        for j in range(n):
            if reduced_matrix[i, j] < min_val:
                min_val = reduced_matrix[i, j]
        
        if min_val != np.inf and min_val != 0:
            for j in range(n):
                if reduced_matrix[i, j] != np.inf:
                    reduced_matrix[i, j] -= min_val
            reduction_cost += min_val
    
    # Редукция по столбцам
    for j in range(n):
        # Ищем минимальный элемент в столбце
        min_val = np.inf
        for i in range(n):
            if reduced_matrix[i, j] < min_val:
                min_val = reduced_matrix[i, j]
        
        if min_val != np.inf and min_val != 0:
            for i in range(n):
                if reduced_matrix[i, j] != np.inf:
                    reduced_matrix[i, j] -= min_val
            reduction_cost += min_val
    
    return reduction_cost, reduced_matrix

def get_next_cities(matrix, current_city, visited):
    """Получение списка доступных городов из текущего"""
    n = matrix.shape[0]
    next_cities = []
    
    for city in range(n):
        if (city not in visited and 
            matrix[current_city, city] != np.inf and
            current_city != city):
            next_cities.append(city)
    
    return next_cities

def calculate_lower_bound(matrix, path, current_cost):
    """Вычисление нижней границы для текущего узла"""
    n = matrix.shape[0]
    
    if len(path) == n:
        # Если путь полный, добавляем возврат в начальный город
        return_cost = matrix[path[-1], path[0]]
        if return_cost != np.inf:
            return current_cost + return_cost
        else:
            return np.inf
    
    # Копируем матрицу для редукции
    temp_matrix = matrix.copy()
    
    # Запрещаем переходы в уже посещенные города
    for city in path:
        temp_matrix[city, :] = np.inf
        temp_matrix[:, city] = np.inf
    
    # Запрещаем переходы из последнего города в уже посещенные
    if path:
        last_city = path[-1]
        for city in path[:-1]:
            temp_matrix[last_city, city] = np.inf
    
    # Выполняем редукцию
    reduction_cost, _ = reduce_matrix(temp_matrix)
    
    return current_cost + reduction_cost

class Node:
    """Узел дерева поиска"""
    def __init__(self, level, path, cost, bound, matrix):
        self.level = level  # Уровень в дереве (сколько городов посещено)
        self.path = path.copy()  # Текущий путь
        self.cost = cost  # Текущая стоимость
        self.bound = bound  # Нижняя граница
        self.matrix = matrix.copy()  # Текущая матрица стоимостей
    
    def __lt__(self, other):
        # Для приоритетной очереди: меньшая граница имеет высший приоритет
        return self.bound < other.bound

def branch_and_bound_tsp(cost_matrix, start_city=0):
    """Алгоритм ветвей и границ для задачи коммивояжера"""
    n = cost_matrix.shape[0]
    
    # Инициализация начального узла
    initial_matrix = cost_matrix.copy()
    
    # Вычисляем начальную границу
    initial_reduction_cost, reduced_matrix = reduce_matrix(initial_matrix)
    initial_bound = initial_reduction_cost
    
    # Создаем начальный узел
    initial_node = Node(
        level=1,
        path=[start_city],
        cost=0,
        bound=initial_bound,
        matrix=reduced_matrix
    )
    
    # Инициализируем приоритетную очередь
    pq = []
    heapq.heappush(pq, initial_node)
    
    # Лучшее решение и его стоимость
    best_path = None
    min_cost = np.inf
    
    # Ограничим количество итераций для безопасности
    max_iterations = 10000
    iterations = 0
    
    while pq and iterations < max_iterations:
        iterations += 1
        
        # Извлекаем узел с наименьшей границей
        current_node = heapq.heappop(pq)
        
        # Если граница хуже текущего лучшего решения, пропускаем
        if current_node.bound >= min_cost:
            continue
        
        # Если мы посетили все города
        if current_node.level == n:
            # Добавляем возврат в начальный город
            last_city = current_node.path[-1]
            return_cost = cost_matrix[last_city, start_city]
            
            if return_cost != np.inf:
                total_cost = current_node.cost + return_cost
                
                if total_cost < min_cost:
                    min_cost = total_cost
                    best_path = current_node.path.copy()
                    best_path.append(start_city)
            continue
        
        # Получаем текущий город
        current_city = current_node.path[-1]
        
        # Получаем доступные города для перехода
        available_cities = get_next_cities(
            current_node.matrix, 
            current_city, 
            set(current_node.path)
        )
        
        if not available_cities:
            continue
        
        # Перебираем доступные города
        for next_city in available_cities:
            # Создаем новую матрицу для дочернего узла
            new_matrix = current_node.matrix.copy()
            
            # Запрещаем переходы из текущего города во все другие
            for city in range(n):
                new_matrix[current_city, city] = np.inf
            
            # Запрещаем переходы в следующий город из всех других
            for city in range(n):
                new_matrix[city, next_city] = np.inf
            
            # Запрещаем обратный переход (чтобы избежать циклов)
            new_matrix[next_city, current_city] = np.inf
            
            # Вычисляем стоимость перехода
            transition_cost = cost_matrix[current_city, next_city]
            if transition_cost == np.inf:
                continue
            
            # Новая стоимость пути
            new_cost = current_node.cost + transition_cost
            
            # Редуцируем новую матрицу
            reduction_cost, reduced_new_matrix = reduce_matrix(new_matrix)
            
            # Вычисляем новую границу
            new_bound = new_cost + reduction_cost
            
            # Создаем новый путь
            new_path = current_node.path.copy()
            new_path.append(next_city)
            
            # Создаем дочерний узел
            child_node = Node(
                level=current_node.level + 1,
                path=new_path,
                cost=new_cost,
                bound=new_bound,
                matrix=reduced_new_matrix
            )
            
            # Добавляем узел в очередь, если его граница перспективна
            if child_node.bound < min_cost:
                heapq.heappush(pq, child_node)
    
    return best_path, min_cost

# Тестовая матрица (стоимости переходов между городами)
def create_test_matrix(n=5, seed=42):
    """Создание тестовой матрицы стоимостей"""
    np.random.seed(seed)
    # Создаем матрицу случайных чисел от 10 до 100
    matrix = np.random.uniform(10, 100, size=(n, n))
    
    # Заполняем диагональ бесконечностями
    for i in range(n):
        matrix[i, i] = np.inf
    
    # Делаем матрицу симметричной
    matrix = (matrix + matrix.T) / 2
    
    return matrix

# Тесты
if __name__ == "__main__":
    print("Тест 1: Простая матрица 4x4")
    A = np.array([
        [np.inf, 10, 15, 20],
        [10, np.inf, 35, 25],
        [15, 35, np.inf, 30],
        [20, 25, 30, np.inf]
    ])
    
    path, cost = branch_and_bound_tsp(A, start_city=0)
    print(f"Лучший путь: {path}")
    print(f"Стоимость: {cost}")
    print()
    
    print("Тест 2: Случайная матрица 5x5")
    B = create_test_matrix(5)
    print("Матрица стоимостей:")
    print(B)
    print()
    
    path, cost = branch_and_bound_tsp(B, start_city=0)
    print(f"Лучший путь: {path}")
    print(f"Стоимость: {cost}")
    print()
    
    print("Тест 3: Матрица с невозможными переходами")
    C = np.array([
        [np.inf, 10, np.inf, 20],
        [10, np.inf, 35, 25],
        [np.inf, 35, np.inf, 30],
        [20, 25, 30, np.inf]
    ])
    
    path, cost = branch_and_bound_tsp(C, start_city=0)
    print(f"Лучший путь: {path}")
    print(f"Стоимость: {cost}")