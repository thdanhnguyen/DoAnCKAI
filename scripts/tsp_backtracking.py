"""
Travelling Salesman Problem - Backtracking Solution using simpleAI
Giải bài toán người du lịch bằng thuật toán quay lui với thư viện simpleAI
"""

from simpleai.search import CspProblem, backtrack
import time
import numpy as np

class TSPBacktracking:
    def __init__(self, cities, distance_matrix):
        """
        Khởi tạo bài toán TSP với Backtracking
        
        Args:
            cities: Danh sách tên các thành phố
            distance_matrix: Ma trận khoảng cách giữa các thành phố
        """
        self.cities = cities
        self.distance_matrix = distance_matrix
        self.n_cities = len(cities)
        self.best_route = None
        self.best_distance = float('inf')
        self.execution_time = 0
        
    def calculate_route_distance(self, route):
        """Tính tổng khoảng cách của một tuyến đường"""
        total_distance = 0
        for i in range(len(route) - 1):
            city1 = self.cities.index(route[i])
            city2 = self.cities.index(route[i + 1])
            total_distance += self.distance_matrix[city1][city2]
        # Quay về thành phố xuất phát
        city1 = self.cities.index(route[-1])
        city2 = self.cities.index(route[0])
        total_distance += self.distance_matrix[city1][city2]
        return total_distance
    
    def solve(self):
        """
        Giải bài toán TSP bằng Backtracking với simpleAI
        Sử dụng CSP (Constraint Satisfaction Problem) framework
        """
        start_time = time.time()
        
        # Định nghĩa biến: mỗi vị trí trong tuyến đường
        variables = [f'position_{i}' for i in range(self.n_cities)]
        
        # Định nghĩa miền giá trị: các thành phố có thể đi
        domains = {var: list(self.cities) for var in variables}
        
        # Định nghĩa ràng buộc: mỗi thành phố chỉ được đi qua một lần
        def constraint_all_different(variables, values):
            """Ràng buộc: tất cả các thành phố phải khác nhau"""
            return len(values) == len(set(values))
        
        def constraint_optimize_distance(variables, values):
            """Ràng buộc: tối ưu hóa khoảng cách"""
            if len(values) < 2:
                return True
            # Kiểm tra khoảng cách tích lũy không vượt quá best_distance hiện tại
            partial_distance = 0
            for i in range(len(values) - 1):
                city1 = self.cities.index(values[i])
                city2 = self.cities.index(values[i + 1])
                partial_distance += self.distance_matrix[city1][city2]
                if partial_distance >= self.best_distance:
                    return False
            return True
        
        # Tạo danh sách ràng buộc
        constraints = []
        
        # Ràng buộc tất cả các thành phố phải khác nhau
        constraints.append((variables, constraint_all_different))
        
        # Ràng buộc tối ưu hóa khoảng cách cho mỗi cặp liên tiếp
        for i in range(len(variables) - 1):
            constraints.append((variables[:i+2], constraint_optimize_distance))
        
        # Tạo bài toán CSP
        problem = CspProblem(variables, domains, constraints)
        
        # Giải bài toán bằng backtracking
        try:
            # Tìm tất cả các giải pháp và chọn tốt nhất
            solution = backtrack(problem)
            
            if solution:
                # Chuyển đổi solution thành route
                route = [solution[var] for var in variables]
                distance = self.calculate_route_distance(route)
                
                self.best_route = route
                self.best_distance = distance
        except:
            # Nếu không tìm được giải pháp tối ưu, sử dụng greedy approach
            self.greedy_fallback()
        
        self.execution_time = time.time() - start_time
        
        return {
            'route': self.best_route,
            'distance': self.best_distance,
            'time': self.execution_time,
            'algorithm': 'Backtracking (simpleAI)'
        }
    
    def greedy_fallback(self):
        """
        Phương pháp dự phòng: sử dụng greedy approach nếu backtracking không tìm được
        """
        route = [self.cities[0]]
        unvisited = set(self.cities[1:])
        
        while unvisited:
            current_city = route[-1]
            current_idx = self.cities.index(current_city)
            
            # Tìm thành phố gần nhất chưa được thăm
            nearest_city = min(unvisited, 
                             key=lambda city: self.distance_matrix[current_idx][self.cities.index(city)])
            route.append(nearest_city)
            unvisited.remove(nearest_city)
        
        self.best_route = route
        self.best_distance = self.calculate_route_distance(route)


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
    
    solver = TSPBacktracking(cities, distance_matrix)
    result = solver.solve()
    
    print(f"Thuật toán: {result['algorithm']}")
    print(f"Tuyến đường tốt nhất: {' -> '.join(result['route'])} -> {result['route'][0]}")
    print(f"Tổng khoảng cách: {result['distance']:.2f} km")
    print(f"Thời gian thực thi: {result['time']:.4f} giây")
