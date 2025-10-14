"""
Travelling Salesman Problem - Ant Colony Optimization Solution
Giải bài toán người du lịch bằng thuật toán ACO (Ant Colony Optimization)
"""

import numpy as np
import time
from typing import List, Tuple

class TSP_ACO:
    def __init__(self, cities: List[str], distance_matrix: np.ndarray,
                 n_ants: int = 20, n_iterations: int = 100,
                 alpha: float = 1.0, beta: float = 2.0,
                 evaporation_rate: float = 0.5, q: float = 100):
        """
        Khởi tạo thuật toán ACO cho TSP
        
        Args:
            cities: Danh sách tên các thành phố
            distance_matrix: Ma trận khoảng cách giữa các thành phố
            n_ants: Số lượng kiến trong mỗi iteration
            n_iterations: Số lượng iteration
            alpha: Tham số ảnh hưởng của pheromone
            beta: Tham số ảnh hưởng của heuristic (khoảng cách)
            evaporation_rate: Tỷ lệ bay hơi pheromone
            q: Hằng số cho việc cập nhật pheromone
        """
        self.cities = cities
        self.distance_matrix = distance_matrix
        self.n_cities = len(cities)
        self.n_ants = n_ants
        self.n_iterations = n_iterations
        self.alpha = alpha
        self.beta = beta
        self.evaporation_rate = evaporation_rate
        self.q = q
        
        # Khởi tạo ma trận pheromone
        self.pheromone = np.ones((self.n_cities, self.n_cities))
        
        # Khởi tạo ma trận heuristic (nghịch đảo khoảng cách)
        self.heuristic = np.zeros((self.n_cities, self.n_cities))
        for i in range(self.n_cities):
            for j in range(self.n_cities):
                if i != j and self.distance_matrix[i][j] > 0:
                    self.heuristic[i][j] = 1.0 / self.distance_matrix[i][j]
        
        self.best_route = None
        self.best_distance = float('inf')
        self.execution_time = 0
        self.convergence_data = []
        
    def calculate_route_distance(self, route: List[int]) -> float:
        """Tính tổng khoảng cách của một tuyến đường"""
        total_distance = 0
        for i in range(len(route) - 1):
            total_distance += self.distance_matrix[route[i]][route[i + 1]]
        # Quay về thành phố xuất phát
        total_distance += self.distance_matrix[route[-1]][route[0]]
        return total_distance
    
    def select_next_city(self, current_city: int, unvisited: List[int]) -> int:
        """
        Chọn thành phố tiếp theo dựa trên xác suất
        Xác suất phụ thuộc vào pheromone và heuristic
        """
        probabilities = []
        
        for city in unvisited:
            pheromone_value = self.pheromone[current_city][city] ** self.alpha
            heuristic_value = self.heuristic[current_city][city] ** self.beta
            probabilities.append(pheromone_value * heuristic_value)
        
        # Chuẩn hóa xác suất
        total = sum(probabilities)
        if total == 0:
            return np.random.choice(unvisited)
        
        probabilities = [p / total for p in probabilities]
        
        # Chọn thành phố dựa trên xác suất
        next_city = np.random.choice(unvisited, p=probabilities)
        return next_city
    
    def construct_solution(self) -> Tuple[List[int], float]:
        """Xây dựng một giải pháp (tuyến đường) cho một con kiến"""
        # Bắt đầu từ thành phố ngẫu nhiên
        start_city = np.random.randint(0, self.n_cities)
        route = [start_city]
        unvisited = list(range(self.n_cities))
        unvisited.remove(start_city)
        
        # Xây dựng tuyến đường
        while unvisited:
            current_city = route[-1]
            next_city = self.select_next_city(current_city, unvisited)
            route.append(next_city)
            unvisited.remove(next_city)
        
        distance = self.calculate_route_distance(route)
        return route, distance
    
    def update_pheromone(self, all_routes: List[Tuple[List[int], float]]):
        """Cập nhật ma trận pheromone dựa trên các tuyến đường đã tìm được"""
        # Bay hơi pheromone
        self.pheromone *= (1 - self.evaporation_rate)
        
        # Thêm pheromone mới
        for route, distance in all_routes:
            pheromone_deposit = self.q / distance
            for i in range(len(route) - 1):
                self.pheromone[route[i]][route[i + 1]] += pheromone_deposit
                self.pheromone[route[i + 1]][route[i]] += pheromone_deposit
            # Cạnh quay về
            self.pheromone[route[-1]][route[0]] += pheromone_deposit
            self.pheromone[route[0]][route[-1]] += pheromone_deposit
    
    def solve(self) -> dict:
        """
        Giải bài toán TSP bằng thuật toán ACO
        """
        start_time = time.time()
        
        print(f"\n{'='*60}")
        print(f"Bắt đầu thuật toán ACO với {self.n_ants} kiến, {self.n_iterations} iterations")
        print(f"{'='*60}\n")
        
        for iteration in range(self.n_iterations):
            all_routes = []
            
            # Mỗi con kiến xây dựng một giải pháp
            for ant in range(self.n_ants):
                route, distance = self.construct_solution()
                all_routes.append((route, distance))
                
                # Cập nhật giải pháp tốt nhất
                if distance < self.best_distance:
                    self.best_distance = distance
                    self.best_route = route
            
            # Cập nhật pheromone
            self.update_pheromone(all_routes)
            
            # Lưu dữ liệu hội tụ
            self.convergence_data.append(self.best_distance)
            
            # In tiến trình
            if (iteration + 1) % 10 == 0:
                print(f"Iteration {iteration + 1}/{self.n_iterations}: "
                      f"Khoảng cách tốt nhất = {self.best_distance:.2f} km")
        
        self.execution_time = time.time() - start_time
        
        # Chuyển đổi route từ index sang tên thành phố
        best_route_names = [self.cities[i] for i in self.best_route]
        
        print(f"\n{'='*60}")
        print(f"Hoàn thành! Thời gian: {self.execution_time:.4f} giây")
        print(f"{'='*60}\n")
        
        return {
            'route': best_route_names,
            'distance': self.best_distance,
            'time': self.execution_time,
            'algorithm': 'ACO (Ant Colony Optimization)',
            'convergence': self.convergence_data
        }


if __name__ == "__main__":
    # Test với dữ liệu mẫu
    cities = ['Hà Nội', 'Hải Phòng', 'Đà Nẵng', 'TP.HCM', 'Cần Thơ']
    
    # Ma trận khoảng cách (km)
    distance_matrix = np.array([
        [0, 120, 764, 1710, 1840],
        [120, 0, 840, 1830, 1960],
        [764, 840, 0, 964, 1094],
        [1710, 1830, 964, 0, 169],
        [1840, 1960, 1094, 169, 0]
    ])
    
    solver = TSP_ACO(cities, distance_matrix, n_ants=20, n_iterations=100)
    result = solver.solve()
    
    print(f"Thuật toán: {result['algorithm']}")
    print(f"Tuyến đường tốt nhất: {' -> '.join(result['route'])} -> {result['route'][0]}")
    print(f"Tổng khoảng cách: {result['distance']:.2f} km")
    print(f"Thời gian thực thi: {result['time']:.4f} giây")
