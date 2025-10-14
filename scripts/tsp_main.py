"""
Travelling Salesman Problem - Main Application
Ứng dụng chính để giải và so sánh các thuật toán TSP
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
import io

# Import các module giải thuật
from tsp_backtracking import TSPBacktracking
from tsp_aco import TSP_ACO

class TSPApplication:
    def __init__(self, root):
        self.root = root
        self.root.title("Giải Bài Toán Người Du Lịch (TSP) - Backtracking & ACO")
        self.root.geometry("1400x900")
        self.root.configure(bg='#0a0a0a')
        
        # Dữ liệu mặc định
        self.cities = ['Hà Nội', 'Hải Phòng', 'Đà Nẵng', 'Huế', 'TP.HCM', 'Cần Thơ', 'Nha Trang', 'Đà Lạt']
        self.distance_matrix = np.array([
            [0, 120, 764, 654, 1710, 1840, 1278, 1481],
            [120, 0, 840, 730, 1830, 1960, 1354, 1557],
            [764, 840, 0, 108, 964, 1094, 541, 661],
            [654, 730, 108, 0, 1071, 1201, 649, 769],
            [1710, 1830, 964, 1071, 0, 169, 431, 308],
            [1840, 1960, 1094, 1201, 169, 0, 600, 477],
            [1278, 1354, 541, 649, 431, 600, 0, 137],
            [1481, 1557, 661, 769, 308, 477, 137, 0]
        ])
        
        # Tọa độ để vẽ (giả lập vị trí địa lý)
        self.city_coords = {
            'Hà Nội': (105.8, 21.0),
            'Hải Phòng': (106.7, 20.8),
            'Đà Nẵng': (108.2, 16.0),
            'Huế': (107.6, 16.5),
            'TP.HCM': (106.7, 10.8),
            'Cần Thơ': (105.8, 10.0),
            'Nha Trang': (109.2, 12.2),
            'Đà Lạt': (108.4, 11.9)
        }
        
        self.results = {}
        
        self.setup_ui()
        
    def setup_ui(self):
        """Thiết lập giao diện người dùng"""
        # Style configuration
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        bg_color = '#0a0a0a'
        fg_color = '#ffffff'
        accent_color = '#f7d046'
        secondary_bg = '#1a1a1a'
        
        style.configure('Title.TLabel', background=bg_color, foreground=fg_color, 
                       font=('Arial', 24, 'bold'))
        style.configure('Subtitle.TLabel', background=bg_color, foreground=accent_color, 
                       font=('Arial', 12))
        style.configure('Info.TLabel', background=secondary_bg, foreground=fg_color, 
                       font=('Arial', 10))
        style.configure('Custom.TButton', background=accent_color, foreground='#000000', 
                       font=('Arial', 11, 'bold'), borderwidth=0)
        style.map('Custom.TButton', background=[('active', '#ffd700')])
        
        # Header
        header_frame = tk.Frame(self.root, bg=bg_color, pady=20)
        header_frame.pack(fill='x')
        
        title_label = ttk.Label(header_frame, text="🗺️ GIẢI BÀI TOÁN NGƯỜI DU LỊCH (TSP)", 
                               style='Title.TLabel')
        title_label.pack()
        
        subtitle_label = ttk.Label(header_frame, 
                                   text="So sánh thuật toán Backtracking (simpleAI) và ACO (Ant Colony Optimization)",
                                   style='Subtitle.TLabel')
        subtitle_label.pack(pady=5)
        
        # Main container
        main_container = tk.Frame(self.root, bg=bg_color)
        main_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left panel - Controls
        left_panel = tk.Frame(main_container, bg=secondary_bg, width=350)
        left_panel.pack(side='left', fill='y', padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Cities info
        cities_frame = tk.LabelFrame(left_panel, text="Danh sách thành phố", 
                                     bg=secondary_bg, fg=fg_color, font=('Arial', 11, 'bold'),
                                     padx=10, pady=10)
        cities_frame.pack(fill='x', padx=10, pady=10)
        
        cities_text = scrolledtext.ScrolledText(cities_frame, height=8, width=35, 
                                               bg='#2a2a2a', fg=fg_color, 
                                               font=('Courier', 9))
        cities_text.pack()
        cities_text.insert('1.0', '\n'.join([f"{i+1}. {city}" for i, city in enumerate(self.cities)]))
        cities_text.config(state='disabled')
        
        # Algorithm parameters
        params_frame = tk.LabelFrame(left_panel, text="Tham số thuật toán ACO", 
                                     bg=secondary_bg, fg=fg_color, font=('Arial', 11, 'bold'),
                                     padx=10, pady=10)
        params_frame.pack(fill='x', padx=10, pady=10)
        
        # ACO parameters
        tk.Label(params_frame, text="Số lượng kiến:", bg=secondary_bg, fg=fg_color).grid(row=0, column=0, sticky='w', pady=5)
        self.ants_var = tk.StringVar(value="30")
        tk.Entry(params_frame, textvariable=self.ants_var, width=10, bg='#2a2a2a', fg=fg_color).grid(row=0, column=1, pady=5)
        
        tk.Label(params_frame, text="Số iterations:", bg=secondary_bg, fg=fg_color).grid(row=1, column=0, sticky='w', pady=5)
        self.iterations_var = tk.StringVar(value="100")
        tk.Entry(params_frame, textvariable=self.iterations_var, width=10, bg='#2a2a2a', fg=fg_color).grid(row=1, column=1, pady=5)
        
        tk.Label(params_frame, text="Alpha (α):", bg=secondary_bg, fg=fg_color).grid(row=2, column=0, sticky='w', pady=5)
        self.alpha_var = tk.StringVar(value="1.0")
        tk.Entry(params_frame, textvariable=self.alpha_var, width=10, bg='#2a2a2a', fg=fg_color).grid(row=2, column=1, pady=5)
        
        tk.Label(params_frame, text="Beta (β):", bg=secondary_bg, fg=fg_color).grid(row=3, column=0, sticky='w', pady=5)
        self.beta_var = tk.StringVar(value="2.0")
        tk.Entry(params_frame, textvariable=self.beta_var, width=10, bg='#2a2a2a', fg=fg_color).grid(row=3, column=1, pady=5)
        
        # Buttons
        button_frame = tk.Frame(left_panel, bg=secondary_bg)
        button_frame.pack(fill='x', padx=10, pady=20)
        
        solve_btn = tk.Button(button_frame, text="🚀 Giải bài toán", 
                             command=self.solve_tsp,
                             bg=accent_color, fg='#000000', 
                             font=('Arial', 12, 'bold'),
                             relief='flat', cursor='hand2', pady=10)
        solve_btn.pack(fill='x', pady=5)
        
        compare_btn = tk.Button(button_frame, text="📊 So sánh kết quả", 
                               command=self.compare_results,
                               bg='#4a4a4a', fg=fg_color, 
                               font=('Arial', 11, 'bold'),
                               relief='flat', cursor='hand2', pady=8)
        compare_btn.pack(fill='x', pady=5)
        
        # Results display
        results_frame = tk.LabelFrame(left_panel, text="Kết quả", 
                                     bg=secondary_bg, fg=fg_color, font=('Arial', 11, 'bold'),
                                     padx=10, pady=10)
        results_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.results_text = scrolledtext.ScrolledText(results_frame, height=15, 
                                                     bg='#2a2a2a', fg=fg_color, 
                                                     font=('Courier', 9), wrap='word')
        self.results_text.pack(fill='both', expand=True)
        
        # Right panel - Visualization
        right_panel = tk.Frame(main_container, bg=secondary_bg)
        right_panel.pack(side='right', fill='both', expand=True)
        
        # Create matplotlib figure
        self.fig, self.axes = plt.subplots(2, 2, figsize=(12, 10))
        self.fig.patch.set_facecolor('#1a1a1a')
        
        for ax in self.axes.flat:
            ax.set_facecolor('#2a2a2a')
            ax.tick_params(colors='white')
            ax.spines['bottom'].set_color('white')
            ax.spines['top'].set_color('white')
            ax.spines['left'].set_color('white')
            ax.spines['right'].set_color('white')
            ax.xaxis.label.set_color('white')
            ax.yaxis.label.set_color('white')
            ax.title.set_color('white')
        
        self.canvas = FigureCanvasTkAgg(self.fig, right_panel)
        self.canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)
        
        # Initial plot
        self.plot_initial_cities()
        
    def plot_initial_cities(self):
        """Vẽ vị trí ban đầu của các thành phố"""
        ax = self.axes[0, 0]
        ax.clear()
        ax.set_facecolor('#2a2a2a')
        
        # Plot cities
        x_coords = [self.city_coords[city][0] for city in self.cities]
        y_coords = [self.city_coords[city][1] for city in self.cities]
        
        ax.scatter(x_coords, y_coords, c='#f7d046', s=200, zorder=3, edgecolors='white', linewidth=2)
        
        # Add city labels
        for city in self.cities:
            x, y = self.city_coords[city]
            ax.annotate(city, (x, y), xytext=(5, 5), textcoords='offset points',
                       fontsize=9, color='white', weight='bold')
        
        ax.set_xlabel('Kinh độ', fontsize=10, color='white')
        ax.set_ylabel('Vĩ độ', fontsize=10, color='white')
        ax.set_title('Vị trí các thành phố', fontsize=12, color='white', weight='bold')
        ax.grid(True, alpha=0.3, color='gray')
        
        # Clear other subplots
        for i in range(1, 4):
            ax = self.axes.flat[i]
            ax.clear()
            ax.set_facecolor('#2a2a2a')
            ax.text(0.5, 0.5, 'Chờ kết quả...', ha='center', va='center',
                   fontsize=14, color='gray', transform=ax.transAxes)
            ax.set_xticks([])
            ax.set_yticks([])
        
        self.canvas.draw()
        
    def plot_route(self, ax, route, title, color='#f7d046'):
        """Vẽ tuyến đường"""
        ax.clear()
        ax.set_facecolor('#2a2a2a')
        
        # Get coordinates
        x_coords = [self.city_coords[city][0] for city in route]
        y_coords = [self.city_coords[city][1] for city in route]
        
        # Add starting point at the end to complete the cycle
        x_coords.append(x_coords[0])
        y_coords.append(y_coords[0])
        
        # Plot route
        ax.plot(x_coords, y_coords, 'o-', color=color, linewidth=2, 
               markersize=10, markerfacecolor=color, markeredgecolor='white', 
               markeredgewidth=2, zorder=2)
        
        # Add city labels
        for i, city in enumerate(route):
            x, y = self.city_coords[city]
            ax.annotate(f"{i+1}. {city}", (x, y), xytext=(5, 5), 
                       textcoords='offset points', fontsize=8, color='white', weight='bold')
        
        ax.set_xlabel('Kinh độ', fontsize=10, color='white')
        ax.set_ylabel('Vĩ độ', fontsize=10, color='white')
        ax.set_title(title, fontsize=11, color='white', weight='bold')
        ax.grid(True, alpha=0.3, color='gray')
        
    def solve_tsp(self):
        """Giải bài toán TSP bằng cả hai thuật toán"""
        self.results_text.delete('1.0', tk.END)
        self.results_text.insert('1.0', "Đang giải bài toán...\n\n")
        self.root.update()
        
        try:
            # Get ACO parameters
            n_ants = int(self.ants_var.get())
            n_iterations = int(self.iterations_var.get())
            alpha = float(self.alpha_var.get())
            beta = float(self.beta_var.get())
            
            # Solve with Backtracking
            self.results_text.insert(tk.END, "=" * 50 + "\n")
            self.results_text.insert(tk.END, "THUẬT TOÁN BACKTRACKING (simpleAI)\n")
            self.results_text.insert(tk.END, "=" * 50 + "\n\n")
            self.root.update()
            
            bt_solver = TSPBacktracking(self.cities, self.distance_matrix)
            bt_result = bt_solver.solve()
            self.results['backtracking'] = bt_result
            
            self.results_text.insert(tk.END, f"Tuyến đường: {' → '.join(bt_result['route'])} → {bt_result['route'][0]}\n")
            self.results_text.insert(tk.END, f"Tổng khoảng cách: {bt_result['distance']:.2f} km\n")
            self.results_text.insert(tk.END, f"Thời gian: {bt_result['time']:.4f} giây\n\n")
            
            # Solve with ACO
            self.results_text.insert(tk.END, "=" * 50 + "\n")
            self.results_text.insert(tk.END, "THUẬT TOÁN ACO (Ant Colony Optimization)\n")
            self.results_text.insert(tk.END, "=" * 50 + "\n\n")
            self.root.update()
            
            # Redirect stdout to capture ACO progress
            old_stdout = sys.stdout
            sys.stdout = io.StringIO()
            
            aco_solver = TSP_ACO(self.cities, self.distance_matrix, 
                                n_ants=n_ants, n_iterations=n_iterations,
                                alpha=alpha, beta=beta)
            aco_result = aco_solver.solve()
            
            # Get captured output
            aco_output = sys.stdout.getvalue()
            sys.stdout = old_stdout
            
            self.results['aco'] = aco_result
            
            self.results_text.insert(tk.END, aco_output + "\n")
            self.results_text.insert(tk.END, f"Tuyến đường: {' → '.join(aco_result['route'])} → {aco_result['route'][0]}\n")
            self.results_text.insert(tk.END, f"Tổng khoảng cách: {aco_result['distance']:.2f} km\n")
            self.results_text.insert(tk.END, f"Thời gian: {aco_result['time']:.4f} giây\n\n")
            
            # Plot results
            self.plot_route(self.axes[0, 1], bt_result['route'], 
                          f"Backtracking\nKhoảng cách: {bt_result['distance']:.2f} km", 
                          color='#4a9eff')
            
            self.plot_route(self.axes[1, 0], aco_result['route'], 
                          f"ACO\nKhoảng cách: {aco_result['distance']:.2f} km", 
                          color='#ff6b6b')
            
            # Plot convergence for ACO
            ax = self.axes[1, 1]
            ax.clear()
            ax.set_facecolor('#2a2a2a')
            ax.plot(aco_result['convergence'], color='#f7d046', linewidth=2)
            ax.set_xlabel('Iteration', fontsize=10, color='white')
            ax.set_ylabel('Khoảng cách tốt nhất (km)', fontsize=10, color='white')
            ax.set_title('Quá trình hội tụ của ACO', fontsize=11, color='white', weight='bold')
            ax.grid(True, alpha=0.3, color='gray')
            
            self.canvas.draw()
            
            self.results_text.insert(tk.END, "=" * 50 + "\n")
            self.results_text.insert(tk.END, "✅ Hoàn thành! Nhấn 'So sánh kết quả' để xem chi tiết.\n")
            self.results_text.insert(tk.END, "=" * 50 + "\n")
            
        except Exception as e:
            messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")
            
    def compare_results(self):
        """So sánh kết quả của hai thuật toán"""
        if not self.results:
            messagebox.showwarning("Cảnh báo", "Vui lòng giải bài toán trước!")
            return
        
        comparison_window = tk.Toplevel(self.root)
        comparison_window.title("So sánh kết quả")
        comparison_window.geometry("800x600")
        comparison_window.configure(bg='#0a0a0a')
        
        # Title
        title = tk.Label(comparison_window, text="📊 SO SÁNH KẾT QUẢ", 
                        bg='#0a0a0a', fg='#f7d046', font=('Arial', 18, 'bold'))
        title.pack(pady=20)
        
        # Comparison table
        table_frame = tk.Frame(comparison_window, bg='#1a1a1a')
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Headers
        headers = ['Tiêu chí', 'Backtracking', 'ACO', 'Tốt hơn']
        for i, header in enumerate(headers):
            label = tk.Label(table_frame, text=header, bg='#2a2a2a', fg='#f7d046',
                           font=('Arial', 12, 'bold'), relief='solid', borderwidth=1)
            label.grid(row=0, column=i, sticky='nsew', padx=1, pady=1, ipady=10)
        
        bt = self.results.get('backtracking', {})
        aco = self.results.get('aco', {})
        
        # Data rows
        comparisons = [
            ('Khoảng cách (km)', f"{bt.get('distance', 0):.2f}", f"{aco.get('distance', 0):.2f}",
             'Backtracking' if bt.get('distance', float('inf')) < aco.get('distance', float('inf')) else 'ACO'),
            ('Thời gian (giây)', f"{bt.get('time', 0):.4f}", f"{aco.get('time', 0):.4f}",
             'Backtracking' if bt.get('time', float('inf')) < aco.get('time', float('inf')) else 'ACO'),
            ('Số thành phố', str(len(self.cities)), str(len(self.cities)), 'Bằng nhau'),
        ]
        
        for i, (criterion, bt_val, aco_val, winner) in enumerate(comparisons, start=1):
            # Criterion
            label = tk.Label(table_frame, text=criterion, bg='#1a1a1a', fg='white',
                           font=('Arial', 11), relief='solid', borderwidth=1, anchor='w', padx=10)
            label.grid(row=i, column=0, sticky='nsew', padx=1, pady=1, ipady=8)
            
            # Backtracking value
            bg_color = '#2d5016' if winner == 'Backtracking' else '#1a1a1a'
            label = tk.Label(table_frame, text=bt_val, bg=bg_color, fg='white',
                           font=('Arial', 11), relief='solid', borderwidth=1)
            label.grid(row=i, column=1, sticky='nsew', padx=1, pady=1, ipady=8)
            
            # ACO value
            bg_color = '#2d5016' if winner == 'ACO' else '#1a1a1a'
            label = tk.Label(table_frame, text=aco_val, bg=bg_color, fg='white',
                           font=('Arial', 11), relief='solid', borderwidth=1)
            label.grid(row=i, column=2, sticky='nsew', padx=1, pady=1, ipady=8)
            
            # Winner
            label = tk.Label(table_frame, text=winner, bg='#1a1a1a', fg='#f7d046',
                           font=('Arial', 11, 'bold'), relief='solid', borderwidth=1)
            label.grid(row=i, column=3, sticky='nsew', padx=1, pady=1, ipady=8)
        
        # Configure grid weights
        for i in range(4):
            table_frame.columnconfigure(i, weight=1)
        
        # Summary
        summary_frame = tk.Frame(comparison_window, bg='#1a1a1a', relief='solid', borderwidth=2)
        summary_frame.pack(fill='x', padx=20, pady=20)
        
        summary_title = tk.Label(summary_frame, text="📝 KẾT LUẬN", 
                                bg='#1a1a1a', fg='#f7d046', font=('Arial', 14, 'bold'))
        summary_title.pack(pady=10)
        
        # Determine overall winner
        bt_distance = bt.get('distance', float('inf'))
        aco_distance = aco.get('distance', float('inf'))
        
        if bt_distance < aco_distance:
            conclusion = (f"✅ Backtracking tìm được tuyến đường ngắn hơn ({bt_distance:.2f} km so với {aco_distance:.2f} km)\n"
                         f"⏱️ Tuy nhiên, ACO có thể nhanh hơn với bài toán lớn và cho kết quả gần tối ưu")
        elif aco_distance < bt_distance:
            conclusion = (f"✅ ACO tìm được tuyến đường ngắn hơn ({aco_distance:.2f} km so với {bt_distance:.2f} km)\n"
                         f"⚡ ACO phù hợp hơn cho bài toán TSP với nhiều thành phố")
        else:
            conclusion = "🤝 Cả hai thuật toán đều tìm được tuyến đường có độ dài bằng nhau"
        
        summary_text = tk.Label(summary_frame, text=conclusion, 
                               bg='#1a1a1a', fg='white', font=('Arial', 11),
                               justify='left', wraplength=700)
        summary_text.pack(pady=10, padx=20)
        
        # Close button
        close_btn = tk.Button(comparison_window, text="Đóng", command=comparison_window.destroy,
                             bg='#f7d046', fg='#000000', font=('Arial', 11, 'bold'),
                             relief='flat', cursor='hand2', pady=8, padx=30)
        close_btn.pack(pady=10)


def main():
    """Hàm chính để chạy ứng dụng"""
    root = tk.Tk()
    app = TSPApplication(root)
    root.mainloop()


if __name__ == "__main__":
    main()
