"""
Travelling Salesman Problem - GUI Application with Tkinter and Matplotlib
Giao diện GUI Tkinter để so sánh Backtracking và ACO với biểu đồ Matplotlib
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import numpy as np
from tsp_backtracking import TSPBacktracking
from tsp_aco import TSP_ACO
import csv
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading

class TSPGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Travelling Salesman Problem - Backtracking & ACO")
        self.root.geometry("1600x900")
        
        self.cities = ['Hà Nội', 'Hải Phòng', 'Đà Nẵng', 'TP.HCM', 'Cần Thơ']
        self.coordinates = [
            (21.0285, 105.8542), (20.8449, 106.6881), (16.0544, 108.2022),
            (10.7769, 106.6964), (10.0379, 105.7869)
        ]
        self.distance_matrix = np.array([
            [0, 120, 764, 1710, 1840],
            [120, 0, 840, 1830, 1960],
            [764, 840, 0, 964, 1094],
            [1710, 1830, 964, 0, 169],
            [1840, 1960, 1094, 169, 0]
        ])
        
        self.result_backtracking = None
        self.result_aco = None
        self.normalized_coordinates = None
        
        self.create_widgets()
    
    def create_widgets(self):
        """Tạo giao diện"""
        # Main container
        main_container = ttk.PanedWindow(self.root, orient='horizontal')
        main_container.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Left panel - Input & Parameters
        left_panel = ttk.Frame(main_container)
        main_container.add(left_panel, weight=1)
        self.create_left_panel(left_panel)
        
        # Right panel - Results & Visualization
        right_panel = ttk.Frame(main_container)
        main_container.add(right_panel, weight=2)
        self.create_right_panel(right_panel)
    
    def create_left_panel(self, parent):
        """Tạo panel bên trái"""
        # Notebook cho các tab
        notebook = ttk.Notebook(parent)
        notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Tab 1: Input Data
        input_frame = ttk.Frame(notebook)
        notebook.add(input_frame, text='Nhập dữ liệu')
        self.create_input_tab(input_frame)
        
        # Tab 2: Algorithm Parameters
        params_frame = ttk.Frame(notebook)
        notebook.add(params_frame, text='Tham số')
        self.create_params_tab(params_frame)
    
    def create_input_tab(self, parent):
        """Tạo tab nhập dữ liệu"""
        # Sub-tabs
        sub_notebook = ttk.Notebook(parent)
        sub_notebook.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Default cities tab
        default_tab = ttk.Frame(sub_notebook)
        sub_notebook.add(default_tab, text='Mặc định')
        
        ttk.Button(default_tab, text='Sử dụng 5 thành phố mặc định', 
                  command=self.use_default_cities).pack(pady=5)
        
        default_text = scrolledtext.ScrolledText(default_tab, height=10, width=40)
        default_text.pack(fill='both', expand=True, padx=5, pady=5)
        default_text.insert('end', self.format_cities())
        default_text.config(state='disabled')
        
        # Manual input tab
        manual_tab = ttk.Frame(sub_notebook)
        sub_notebook.add(manual_tab, text='Nhập tay')
        
        frame_manual = ttk.Frame(manual_tab)
        frame_manual.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(frame_manual, text='Tên:').grid(row=0, column=0)
        self.entry_city_name = ttk.Entry(frame_manual, width=15)
        self.entry_city_name.grid(row=0, column=1, padx=5)
        
        ttk.Label(frame_manual, text='Kinh độ:').grid(row=1, column=0)
        self.entry_lon = ttk.Entry(frame_manual, width=15)
        self.entry_lon.grid(row=1, column=1, padx=5)
        
        ttk.Label(frame_manual, text='Vĩ độ:').grid(row=2, column=0)
        self.entry_lat = ttk.Entry(frame_manual, width=15)
        self.entry_lat.grid(row=2, column=1, padx=5)
        
        button_frame = ttk.Frame(manual_tab)
        button_frame.pack(fill='x', padx=5, pady=5)
        ttk.Button(button_frame, text='Thêm', command=self.add_city).pack(side='left', padx=2)
        ttk.Button(button_frame, text='Xóa cuối', command=self.remove_city).pack(side='left', padx=2)
        ttk.Button(button_frame, text='Xóa tất cả', command=self.clear_cities).pack(side='left', padx=2)
        
        self.text_manual_cities = scrolledtext.ScrolledText(manual_tab, height=8, width=40)
        self.text_manual_cities.pack(fill='both', expand=True, padx=5, pady=5)
        
        # CSV tab
        csv_tab = ttk.Frame(sub_notebook)
        sub_notebook.add(csv_tab, text='File CSV')
        
        frame_csv = ttk.Frame(csv_tab)
        frame_csv.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(frame_csv, text='File:').pack(side='left')
        self.entry_csv = ttk.Entry(frame_csv, width=30)
        self.entry_csv.pack(side='left', padx=5)
        ttk.Button(frame_csv, text='Browse', command=self.browse_csv).pack(side='left', padx=2)
        ttk.Button(frame_csv, text='Load', command=self.load_csv).pack(side='left', padx=2)
        
        self.text_csv_cities = scrolledtext.ScrolledText(csv_tab, height=12, width=40)
        self.text_csv_cities.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Random tab
        random_tab = ttk.Frame(sub_notebook)
        sub_notebook.add(random_tab, text='Random')
        
        frame_random = ttk.Frame(random_tab)
        frame_random.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(frame_random, text='N (5-15):').grid(row=0, column=0)
        self.spin_n_cities = ttk.Spinbox(frame_random, from_=5, to=15, width=10)
        self.spin_n_cities.set(10)
        self.spin_n_cities.grid(row=0, column=1, padx=5)
        
        ttk.Button(frame_random, text='Random (5-15 thành phố)', 
                  command=self.generate_random_cities).grid(row=0, column=2, padx=5)
        
        self.text_random_cities = scrolledtext.ScrolledText(random_tab, height=12, width=40)
        self.text_random_cities.pack(fill='both', expand=True, padx=5, pady=5)
    
    def create_params_tab(self, parent):
        """Tạo tab tham số"""
        # Backtracking parameters
        bt_frame = ttk.LabelFrame(parent, text='Tham số BACKTRACKING', padding=10)
        bt_frame.pack(fill='x', padx=5, pady=5)
        
        ttk.Label(bt_frame, text='Backtracking không có tham số điều chỉnh - Tìm kiếm toàn bộ không gian').pack()
        ttk.Label(bt_frame, text='Độ phức tạp: O(n!)').pack()
        
        # ACO parameters
        aco_frame = ttk.LabelFrame(parent, text='Tham số ACO', padding=10)
        aco_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Number of ants
        frame1 = ttk.Frame(aco_frame)
        frame1.pack(fill='x', pady=5)
        ttk.Label(frame1, text='Số kiến (5-50):', width=20).pack(side='left')
        self.spin_ants = ttk.Spinbox(frame1, from_=5, to=50, width=10)
        self.spin_ants.set(20)
        self.spin_ants.pack(side='left', padx=5)
        
        # Iterations
        frame2 = ttk.Frame(aco_frame)
        frame2.pack(fill='x', pady=5)
        ttk.Label(frame2, text='Iterations (10-200):', width=20).pack(side='left')
        self.spin_iter = ttk.Spinbox(frame2, from_=10, to=200, width=10)
        self.spin_iter.set(50)
        self.spin_iter.pack(side='left', padx=5)
        
        # Alpha
        frame3 = ttk.Frame(aco_frame)
        frame3.pack(fill='x', pady=5)
        ttk.Label(frame3, text='Alpha (0.1-3.0):', width=20).pack(side='left')
        self.spin_alpha = ttk.Spinbox(frame3, from_=0.1, to=3.0, increment=0.1, width=10)
        self.spin_alpha.set(1.0)
        self.spin_alpha.pack(side='left', padx=5)
        
        # Beta
        frame4 = ttk.Frame(aco_frame)
        frame4.pack(fill='x', pady=5)
        ttk.Label(frame4, text='Beta (0.1-5.0):', width=20).pack(side='left')
        self.spin_beta = ttk.Spinbox(frame4, from_=0.1, to=5.0, increment=0.1, width=10)
        self.spin_beta.set(2.0)
        self.spin_beta.pack(side='left', padx=5)
        
        # Evaporation rate
        frame5 = ttk.Frame(aco_frame)
        frame5.pack(fill='x', pady=5)
        ttk.Label(frame5, text='Evaporation (0.1-0.9):', width=20).pack(side='left')
        self.spin_evap = ttk.Spinbox(frame5, from_=0.1, to=0.9, increment=0.1, width=10)
        self.spin_evap.set(0.5)
        self.spin_evap.pack(side='left', padx=5)
        
        # Q constant
        frame6 = ttk.Frame(aco_frame)
        frame6.pack(fill='x', pady=5)
        ttk.Label(frame6, text='Q constant (10-500):', width=20).pack(side='left')
        self.spin_q = ttk.Spinbox(frame6, from_=10, to=500, width=10)
        self.spin_q.set(100)
        self.spin_q.pack(side='left', padx=5)
        
        # Solve buttons
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill='x', padx=5, pady=10)
        
        ttk.Button(button_frame, text='GIẢI BÀI TOÁN', 
                  command=self.solve_problem).pack(side='left', padx=5)
        ttk.Button(button_frame, text='Xem biểu đồ', 
                  command=self.show_comparison_chart).pack(side='left', padx=5)
        ttk.Button(button_frame, text='In chi tiết', 
                  command=self.print_details).pack(side='left', padx=5)
    
    def create_right_panel(self, parent):
        """Tạo panel bên phải"""
        notebook = ttk.Notebook(parent)
        notebook.pack(fill='both', expand=True)
        
        # Results tab
        results_frame = ttk.Frame(notebook)
        notebook.add(results_frame, text='Kết quả')
        
        self.text_results = scrolledtext.ScrolledText(results_frame, height=20, width=80)
        self.text_results.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Chart tab
        self.chart_frame = ttk.Frame(notebook)
        notebook.add(self.chart_frame, text='Biểu đồ')
    
    def use_default_cities(self):
        """Sử dụng dữ liệu mặc định"""
        self.cities = ['Hà Nội', 'Hải Phòng', 'Đà Nẵng', 'TP.HCM', 'Cần Thơ']
        self.coordinates = [
            (21.0285, 105.8542), (20.8449, 106.6881), (16.0544, 108.2022),
            (10.7769, 106.6964), (10.0379, 105.7869)
        ]
        self.normalize_coordinates()
        self.distance_matrix = self.calculate_distance_matrix()
        messagebox.showinfo('Thành công', f'Đã load {len(self.cities)} thành phố mặc định')
    
    def add_city(self):
        """Thêm thành phố"""
        name = self.entry_city_name.get()
        lon = self.entry_lon.get()
        lat = self.entry_lat.get()
        
        if not name or not lon or not lat:
            messagebox.showerror('Lỗi', 'Nhập đầy đủ thông tin!')
            return
        
        try:
            lon, lat = float(lon), float(lat)
            self.cities.append(name)
            self.coordinates.append((lat, lon))
            self.normalize_coordinates()
            self.distance_matrix = self.calculate_distance_matrix()
            
            self.entry_city_name.delete(0, 'end')
            self.entry_lon.delete(0, 'end')
            self.entry_lat.delete(0, 'end')
            
            self.update_manual_cities_display()
            messagebox.showinfo('Thành công', f'Đã thêm {name}')
        except ValueError:
            messagebox.showerror('Lỗi', 'Tọa độ phải là số!')
    
    def remove_city(self):
        """Xóa thành phố cuối"""
        if self.cities:
            removed = self.cities.pop()
            self.coordinates.pop()
            self.normalize_coordinates()
            if self.cities:
                self.distance_matrix = self.calculate_distance_matrix()
            self.update_manual_cities_display()
    
    def clear_cities(self):
        """Xóa tất cả thành phố"""
        self.cities = []
        self.coordinates = []
        self.text_manual_cities.config(state='normal')
        self.text_manual_cities.delete('1.0', 'end')
        self.text_manual_cities.config(state='disabled')
    
    def browse_csv(self):
        """Chọn file CSV"""
        file = filedialog.askopenfilename(filetypes=[('CSV', '*.csv')])
        if file:
            self.entry_csv.delete(0, 'end')
            self.entry_csv.insert(0, file)
    
    def load_csv(self):
        """Load file CSV"""
        file = self.entry_csv.get()
        if not file or not os.path.exists(file):
            messagebox.showerror('Lỗi', 'Chọn file CSV hợp lệ!')
            return
        
        try:
            self.cities = []
            self.coordinates = []
            
            with open(file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header
                for row in reader:
                    if len(row) >= 3:
                        name, lon, lat = row[0], float(row[1]), float(row[2])
                        self.cities.append(name)
                        self.coordinates.append((lat, lon))
            
            if len(self.cities) > 15:
                messagebox.showwarning('Cảnh báo', 
                    f'CSV có {len(self.cities)} thành phố.\n'
                    f'Backtracking chỉ hoạt động tối đa 15 thành phố.\n'
                    f'Chỉ sử dụng tối đa 15 thành phố đầu tiên.')
                self.cities = self.cities[:15]
                self.coordinates = self.coordinates[:15]
            
            self.normalize_coordinates()
            self.distance_matrix = self.calculate_distance_matrix()
            self.update_csv_cities_display()
            messagebox.showinfo('Thành công', f'Đã load {len(self.cities)} thành phố từ CSV')
        except Exception as e:
            messagebox.showerror('Lỗi', f'Lỗi load CSV: {str(e)}')
    
    def generate_random_cities(self):
        """Sinh ngẫu nhiên thành phố (5-15 thành phố)"""
        n = int(self.spin_n_cities.get())
        self.cities = [f'Thành phố {i+1}' for i in range(n)]
        self.coordinates = [(np.random.uniform(16, 22), np.random.uniform(103, 108)) for _ in range(n)]
        
        self.normalize_coordinates()
        self.distance_matrix = self.calculate_distance_matrix()
        
        text = f'Sinh {n} thành phố ngẫu nhiên:\n\n'
        for i, city in enumerate(self.cities):
            lat, lon = self.coordinates[i]
            text += f'{i+1}. {city} (Lat: {lat:.2f}, Lon: {lon:.2f})\n'
        
        self.text_random_cities.config(state='normal')
        self.text_random_cities.delete('1.0', 'end')
        self.text_random_cities.insert('end', text)
        self.text_random_cities.config(state='disabled')
        
        messagebox.showinfo('Thành công', f'Sinh {n} thành phố ngẫu nhiên')
    
    def update_manual_cities_display(self):
        """Cập nhật hiển thị danh sách thành phố nhập tay"""
        text = f'Danh sách ({len(self.cities)} thành phố):\n\n'
        for i, city in enumerate(self.cities):
            text += f'{i+1}. {city}\n'
        
        self.text_manual_cities.config(state='normal')
        self.text_manual_cities.delete('1.0', 'end')
        self.text_manual_cities.insert('end', text)
        self.text_manual_cities.config(state='disabled')
    
    def update_csv_cities_display(self):
        """Cập nhật hiển thị danh sách thành phố từ CSV"""
        text = f'Tổng {len(self.cities)} thành phố từ CSV:\n\n'
        for i, city in enumerate(self.cities[:10]):
            lat, lon = self.coordinates[i]
            text += f'{i+1}. {city} (Lat: {lat:.4f}, Lon: {lon:.4f})\n'
        if len(self.cities) > 10:
            text += f'... và {len(self.cities)-10} thành phố khác\n'
        
        self.text_csv_cities.config(state='normal')
        self.text_csv_cities.delete('1.0', 'end')
        self.text_csv_cities.insert('end', text)
        self.text_csv_cities.config(state='disabled')
    
    def format_cities(self):
        """Format danh sách thành phố"""
        text = 'Danh sách 5 thành phố mặc định:\n\n'
        for i, city in enumerate(self.cities):
            text += f'{i+1}. {city}\n'
        return text
    
    def normalize_coordinates(self):
        """Chuẩn hóa tọa độ về [0, 100]"""
        if not self.coordinates:
            return
        
        coords = np.array(self.coordinates)
        lat_min, lat_max = coords[:, 0].min(), coords[:, 0].max()
        lon_min, lon_max = coords[:, 1].min(), coords[:, 1].max()
        
        lat_range = lat_max - lat_min if lat_max > lat_min else 1
        lon_range = lon_max - lon_min if lon_max > lon_min else 1
        
        self.normalized_coordinates = [
            ((lat - lat_min) / lat_range * 100 if lat_range > 0 else 50,
             (lon - lon_min) / lon_range * 100 if lon_range > 0 else 50)
            for lat, lon in self.coordinates
        ]
    
    def calculate_distance_matrix(self):
        """Tính ma trận khoảng cách"""
        n = len(self.cities)
        matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(i+1, n):
                lat1, lon1 = self.normalized_coordinates[i]
                lat2, lon2 = self.normalized_coordinates[j]
                dist = np.sqrt((lat2-lat1)**2 + (lon2-lon1)**2)
                matrix[i][j] = dist
                matrix[j][i] = dist
        
        return matrix
    
    def solve_problem(self):
        """Giải bài toán"""
        if len(self.cities) < 3:
            messagebox.showerror('Lỗi', 'Cần ít nhất 3 thành phố!')
            return
        
        if len(self.cities) > 15:
            messagebox.showerror('Lỗi', f'Tối đa 15 thành phố (hiện có {len(self.cities)})')
            return
        
        # Lấy tham số
        n_ants = int(self.spin_ants.get())
        n_iter = int(self.spin_iter.get())
        alpha = float(self.spin_alpha.get())
        beta = float(self.spin_beta.get())
        evap = float(self.spin_evap.get())
        q = float(self.spin_q.get())
        
        self.text_results.config(state='normal')
        self.text_results.delete('1.0', 'end')
        self.text_results.insert('end', 'Đang giải bài toán...\n')
        self.text_results.config(state='disabled')
        self.root.update()
        
        # Giải Backtracking
        bt_solver = TSPBacktracking(self.cities, self.distance_matrix)
        self.result_backtracking = bt_solver.solve(verbose=False)
        
        # Giải ACO
        aco_solver = TSP_ACO(self.cities, self.distance_matrix,
                            n_ants=n_ants, n_iterations=n_iter,
                            alpha=alpha, beta=beta, evaporation_rate=evap, q=q)
        self.result_aco = aco_solver.solve(verbose=False)
        
        self.aco_solver = aco_solver  # Lưu để vẽ biểu đồ
        
        # Hiển thị kết quả
        self.display_results()
    
    def display_results(self):
        """Hiển thị kết quả"""
        text = "=" * 100 + "\n"
        text += "KẾT QUẢ SO SÁNH BACKTRACKING VÀ ACO\n"
        text += "=" * 100 + "\n\n"
        
        text += f"Số thành phố: {len(self.cities)}\n"
        text += f"Danh sách: {', '.join(self.cities[:5])}"
        if len(self.cities) > 5:
            text += f", ... và {len(self.cities)-5} thành phố khác"
        text += "\n\n"
        
        # Backtracking
        text += "1. BACKTRACKING (Quay lui)\n"
        text += "-" * 100 + "\n"
        text += f"Tuyến đường: {' → '.join(self.result_backtracking['route'])} → {self.result_backtracking['route'][0]}\n"
        text += f"Khoảng cách: {self.result_backtracking['distance']:.4f} km\n"
        text += f"Thời gian: {self.result_backtracking['time']:.6f} giây\n"
        text += f"Độ phức tạp: O(n!)\n"
        text += f"Số tuyến đường khám phá: {self.result_backtracking['explored_routes']}\n\n"
        
        # ACO
        text += "2. ACO (Ant Colony Optimization)\n"
        text += "-" * 100 + "\n"
        text += f"Tuyến đường: {' → '.join(self.result_aco['route'])} → {self.result_aco['route'][0]}\n"
        text += f"Khoảng cách: {self.result_aco['distance']:.4f} km\n"
        text += f"Thời gian: {self.result_aco['time']:.6f} giây\n"
        text += f"Độ phức tạp: O(n² × m × iterations)\n\n"
        
        text += "THAM SỐ ACO:\n"
        text += f"  Kiến: {self.aco_solver.n_ants}, Iterations: {self.aco_solver.n_iterations}\n"
        text += f"  Alpha: {self.aco_solver.alpha}, Beta: {self.aco_solver.beta}\n"
        text += f"  Evaporation: {self.aco_solver.evaporation_rate}, Q: {self.aco_solver.q}\n\n"
        
        # So sánh
        text += "3. SO SÁNH\n"
        text += "-" * 100 + "\n"
        
        dist_diff = abs(self.result_backtracking['distance'] - self.result_aco['distance'])
        if self.result_backtracking['distance'] > 0:
            percent_diff = (dist_diff / self.result_backtracking['distance']) * 100
        else:
            percent_diff = 0
        
        text += f"Khoảng cách - BT: {self.result_backtracking['distance']:.4f} / ACO: {self.result_aco['distance']:.4f}\n"
        text += f"Chênh lệch: {dist_diff:.4f} ({percent_diff:.2f}%)\n"
        
        if self.result_backtracking['distance'] < self.result_aco['distance']:
            text += f"✓ Backtracking tốt hơn {percent_diff:.2f}%\n\n"
        else:
            text += f"✓ ACO tốt hơn {percent_diff:.2f}%\n\n"
        
        time_diff = abs(self.result_backtracking['time'] - self.result_aco['time'])
        if self.result_backtracking['time'] > 0:
            time_percent = (time_diff / self.result_backtracking['time']) * 100
        else:
            time_percent = 0
        
        text += f"Thời gian - BT: {self.result_backtracking['time']:.6f}s / ACO: {self.result_aco['time']:.6f}s\n"
        text += f"Chênh lệch: {time_diff:.6f}s ({time_percent:.2f}%)\n"
        
        self.text_results.config(state='normal')
        self.text_results.delete('1.0', 'end')
        self.text_results.insert('end', text)
        self.text_results.config(state='disabled')
        
        messagebox.showinfo('Thành công', 'Đã giải xong! Nhấn "Xem biểu đồ" để xem chi tiết.')
    
    def show_comparison_chart(self):
        """Hiển thị biểu đồ so sánh"""
        if not self.result_backtracking or not self.result_aco:
            messagebox.showerror('Lỗi', 'Giải bài toán trước!')
            return
        
        # Xóa biểu đồ cũ
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        fig = Figure(figsize=(12, 6), dpi=100)
        
        # Biểu đồ 1: So sánh khoảng cách
        ax1 = fig.add_subplot(121)
        algorithms = ['Backtracking', 'ACO']
        distances = [self.result_backtracking['distance'], self.result_aco['distance']]
        colors = ['#FF6B6B', '#4ECDC4']
        bars = ax1.bar(algorithms, distances, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
        ax1.set_ylabel('Khoảng cách (km)', fontsize=12)
        ax1.set_title('So sánh khoảng cách tuyến đường', fontsize=12, fontweight='bold')
        ax1.grid(axis='y', alpha=0.3)
        
        for bar, dist in zip(bars, distances):
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height,
                    f'{dist:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        # Biểu đồ 2: Quá trình hội tụ ACO
        ax2 = fig.add_subplot(122)
        iterations = range(1, len(self.aco_solver.convergence_data) + 1)
        ax2.plot(iterations, self.aco_solver.convergence_data, 'o-', 
                color='#4ECDC4', linewidth=2, markersize=4)
        ax2.axhline(y=self.result_backtracking['distance'], color='#FF6B6B', 
                   linestyle='--', linewidth=2, label=f'Backtracking: {self.result_backtracking["distance"]:.2f}')
        ax2.set_xlabel('Iteration', fontsize=12)
        ax2.set_ylabel('Khoảng cách tốt nhất (km)', fontsize=12)
        ax2.set_title('Quá trình hội tụ ACO', fontsize=12, fontweight='bold')
        ax2.legend()
        ax2.grid(alpha=0.3)
        
        fig.tight_layout()
        
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def print_details(self):
        """In chi tiết từng bước"""
        if not self.result_backtracking or not self.result_aco:
            messagebox.showerror('Lỗi', 'Giải bài toán trước!')
            return
        
        output = "=" * 120 + "\n"
        output += "CHI TIẾT TỪNG BƯỚC CỦA CÁC THUẬT TOÁN\n"
        output += "=" * 120 + "\n\n"
        
        output += "BACKTRACKING - CÁC BƯỚC KHÁM PHÁ:\n"
        output += "-" * 120 + "\n"
        if self.result_backtracking['steps']:
            for step in self.result_backtracking['steps'][:50]:
                output += step + "\n"
            if len(self.result_backtracking['steps']) > 50:
                output += f"\n... và {len(self.result_backtracking['steps'])-50} bước khác ...\n"
        else:
            output += "Không có chi tiết bước\n"
        
        output += "\n" + "=" * 120 + "\n"
        output += "ACO - CÁC BƯỚC HỘI TỤ:\n"
        output += "-" * 120 + "\n"
        if self.result_aco['steps']:
            for step in self.result_aco['steps']:
                output += step + "\n"
        else:
            output += "Không có chi tiết bước\n"
        
        # Tạo cửa sổ mới để hiển thị chi tiết
        detail_window = tk.Toplevel(self.root)
        detail_window.title("Chi tiết từng bước")
        detail_window.geometry("1200x600")
        
        detail_text = scrolledtext.ScrolledText(detail_window, height=30, width=140)
        detail_text.pack(fill='both', expand=True, padx=5, pady=5)
        detail_text.insert('end', output)
        detail_text.config(state='disabled')

def main():
    root = tk.Tk()
    gui = TSPGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
