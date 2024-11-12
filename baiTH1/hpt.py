import tkinter as tk
import numpy as np
from tkinter import messagebox

# Hàm kiểm tra chỉ cho phép nhập số (bao gồm cả số âm)
def validate_float_input(P):
    if P == "" or P == "-":  # Cho phép chuỗi trống hoặc dấu trừ
        return True
    try:
        float(P)  # Cố gắng chuyển đổi P sang số thực
        return True
    except ValueError:
        return False

# Hàm tạo các ô nhập hệ số
def create_input_fields():
    global entries, window_matrix, num_vars
    try:
        num_vars = int(entry_num_vars.get())  # Số ẩn
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập số ẩn hợp lệ.")
        return

    # Tạo cửa sổ mới để nhập hệ số và nút giải hệ phương trình
    window_matrix = tk.Toplevel(root)
    window_matrix.title("Nhập Hệ Số Ma Trận")
    window_matrix.configure(bg="#f0f0f0")
    
    entries = []  # Danh sách lưu các ô nhập liệu
    for i in range(num_vars):
        row = []
        for j in range(num_vars + 1):  # +1 cho cột giá trị sau dấu "="
            entry = tk.Entry(window_matrix, width=8, validate="key", validatecommand=(vcmd, "%P"), font=("Arial", 10))
            entry.grid(row=i, column=j, padx=5, pady=5)
            row.append(entry)
        entries.append(row)

    # Nút giải hệ phương trình
    btn_solve = tk.Button(window_matrix, text="Giải hệ phương trình", command=solve_system, font=("Arial", 12), bg="#2196F3", fg="white")
    btn_solve.grid(row=num_vars + 1, column=0, columnspan=num_vars + 1, pady=10)

    # Nút xóa dữ liệu trong cửa sổ nhập hệ số
    btn_clear_matrix = tk.Button(window_matrix, text="Xóa Dữ Liệu", command=clear_matrix_data, font=("Arial", 12), bg="#FF5722", fg="white")
    btn_clear_matrix.grid(row=num_vars + 2, column=0, columnspan=num_vars + 1, pady=10)

# Hàm xóa dữ liệu trong các ô nhập hệ số
def clear_matrix_data():
    for row in entries:
        for entry in row:
            entry.delete(0, tk.END)

# Hàm xóa dữ liệu trong ô nhập số ẩn ở cửa sổ chính
def clear_main_data():
    entry_num_vars.delete(0, tk.END)

# Hàm kiểm tra các ô nhập liệu
def are_entries_filled():
    for row in entries:
        for entry in row:
            if entry.get() == "":
                return False
    return True

# Hàm giải hệ phương trình
def solve_system():
    if not are_entries_filled():  # Kiểm tra các ô nhập
        messagebox.showerror("Lỗi", "Tất cả các ô nhập liệu phải được điền.")
        return

    try:
        # Tạo ma trận hệ số và vector hằng số
        A = []
        B = []
        for i in range(num_vars):
            row = []
            for j in range(num_vars):
                row.append(float(entries[i][j].get()))
            A.append(row)
            B.append(float(entries[i][num_vars].get()))

        A = np.array(A)
        B = np.array(B)

        # Kiểm tra số nghiệm
        rank_A = np.linalg.matrix_rank(A)
        augmented_matrix = np.hstack((A, B.reshape(-1, 1)))
        rank_augmented = np.linalg.matrix_rank(augmented_matrix)

        if rank_A != rank_augmented:
            messagebox.showerror("Kết quả", "Hệ phương trình vô nghiệm.")
        elif rank_A < num_vars:
            messagebox.showinfo("Kết quả", "Hệ phương trình có vô số nghiệm.")
        else:
            X = np.linalg.solve(A, B)
            result = "\nNghiệm của hệ phương trình là:\n" + "\n".join([f"x{i + 1} = {X[i]:.2f}" for i in range(len(X))])
            messagebox.showinfo("Kết quả", result)

    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập số hợp lệ.")
    except np.linalg.LinAlgError:
        messagebox.showerror("Lỗi", "Hệ phương trình không có nghiệm hoặc có vô số nghiệm.")

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Giải Hệ Phương Trình Bằng Ma Trận")
root.configure(bg="#f0f0f0")

# Xác định hàm kiểm tra cho các ô nhập chỉ cho phép số
vcmd = root.register(validate_float_input)

# Nhãn và ô nhập cho số ẩn
label_num_vars = tk.Label(root, text="Số ẩn:", font=("Arial", 12), bg="#f0f0f0")
label_num_vars.grid(row=0, column=0, padx=10, pady=10, sticky="e")
entry_num_vars = tk.Entry(root, validate="key", validatecommand=(vcmd, "%P"), font=("Arial", 12))
entry_num_vars.grid(row=0, column=1, padx=10, pady=10)

# Nút tạo ô nhập hệ số
btn_create_fields = tk.Button(root, text="Tạo ô nhập hệ số", command=create_input_fields, font=("Arial", 12), bg="#4CAF50", fg="white")
btn_create_fields.grid(row=1, column=0, columnspan=2, pady=10)

# Nút xóa dữ liệu trong cửa sổ chính
btn_clear_main = tk.Button(root, text="Xóa Dữ Liệu", command=clear_main_data, font=("Arial", 12), bg="#FF5722", fg="white")
btn_clear_main.grid(row=2, column=0, columnspan=2, pady=10)

# Chạy vòng lặp chính của giao diện
root.mainloop()
