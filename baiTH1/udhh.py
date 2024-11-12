import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Cửa sổ chính
class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Chọn Hình 2D hoặc 3D")
        self.geometry("400x200")

        label = tk.Label(self, text="Chọn loại hình:", font=("Arial", 12))
        label.pack(pady=10)

        self.mode_var = tk.StringVar()
        self.mode_combobox = ttk.Combobox(self, textvariable=self.mode_var, values=["Hình 2D", "Hình 3D"])
        self.mode_combobox.pack(pady=5)
        self.mode_combobox.bind("<<ComboboxSelected>>", self.on_mode_selected)

    def on_mode_selected(self, event):
        if self.mode_var.get() == "Hình 2D":
            Shape2DWindow(self)
        elif self.mode_var.get() == "Hình 3D":
            Shape3DWindow(self)

class Shape2DWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Chọn Hình 2D")
        self.geometry("400x400")

        label = tk.Label(self, text="Chọn hình 2D:", font=("Arial", 12))
        label.pack(pady=10)

        shapes = ["Hình Vuông", "Hình Chữ Nhật", "Hình Tam Giác", "Hình Thang", "Hình Bình Hành", "Hình Tròn"]
        self.shape_var = tk.StringVar()
        self.shape_combobox = ttk.Combobox(self, textvariable=self.shape_var, values=shapes)
        self.shape_combobox.pack(pady=5)
        self.shape_combobox.bind("<<ComboboxSelected>>", self.on_shape_selected)

        self.input_frame = tk.Frame(self)
        self.input_frame.pack(pady=10)

        self.result_label = tk.Label(self, text="", font=("Arial", 10))
        self.result_label.pack(pady=5)

        # Tạo nút tính toán và vẽ hình riêng biệt
        self.calculate_button = tk.Button(self, text="Tính Toán", command=self.calculate_area_and_perimeter)
        self.calculate_button.pack(pady=5)

        self.draw_button = tk.Button(self, text="Vẽ Hình 2D", command=self.draw_2d_shape)
        self.draw_button.pack(pady=5)

        # Nút xóa dữ liệu
        self.clear_button = tk.Button(self, text="Xóa Dữ Liệu", command=self.clear_data)
        self.clear_button.pack(pady=5)

    def on_shape_selected(self, event):
        for widget in self.input_frame.winfo_children():
            widget.destroy()

        shape = self.shape_var.get()
        if shape == "Hình Vuông":
            self.create_square_inputs()
        elif shape == "Hình Chữ Nhật":
            self.create_rectangle_inputs()
        elif shape == "Hình Tam Giác":
            self.create_triangle_inputs()
        elif shape == "Hình Thang":
            self.create_trapezoid_inputs()
        elif shape == "Hình Bình Hành":
            self.create_parallelogram_inputs()
        elif shape == "Hình Tròn":
            self.create_circle_inputs()

    def create_square_inputs(self):
        tk.Label(self.input_frame, text="Cạnh:").pack()
        self.side_entry = tk.Entry(self.input_frame)
        self.side_entry.pack()
        self.unit_combobox()

    def create_rectangle_inputs(self):
        tk.Label(self.input_frame, text="Chiều Dài:").pack()
        self.length_entry = tk.Entry(self.input_frame)
        self.length_entry.pack()
        tk.Label(self.input_frame, text="Chiều Rộng:").pack()
        self.width_entry = tk.Entry(self.input_frame)
        self.width_entry.pack()
        self.unit_combobox()

    def create_triangle_inputs(self):
        tk.Label(self.input_frame, text="Cạnh 1:").pack()
        self.side1_entry = tk.Entry(self.input_frame)
        self.side1_entry.pack()
        tk.Label(self.input_frame, text="Cạnh 2:").pack()
        self.side2_entry = tk.Entry(self.input_frame)
        self.side2_entry.pack()
        tk.Label(self.input_frame, text="Cạnh 3:").pack()
        self.side3_entry = tk.Entry(self.input_frame)
        self.side3_entry.pack()
        self.unit_combobox()

    def create_trapezoid_inputs(self):
        tk.Label(self.input_frame, text="Đáy Lớn:").pack()
        self.base1_entry = tk.Entry(self.input_frame)
        self.base1_entry.pack()
        tk.Label(self.input_frame, text="Đáy Nhỏ:").pack()
        self.base2_entry = tk.Entry(self.input_frame)
        self.base2_entry.pack()
        tk.Label(self.input_frame, text="Chiều Cao:").pack()
        self.height_entry = tk.Entry(self.input_frame)
        self.height_entry.pack()
        self.unit_combobox()

    def create_parallelogram_inputs(self):
        tk.Label(self.input_frame, text="Cạnh Đáy:").pack()
        self.base_entry = tk.Entry(self.input_frame)
        self.base_entry.pack()
        tk.Label(self.input_frame, text="Cạnh Bên:").pack()
        self.side_entry = tk.Entry(self.input_frame)
        self.side_entry.pack()
        tk.Label(self.input_frame, text="Chiều Cao:").pack()
        self.height_entry = tk.Entry(self.input_frame)
        self.height_entry.pack()
        self.unit_combobox()

    def create_circle_inputs(self):
        tk.Label(self.input_frame, text="Bán Kính:").pack()
        self.radius_entry = tk.Entry(self.input_frame)
        self.radius_entry.pack()
        self.unit_combobox()

    def unit_combobox(self):
        tk.Label(self.input_frame, text="Chọn đơn vị:").pack()
        self.units = ["cm", "m", "in"]
        self.unit_var = tk.StringVar()
        unit_combobox = ttk.Combobox(self.input_frame, textvariable=self.unit_var, values=self.units)
        unit_combobox.pack()

    def calculate_area_and_perimeter(self):
        shape = self.shape_var.get()
        unit = self.unit_var.get()

        if shape == "Hình Vuông":
            side = float(self.side_entry.get())
            area = side ** 2
            perimeter = 4 * side
            self.result_label.config(text=f"Diện Tích: {area} {unit}², Chu Vi: {perimeter} {unit}")
        elif shape == "Hình Chữ Nhật":
            length = float(self.length_entry.get())
            width = float(self.width_entry.get())
            area = length * width
            perimeter = 2 * (length + width)
            self.result_label.config(text=f"Diện Tích: {area} {unit}², Chu Vi: {perimeter} {unit}")
        elif shape == "Hình Tam Giác":
            side1 = float(self.side1_entry.get())
            side2 = float(self.side2_entry.get())
            side3 = float(self.side3_entry.get())
            s = (side1 + side2 + side3) / 2
            area = (s * (s - side1) * (s - side2) * (s - side3)) ** 0.5
            perimeter = side1 + side2 + side3
            self.result_label.config(text=f"Diện Tích: {area:.2f} {unit}², Chu Vi: {perimeter} {unit}")
        elif shape == "Hình Thang":
            base1 = float(self.base1_entry.get())
            base2 = float(self.base2_entry.get())
            height = float(self.height_entry.get())
            area = ((base1 + base2) / 2) * height
            perimeter = base1 + base2 + 2 * height
            self.result_label.config(text=f"Diện Tích: {area} {unit}², Chu Vi: {perimeter} {unit}")
        elif shape == "Hình Bình Hành":
            base = float(self.base_entry.get())
            side = float(self.side_entry.get())
            height = float(self.height_entry.get())
            area = base * height
            perimeter = 2 * (base + side)
            self.result_label.config(text=f"Diện Tích: {area} {unit}², Chu Vi: {perimeter} {unit}")
        elif shape == "Hình Tròn":
            radius = float(self.radius_entry.get())
            area = np.pi * radius ** 2
            perimeter = 2 * np.pi * radius
            self.result_label.config(text=f"Diện Tích: {area:.2f} {unit}², Chu Vi: {perimeter:.2f} {unit}")

    def draw_2d_shape(self):
        shape = self.shape_var.get()

        if shape == "Hình Vuông":
            side = float(self.side_entry.get())
            self.plot_square(side)
        elif shape == "Hình Chữ Nhật":
            length = float(self.length_entry.get())
            width = float(self.width_entry.get())
            self.plot_rectangle(length, width)
        elif shape == "Hình Tam Giác":
            side1 = float(self.side1_entry.get())
            side2 = float(self.side2_entry.get())
            side3 = float(self.side3_entry.get())
            self.plot_triangle(side1, side2, side3)
        elif shape == "Hình Thang":
            base1 = float(self.base1_entry.get())
            base2 = float(self.base2_entry.get())
            height = float(self.height_entry.get())
            self.plot_trapezoid(base1, base2, height)
        elif shape == "Hình Bình Hành":
            base = float(self.base_entry.get())
            side = float(self.side_entry.get())
            height = float(self.height_entry.get())
            self.plot_parallelogram(base, side, height)
        elif shape == "Hình Tròn":
            radius = float(self.radius_entry.get())
            self.plot_circle(radius)

    def clear_data(self):
        # Xóa tất cả các trường nhập liệu và kết quả
        for widget in self.input_frame.winfo_children():
            widget.destroy()
        self.result_label.config(text="")
        self.shape_var.set('')
        self.unit_var.set('')

    # Các hàm vẽ hình
    def plot_square(self, side):
        fig, ax = plt.subplots()
        square = plt.Rectangle((0, 0), side, side, fill=None, edgecolor='r')
        ax.add_patch(square)
        ax.set_xlim(-1, side + 1)
        ax.set_ylim(-1, side + 1)
        ax.set_aspect('equal', 'box')
        plt.title("Hình Vuông")
        plt.show()

    def plot_rectangle(self, length, width):
        fig, ax = plt.subplots()
        rectangle = plt.Rectangle((0, 0), length, width, fill=None, edgecolor='b')
        ax.add_patch(rectangle)
        ax.set_xlim(-1, length + 1)
        ax.set_ylim(-1, width + 1)
        ax.set_aspect('equal', 'box')
        plt.title("Hình Chữ Nhật")
        plt.show()

    def plot_triangle(self, side1, side2, side3):
        fig, ax = plt.subplots()
        p = (side1 + side2 + side3) / 2
        h = (2 / side1) * np.sqrt(p * (p - side1) * (p - side2) * (p - side3))
        ax.plot([0, side1, side2 * np.cos(np.arccos((side1**2 + side2**2 - side3**2) / (2 * side1 * side2)))], 
                [0, 0, h], 'r-')
        ax.fill([0, side1, side2 * np.cos(np.arccos((side1**2 + side2**2 - side3**2) / (2 * side1 * side2)))], 
                [0, 0, h], 'b', alpha=0.3)
        ax.set_xlim(-1, max(side1, side2) + 1)
        ax.set_ylim(-1, h + 1)
        ax.set_aspect('equal', 'box')
        plt.title("Hình Tam Giác")
        plt.show()

    def plot_trapezoid(self, base1, base2, height):
        fig, ax = plt.subplots()
        ax.plot([0, base1, base2, 0], [0, 0, height, height], 'r-')
        ax.fill([0, base1, base2, 0], [0, 0, height, height], 'b', alpha=0.3)
        ax.set_xlim(-1, max(base1, base2) + 1)
        ax.set_ylim(-1, height + 1)
        ax.set_aspect('equal', 'box')
        plt.title("Hình Thang")
        plt.show()

    def plot_parallelogram(self, base, side, height):
        fig, ax = plt.subplots()
        ax.plot([0, base, base + side, side], [0, 0, height, height], 'r-')
        ax.fill([0, base, base + side, side], [0, 0, height, height], 'b', alpha=0.3)
        ax.set_xlim(-1, base + side + 1)
        ax.set_ylim(-1, height + 1)
        ax.set_aspect('equal', 'box')
        plt.title("Hình Bình Hành")
        plt.show()

    def plot_circle(self, radius):
        fig, ax = plt.subplots()
        circle = plt.Circle((radius, radius), radius, fill=False, edgecolor='g')
        ax.add_patch(circle)
        ax.set_xlim(-1, radius * 2 + 1)
        ax.set_ylim(-1, radius * 2 + 1)
        ax.set_aspect('equal', 'box')
        plt.title("Hình Tròn")
        plt.show()

# Cửa sổ cho hình 3D
class Shape3DWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Chọn Hình 3D")
        self.geometry("400x500")

        label = tk.Label(self, text="Chọn hình 3D:", font=("Arial", 12))
        label.pack(pady=10)

        shapes = ["Hình Hộp Chữ Nhật", "Hình Cầu", "Hình Chóp", "Hình Lập Phương", "Hình Trụ"]
        self.shape_var = tk.StringVar()
        self.shape_combobox = ttk.Combobox(self, textvariable=self.shape_var, values=shapes)
        self.shape_combobox.pack(pady=5)
        self.shape_combobox.bind("<<ComboboxSelected>>", self.on_shape_selected)

        self.input_frame = tk.Frame(self)
        self.input_frame.pack(pady=10)

        self.result_label = tk.Label(self, text="", font=("Arial", 10))
        self.result_label.pack(pady=5)

        # Sử dụng Combobox cho đơn vị
        self.unit_label = tk.Label(self, text="Đơn vị:", font=("Arial", 10))
        self.unit_label.pack(pady=5)

        # Combobox cho đơn vị
        self.unit_options = ["cm", "m", "inch", "ft"]
        self.unit_combobox = ttk.Combobox(self, values=self.unit_options)
        self.unit_combobox.set(self.unit_options[0])  # Mặc định là cm
        self.unit_combobox.pack(pady=5)

        self.calculate_button = tk.Button(self, text="Tính Toán", command=self.calculate_values)
        self.calculate_button.pack(pady=5)

        self.draw_button = tk.Button(self, text="Vẽ Hình 3D", command=self.draw_3d_shape)
        self.draw_button.pack(pady=5)

        self.clear_button = tk.Button(self, text="Xóa Dữ Liệu", command=self.clear_inputs)
        self.clear_button.pack(pady=5)

    def on_shape_selected(self, event):
        for widget in self.input_frame.winfo_children():
            widget.destroy()

        shape = self.shape_var.get()
        if shape == "Hình Hộp Chữ Nhật":
            self.create_box_inputs()
        elif shape == "Hình Cầu":
            self.create_sphere_inputs()
        elif shape == "Hình Chóp":
            self.create_cone_inputs()
        elif shape == "Hình Lập Phương":
            self.create_cube_inputs()
        elif shape == "Hình Trụ":
            self.create_cylinder_inputs()

    def create_box_inputs(self):
        tk.Label(self.input_frame, text="Chiều Dài:").pack()
        self.length_entry = tk.Entry(self.input_frame)
        self.length_entry.pack()
        tk.Label(self.input_frame, text="Chiều Rộng:").pack()
        self.width_entry = tk.Entry(self.input_frame)
        self.width_entry.pack()
        tk.Label(self.input_frame, text="Chiều Cao:").pack()
        self.height_entry = tk.Entry(self.input_frame)
        self.height_entry.pack()

    def create_sphere_inputs(self):
        tk.Label(self.input_frame, text="Bán Kính:").pack()
        self.radius_entry = tk.Entry(self.input_frame)
        self.radius_entry.pack()

    def create_cone_inputs(self):
        tk.Label(self.input_frame, text="Bán Kính:").pack()
        self.radius_entry = tk.Entry(self.input_frame)
        self.radius_entry.pack()
        tk.Label(self.input_frame, text="Chiều Cao:").pack()
        self.height_entry = tk.Entry(self.input_frame)
        self.height_entry.pack()

    def create_cube_inputs(self):
        tk.Label(self.input_frame, text="Chiều Dài Cạnh:").pack()
        self.side_entry = tk.Entry(self.input_frame)
        self.side_entry.pack()

    def create_cylinder_inputs(self):
        tk.Label(self.input_frame, text="Bán Kính:").pack()
        self.radius_entry = tk.Entry(self.input_frame)
        self.radius_entry.pack()
        tk.Label(self.input_frame, text="Chiều Cao:").pack()
        self.height_entry = tk.Entry(self.input_frame)
        self.height_entry.pack()

    def calculate_values(self):
        shape = self.shape_var.get()
        unit = self.unit_combobox.get()  # Lấy đơn vị từ Combobox

        if shape == "Hình Hộp Chữ Nhật":
            length = float(self.length_entry.get())
            width = float(self.width_entry.get())
            height = float(self.height_entry.get())
            surface_area, lateral_area, volume = self.calculate_box(length, width, height)
            result_text = f"Diện Tích Toàn Phần: {surface_area} {unit}^2\n"
            result_text += f"Diện Tích Xung Quanh: {lateral_area} {unit}^2\n"
            result_text += f"Thể Tích: {volume} {unit}^3\n"

        elif shape == "Hình Cầu":
            radius = float(self.radius_entry.get())
            surface_area, volume = self.calculate_sphere(radius)
            result_text = f"Diện Tích Toàn Phần: {surface_area} {unit}^2\n"
            result_text += f"Thể Tích: {volume} {unit}^3\n"

        elif shape == "Hình Chóp":
            radius = float(self.radius_entry.get())
            height = float(self.height_entry.get())
            lateral_area, surface_area, volume = self.calculate_cone(radius, height)
            result_text = f"Diện Tích Xung Quanh: {lateral_area} {unit}^2\n"
            result_text += f"Diện Tích Toàn Phần: {surface_area} {unit}^2\n"
            result_text += f"Thể Tích: {volume} {unit}^3\n"

        elif shape == "Hình Lập Phương":
            side = float(self.side_entry.get())
            surface_area, volume = self.calculate_cube(side)
            result_text = f"Diện Tích Toàn Phần: {surface_area} {unit}^2\n"
            result_text += f"Thể Tích: {volume} {unit}^3\n"

        elif shape == "Hình Trụ":
            radius = float(self.radius_entry.get())
            height = float(self.height_entry.get())
            lateral_area, surface_area, volume = self.calculate_cylinder(radius, height)
            result_text = f"Diện Tích Xung Quanh: {lateral_area} {unit}^2\n"
            result_text += f"Diện Tích Toàn Phần: {surface_area} {unit}^2\n"
            result_text += f"Thể Tích: {volume} {unit}^3\n"

        self.result_label.config(text=result_text)

    def draw_3d_shape(self):
        shape = self.shape_var.get()

        if shape == "Hình Hộp Chữ Nhật":
            length = float(self.length_entry.get())
            width = float(self.width_entry.get())
            height = float(self.height_entry.get())
            self.plot_box(length, width, height)

        elif shape == "Hình Cầu":
            radius = float(self.radius_entry.get())
            self.plot_sphere(radius)

        elif shape == "Hình Chóp":
            radius = float(self.radius_entry.get())
            height = float(self.height_entry.get())
            self.plot_cone(radius, height)

        elif shape == "Hình Lập Phương":
            side = float(self.side_entry.get())
            self.plot_cube(side)

        elif shape == "Hình Trụ":
            radius = float(self.radius_entry.get())
            height = float(self.height_entry.get())
            self.plot_cylinder(radius, height)

    def clear_inputs(self):
        for widget in self.input_frame.winfo_children():
            widget.destroy()
        self.result_label.config(text="")
        self.unit_combobox.set(self.unit_options[0])  # Đặt lại giá trị mặc định của Combobox
        self.shape_var.set("")


    # Tính toán các diện tích và thể tích
    def calculate_box(self, length, width, height):
        surface_area = 2 * (length * width + length * height + width * height)
        lateral_area = 2 * (length + width) * height
        volume = length * width * height
        return surface_area, lateral_area, volume

    def calculate_sphere(self, radius):
        surface_area = 4 * np.pi * radius**2
        volume = (4 / 3) * np.pi * radius**3
        return surface_area, volume

    def calculate_cone(self, radius, height):
        slant_height = np.sqrt(radius**2 + height**2)
        lateral_area = np.pi * radius * slant_height
        surface_area = lateral_area + np.pi * radius**2
        volume = (1 / 3) * np.pi * radius**2 * height
        return lateral_area, surface_area, volume

    def calculate_cube(self, side):
        surface_area = 6 * side**2
        volume = side**3
        return surface_area, volume

    def calculate_cylinder(self, radius, height):
        lateral_area = 2 * np.pi * radius * height
        surface_area = lateral_area + 2 * np.pi * radius**2
        volume = np.pi * radius**2 * height
        return lateral_area, surface_area, volume

    # Vẽ các hình 3D
    def plot_box(self,length, width, height):
        # Tạo tọa độ các đỉnh của hình hộp
        x = [0, length, length, 0, 0, length, length, 0]
        y = [0, 0, width, width, 0, 0, width, width]
        z = [0, 0, 0, 0, height, height, height, height]

        # Tạo các mặt của hình hộp bằng cách lấy chỉ số của các đỉnh
        verts = [
            [ [x[0], y[0], z[0]], [x[1], y[1], z[1]], [x[5], y[5], z[5]], [x[4], y[4], z[4]] ],
            [ [x[7], y[7], z[7]], [x[6], y[6], z[6]], [x[2], y[2], z[2]], [x[3], y[3], z[3]] ],
            [ [x[0], y[0], z[0]], [x[3], y[3], z[3]], [x[7], y[7], z[7]], [x[4], y[4], z[4]] ],
            [ [x[1], y[1], z[1]], [x[2], y[2], z[2]], [x[6], y[6], z[6]], [x[5], y[5], z[5]] ],
            [ [x[0], y[0], z[0]], [x[1], y[1], z[1]], [x[2], y[2], z[2]], [x[3], y[3], z[3]] ],
            [ [x[4], y[4], z[4]], [x[5], y[5], z[5]], [x[6], y[6], z[6]], [x[7], y[7], z[7]] ]
        ]

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Tạo hình hộp
        ax.add_collection3d(Poly3DCollection(verts, facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25))

        # Thiết lập giới hạn cho trục
        ax.set_xlim([0, max(length, width, height)])
        ax.set_ylim([0, max(length, width, height)])
        ax.set_zlim([0, max(length, width, height)])

        # Hiển thị hình
        plt.show()

    def plot_sphere(self, radius):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        x = radius * np.outer(np.cos(u), np.sin(v))
        y = radius * np.outer(np.sin(u), np.sin(v))
        z = radius * np.outer(np.ones(np.size(u)), np.cos(v))
        ax.plot_surface(x, y, z, color='b')
        plt.title("Hình Cầu")
        plt.show()

    def plot_cone(self, radius, height):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Tạo các giá trị u và z
        u = np.linspace(0, 2 * np.pi, 100)  # Góc quay xung quanh hình trụ
        z = np.linspace(0, height, 100)  # Chiều cao của hình chóp

        # Dùng meshgrid để tạo các ma trận 2D cho x và y
        Z, U = np.meshgrid(z, u)  # U là góc quay, Z là chiều cao
        X = radius * (1 - Z / height) * np.cos(U)  # Tính toán giá trị x
        Y = radius * (1 - Z / height) * np.sin(U)  # Tính toán giá trị y

        # Vẽ hình trụ
        ax.plot_surface(X, Y, Z, color='r')

        plt.title("Hình Chóp")
        plt.show()

    def plot_cube(self, side):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        r = [-side/2, side/2]
        x, y = np.meshgrid(r, r)
        ax.plot_surface(x, y, np.full_like(x, -side/2), color='c')
        ax.plot_surface(x, y, np.full_like(x, side/2), color='y')
        ax.plot_surface(x, np.full_like(x, -side/2), y, color='g')
        ax.plot_surface(x, np.full_like(x, side/2), y, color='b')
        ax.plot_surface(np.full_like(x, -side/2), y, x, color='r')
        ax.plot_surface(np.full_like(x, side/2), y, x, color='m')
        plt.title("Hình Lập Phương")
        plt.show()

    def plot_cylinder(self, radius, height):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Số lượng điểm dùng để vẽ hình trụ
        u = np.linspace(0, 2 * np.pi, 100)  # Góc quay quanh trục Z
        z = np.linspace(0, height, 100)     # Chiều cao của hình trụ
        Z, U = np.meshgrid(z, u)  # Lưới 2D cho z và u (góc)

        # Tọa độ x và y cho các điểm trên bề mặt hình trụ
        X = radius * np.cos(U)
        Y = radius * np.sin(U)

        # Vẽ bề mặt hình trụ
        ax.plot_surface(X, Y, Z, color='g')

        # Vẽ mặt đáy trên (z = height)
        Z_top = height * np.ones_like(U)  # Mặt đáy trên tại z = height
        X_top = radius * np.cos(U)
        Y_top = radius * np.sin(U)
        ax.plot_surface(X_top, Y_top, Z_top, color='b')

        # Vẽ mặt đáy dưới (z = 0)
        Z_bottom = np.zeros_like(U)  # Mặt đáy dưới tại z = 0
        X_bottom = radius * np.cos(U)
        Y_bottom = radius * np.sin(U)
        ax.plot_surface(X_bottom, Y_bottom, Z_bottom, color='b')

        ax.set_title("Hình Trụ")
        plt.show()


# Khởi chạy ứng dụng
if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
