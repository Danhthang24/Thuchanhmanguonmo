import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance
import cv2
import numpy as np

# Khai báo biến toàn cục
image = None
original_image = None

def open_image():
    global image, original_image  # Sử dụng biến toàn cục
    # Mở hộp thoại để chọn ảnh
    file_path = filedialog.askopenfilename(title="Chọn ảnh", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")])
    
    if file_path:
        # Đọc ảnh và hiển thị thông tin ban đầu
        image = Image.open(file_path)
        original_image = image.copy()  # Lưu ảnh gốc để có thể khôi phục lại

        # Hiển thị ảnh gốc
        image_tk = ImageTk.PhotoImage(image)
        label.config(image=image_tk)
        label.image = image_tk

def adjust_brightness(val):
    global image, original_image  # Sử dụng biến toàn cục
    if original_image is not None:
        enhancer = ImageEnhance.Brightness(original_image)
        image = enhancer.enhance(float(val) / 50)  # Điều chỉnh độ sáng
        update_image()
    else:
        print("Chưa mở ảnh. Vui lòng chọn ảnh trước.")

def adjust_contrast(val):
    global image, original_image  # Sử dụng biến toàn cục
    if original_image is not None:
        enhancer = ImageEnhance.Contrast(original_image)
        image = enhancer.enhance(float(val) / 50)  # Điều chỉnh độ tương phản
        update_image()
    else:
        print("Chưa mở ảnh. Vui lòng chọn ảnh trước.")

def remove_noise(val):
    global image, original_image  # Sử dụng biến toàn cục
    if original_image is not None:
        # Chuyển ảnh gốc thành mảng numpy (để xử lý với OpenCV)
        img_np = np.array(original_image)
        
        # Đảm bảo ksize là số lẻ
        ksize = int(val)
        if ksize % 2 == 0:  # Nếu ksize là số chẵn
            ksize += 1  # Tăng thêm 1 để trở thành số lẻ
        
        # Áp dụng Median Blur để giảm nhiễu
        img_np = cv2.medianBlur(img_np, ksize)
        
        image = Image.fromarray(img_np)
        update_image()
    else:
        print("Chưa mở ảnh. Vui lòng chọn ảnh trước.")

def adjust_shadows(val):
    global image, original_image  # Sử dụng biến toàn cục
    if original_image is not None:
        img_np = np.array(original_image)
        # Gamma correction để làm sáng vùng tối
        gamma = float(val) / 50  # Điều chỉnh gamma
        img_np = np.power(img_np / 255.0, gamma) * 255
        img_np = np.uint8(np.clip(img_np, 0, 255))
        image = Image.fromarray(img_np)
        update_image()
    else:
        print("Chưa mở ảnh. Vui lòng chọn ảnh trước.")

def update_image():
    global image
    image_tk = ImageTk.PhotoImage(image)
    label.config(image=image_tk)
    label.image = image_tk

def reset_image():
    global image, original_image
    if original_image is not None:
        # Khôi phục lại ảnh gốc
        image = original_image.copy()
        
        # Cập nhật ảnh và thanh trượt
        update_image()
        brightness_slider.set(50)
        contrast_slider.set(50)
        noise_slider.set(1)
        shadow_slider.set(50)
    else:
        print("Chưa mở ảnh. Vui lòng chọn ảnh trước.")

def save_image():
    global image
    if image is not None:
        # Mở hộp thoại để chọn nơi lưu ảnh
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg"), ("All Files", "*.*")])
        if file_path:
            # Lưu ảnh vào file
            image.save(file_path)
            print(f"Ảnh đã được lưu tại: {file_path}")
    else:
        print("Chưa có ảnh để lưu. Vui lòng mở và chỉnh sửa ảnh trước.")

# Khởi tạo cửa sổ giao diện Tkinter
root = tk.Tk()
root.title("Ứng dụng Tăng Cường Ảnh")

# Thêm nút chọn ảnh
btn_open = tk.Button(root, text="Chọn Ảnh", command=open_image)
btn_open.pack()

# Thêm label để hiển thị ảnh
label = tk.Label(root)
label.pack()

# Thanh trượt để điều chỉnh độ sáng (dài hơn và mỏng hơn)
brightness_slider = tk.Scale(root, from_=1, to=100, orient="horizontal", label="Độ Sáng", command=adjust_brightness, length=600, width=15)
brightness_slider.set(50)  # Giá trị mặc định
brightness_slider.pack()

# Thanh trượt để điều chỉnh độ tương phản (dài hơn và mỏng hơn)
contrast_slider = tk.Scale(root, from_=1, to=100, orient="horizontal", label="Độ Tương Phản", command=adjust_contrast, length=600, width=15)
contrast_slider.set(50)  # Giá trị mặc định
contrast_slider.pack()

# Thanh trượt để điều chỉnh bộ lọc nhiễu (dài hơn và mỏng hơn)
noise_slider = tk.Scale(root, from_=1, to=15, orient="horizontal", label="Lọc Nhiễu", command=remove_noise, length=600, width=15)
noise_slider.set(1)  # Giá trị mặc định
noise_slider.pack()

# Thanh trượt để điều chỉnh làm sáng vùng tối (dài hơn và mỏng hơn)
shadow_slider = tk.Scale(root, from_=1, to=100, orient="horizontal", label="Làm Sáng Vùng Tối", command=adjust_shadows, length=600, width=15)
shadow_slider.set(50)  # Giá trị mặc định
shadow_slider.pack()

# Nút "Xóa Dữ Liệu" để khôi phục lại ảnh gốc và đặt lại thanh trượt
btn_reset = tk.Button(root, text="Xóa Dữ Liệu", command=reset_image)
btn_reset.pack()

# Nút "Lưu ảnh" để lưu ảnh sau khi chỉnh sửa
btn_save = tk.Button(root, text="Lưu Ảnh", command=save_image)
btn_save.pack()

# Chạy ứng dụng Tkinter
root.mainloop()
