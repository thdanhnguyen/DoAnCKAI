"""
HTTP Server for TSP Application
Server đơn giản sử dụng thư viện chuẩn của Python
"""

import http.server
import socketserver
import json
import os
import sys
from urllib.parse import urlparse, parse_qs
import numpy as np
from math import radians, cos, sin, asin, sqrt

# Import các module giải thuật
from tsp_backtracking import TSPBacktracking
from tsp_aco import TSP_ACO

def haversine(lon1, lat1, lon2, lat2):
    """
    Tính khoảng cách giữa 2 điểm trên Trái Đất (km)
    Sử dụng công thức Haversine
    """
    # Convert to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in kilometers
    r = 6371
    
    return c * r

def build_distance_matrix(cities, coords):
    """
    Xây dựng ma trận khoảng cách từ tọa độ các thành phố
    """
    n = len(cities)
    matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            if i != j:
                city_i = cities[i]
                city_j = cities[j]
                lon1, lat1 = coords[city_i]
                lon2, lat2 = coords[city_j]
                matrix[i][j] = haversine(lon1, lat1, lon2, lat2)
    
    return matrix

# Dữ liệu mặc định
DEFAULT_CITIES = ['Hà Nội', 'Hải Phòng', 'Đà Nẵng', 'Huế', 'TP.HCM', 'Cần Thơ', 'Nha Trang', 'Đà Lạt']
DEFAULT_COORDS = {
    'Hà Nội': [105.8, 21.0],
    'Hải Phòng': [106.7, 20.8],
    'Đà Nẵng': [108.2, 16.0],
    'Huế': [107.6, 16.5],
    'TP.HCM': [106.7, 10.8],
    'Cần Thơ': [105.8, 10.0],
    'Nha Trang': [109.2, 12.2],
    'Đà Lạt': [108.4, 11.9]
}

class TSPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom request handler cho TSP application"""
    
    def do_GET(self):
        """Xử lý GET requests"""
        if self.path == '/' or self.path == '/index.html':
            self.path = '/index.html'
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        elif self.path == '/styles.css':
            self.path = '/styles.css'
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        elif self.path == '/script.js':
            self.path = '/script.js'
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
        else:
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
    
    def do_POST(self):
        """Xử lý POST requests"""
        if self.path == '/solve':
            self.handle_solve()
        else:
            self.send_error(404, "Not Found")
    
    def handle_solve(self):
        """Xử lý request giải bài toán TSP"""
        try:
            # Đọc dữ liệu từ request
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            params = json.loads(post_data.decode('utf-8'))
            
            cities = params.get('cities', DEFAULT_CITIES)
            coords = params.get('coords', DEFAULT_COORDS)
            
            distance_matrix = build_distance_matrix(cities, coords)
            
            print("\n" + "="*60)
            print("Nhận được yêu cầu giải bài toán TSP")
            print("="*60)
            print(f"Số thành phố: {len(cities)}")
            print(f"Danh sách: {', '.join(cities)}")
            print(f"Tham số ACO: n_ants={params.get('n_ants', 30)}, "
                  f"n_iterations={params.get('n_iterations', 100)}, "
                  f"alpha={params.get('alpha', 1.0)}, "
                  f"beta={params.get('beta', 2.0)}")
            print()
            
            # Giải bằng Backtracking
            print("Đang giải bằng Backtracking...")
            bt_solver = TSPBacktracking(cities, distance_matrix)
            bt_result = bt_solver.solve()
            print(f"✓ Backtracking hoàn thành: {bt_result['distance']:.2f} km trong {bt_result['time']:.4f}s")
            
            # Giải bằng ACO
            print("\nĐang giải bằng ACO...")
            aco_solver = TSP_ACO(
                cities, 
                distance_matrix,
                n_ants=params.get('n_ants', 30),
                n_iterations=params.get('n_iterations', 100),
                alpha=params.get('alpha', 1.0),
                beta=params.get('beta', 2.0),
                evaporation_rate=params.get('evaporation', 0.5),  # Sửa tên tham số từ evaporation_rate thành evaporation để khớp với frontend
                q=params.get('q', 100)
            )
            aco_result = aco_solver.solve()
            print(f"✓ ACO hoàn thành: {aco_result['distance']:.2f} km trong {aco_result['time']:.4f}s")
            
            # Chuẩn bị response
            response_data = {
                'backtracking': {
                    'route': bt_result['route'],
                    'distance': float(bt_result['distance']),
                    'time': float(bt_result['time']),
                    'algorithm': bt_result['algorithm']
                },
                'aco': {
                    'route': aco_result['route'],
                    'distance': float(aco_result['distance']),
                    'time': float(aco_result['time']),
                    'algorithm': aco_result['algorithm'],
                    'convergence': [float(x) for x in aco_result['convergence']]
                }
            }
            
            # Gửi response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
            
            print("\n✅ Đã gửi kết quả về client")
            print("="*60 + "\n")
            
        except Exception as e:
            print(f"\n❌ Lỗi: {str(e)}\n")
            import traceback
            traceback.print_exc()
            self.send_error(500, f"Internal Server Error: {str(e)}")
    
    def do_OPTIONS(self):
        """Xử lý OPTIONS requests (CORS preflight)"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        """Override để custom log messages"""
        # Chỉ log các request quan trọng
        if args and isinstance(args[0], str) and '/solve' in args[0]:
            sys.stderr.write("%s - [%s] %s\n" %
                           (self.address_string(),
                            self.log_date_time_string(),
                            format%args))

def run_server(port=8000):
    """Chạy HTTP server"""
    # Chuyển đến thư mục gốc của project
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)
    
    print("\n" + "="*60)
    print("🚀 TSP SOLVER SERVER")
    print("="*60)
    print(f"📂 Thư mục: {os.getcwd()}")
    print(f"🌐 Server đang chạy tại: http://localhost:{port}")
    print(f"🔗 Mở trình duyệt và truy cập: http://localhost:{port}")
    print("="*60)
    print("Nhấn Ctrl+C để dừng server\n")
    
    try:
        with socketserver.TCPServer(("", port), TSPRequestHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n" + "="*60)
        print("🛑 Server đã dừng")
        print("="*60 + "\n")
        sys.exit(0)

if __name__ == "__main__":
    # Lấy port từ command line hoặc dùng mặc định 8000
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Port không hợp lệ, sử dụng port mặc định 8000")
    
    run_server(port)
