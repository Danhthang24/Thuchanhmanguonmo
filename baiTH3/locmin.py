import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk

# Định nghĩa kích thước cố định cho ảnh
DISPLAY_WIDTH = 300
DISPLAY_HEIGHT = 300

# Hàm chọn ảnh
def select_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        global img, processed_img
        img = cv2.imread(file_path)
        processed_img = img.copy()
        display_image(img, lbl_image_original)
        display_image(processed_img, lbl_image_processed)

# Hàm hiển thị ảnh với kích thước cố định
def display_image(image, label):
    # Chuyển đổi sang RGB và điều chỉnh kích thước ảnh theo tỉ lệ
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    h, w = image.shape[:2]
    scale = min(DISPLAY_WIDTH / w, DISPLAY_HEIGHT / h)
    new_size = (int(w * scale), int(h * scale))
    resized_image = cv2.resize(image, new_size)

    # Chuyển đổi ảnh thành định dạng có thể hiển thị
    img_pil = Image.fromarray(resized_image)
    img_tk = ImageTk.PhotoImage(img_pil)
    label.config(image=img_tk)
    label.image = img_tk

# Hàm áp dụng bộ lọc làm mịn
def apply_filter(val):
    global img, processed_img
    if img is None:
        return

    filter_type = filter_var.get()
    kernel_size = int(kernel_slider.get())

    # Đảm bảo kernel là số lẻ
    if kernel_size % 2 == 0:
        kernel_size += 1

    if filter_type == "Gaussian":
        processed_img = cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)
    elif filter_type == "Median":
        processed_img = cv2.medianBlur(img, kernel_size)
    elif filter_type == "Average":
        processed_img = cv2.blur(img, (kernel_size, kernel_size))

    display_image(processed_img, lbl_image_processed)

# Hàm xóa dữ liệu (reset ảnh và các giá trị)
def clear_data():
    global img, processed_img
    img = None
    processed_img = None
    lbl_image_original.config(image=None, text="Ảnh Gốc")
    lbl_image_processed.config(image=None, text="Ảnh Sau Xử Lý")
    kernel_slider.set(3)
    filter_var.set("Gaussian")
# Hàm lưu ảnh
def save_image():
    if processed_img is None:
        return
    # Chọn vị trí và tên tệp lưu ảnh
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
    if file_path:
        # Lưu ảnh
        cv2.imwrite(file_path, processed_img)

# Thiết lập giao diện chính
root = tk.Tk()
root.title("Ứng dụng Lọc Làm Mịn Ảnh")

# Khung chọn ảnh và hiển thị
btn_select = ttk.Button(root, text="Chọn Ảnh", command=select_image)
btn_select.pack(pady=10)

# Hiển thị ảnh gốc và ảnh sau xử lý
frame_images = tk.Frame(root)
frame_images.pack()

lbl_image_original = tk.Label(frame_images, text="Ảnh Gốc", width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT)
lbl_image_original.grid(row=0, column=0, padx=10, pady=10)
lbl_image_processed = tk.Label(frame_images, text="Ảnh Sau Xử Lý", width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT)
lbl_image_processed.grid(row=0, column=1, padx=10, pady=10)

# Chọn bộ lọc
filter_var = tk.StringVar(value="Gaussian")
frame_filter = tk.Frame(root)
frame_filter.pack(pady=5)
ttk.Label(frame_filter, text="Chọn bộ lọc:").pack(side="left")
ttk.Radiobutton(frame_filter, text="Gaussian", variable=filter_var, value="Gaussian").pack(side="left")
ttk.Radiobutton(frame_filter, text="Median", variable=filter_var, value="Median").pack(side="left")
ttk.Radiobutton(frame_filter, text="Average", variable=filter_var, value="Average").pack(side="left")

# Thanh trượt điều chỉnh kích thước kernel
frame_slider = tk.Frame(root)
frame_slider.pack(pady=10)
ttk.Label(frame_slider, text="Kích thước kernel:").pack(side="left")
kernel_slider = tk.Scale(frame_slider, from_=1, to=21, orient="horizontal", command=apply_filter)
kernel_slider.set(3)
kernel_slider.pack(side="left")
# Thêm nút "Lưu Ảnh" vào giao diện
btn_save = ttk.Button(root, text="Lưu Ảnh", command=save_image)
btn_save.pack(pady=10)

# Nút Xóa Dữ Liệu
btn_clear = ttk.Button(root, text="Xóa Dữ Liệu", command=clear_data)
btn_clear.pack(pady=10)

# Chạy ứng dụng
root.mainloop()
