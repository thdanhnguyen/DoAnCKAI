"""
Travelling Salesman Problem - Backtracking Solution (custom implementation)
Giải bài toán người du lịch bằng thuật toán quay lui (không dùng simpleAI)
"""

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
        Giải bài toán TSP bằng Backtracking (tự triển khai)
        Thuật toán: Depth-first search (hoặc brute-force với pruning theo best_distance)
        """
        start_time = time.time()
        # Implement a minimal CSP-style backtracking framework here so code
        # explicitly uses variables, domains, constraints and an assignment.

        # Variables: position_0 ... position_{n-1}
        variables = [f'position_{i}' for i in range(self.n_cities)]

        # Domains: all cities for each variable
        domains = {var: list(self.cities) for var in variables}

        # Constraints: functions that accept (assignment) partial dict and return True/False
        def all_different(assignment):
            # All assigned values must be unique
            vals = list(assignment.values())
            return len(vals) == len(set(vals))

        def partial_distance_constraint(assignment):
            # For any consecutive assigned positions, the partial accumulated distance
            # should not exceed the current best distance (pruning)
            # Build ordered list of assigned positions by position index
            if not assignment:
                return True
            # Extract assigned positions and their numeric indices
            assigned = []
            for var, val in assignment.items():
                idx = int(var.split('_')[1])
                assigned.append((idx, val))
            assigned.sort()

            # compute partial distance along the assigned prefix
            partial = 0
            for i in range(len(assigned) - 1):
                a_city = assigned[i][1]
                b_city = assigned[i+1][1]
                a_idx = self.cities.index(a_city)
                b_idx = self.cities.index(b_city)
                partial += self.distance_matrix[a_idx][b_idx]
                if partial >= self.best_distance:
                    return False
            return True

        constraints = [all_different, partial_distance_constraint]

        # Backtracking driver: assign variables in order
        assignment = {}

        def is_consistent(assignment):
            # Evaluate all constraints on the current partial assignment
            for c in constraints:
                try:
                    if not c(assignment):
                        return False
                except Exception:
                    return False
            return True

        def backtrack_var(idx):
            # idx: index of variable to assign
            if idx >= len(variables):
                # full assignment -> evaluate total distance including return-to-start
                route = [assignment[var] for var in variables]
                dist = self.calculate_route_distance(route)
                if dist < self.best_distance:
                    self.best_distance = dist
                    self.best_route = route.copy()
                return

            var = variables[idx]
            for value in domains[var]:
                # try assign
                assignment[var] = value
                if is_consistent(assignment):
                    backtrack_var(idx+1)
                # undo
                assignment.pop(var, None)

        # To reduce symmetric solutions, fix starting position to first city
        assignment[variables[0]] = self.cities[0]
        if is_consistent(assignment):
            backtrack_var(1)
        
        self.execution_time = time.time() - start_time

        return {
            'route': self.best_route,
            'distance': self.best_distance,
            'time': self.execution_time,
            'algorithm': 'Backtracking (custom)'
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
