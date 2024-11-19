import cv2
import numpy as np
from tkinter import Tk, filedialog, Button, simpledialog, messagebox

# Hàm đọc ảnh và thực hiện tách biên
def detect_edges(image_path, fixed_width=500):
    # Đọc ảnh từ file
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("Không thể mở ảnh.")
        return
    
    # Tính toán chiều cao mới để giữ nguyên tỷ lệ ảnh
    height, width = img.shape
    ratio = fixed_width / width
    new_height = int(height * ratio)
    
    # Thay đổi kích thước ảnh để giữ nguyên tỷ lệ
    resized_img = cv2.resize(img, (fixed_width, new_height))

    # Áp dụng bộ lọc Gaussian để làm mịn ảnh
    blurred_img = cv2.GaussianBlur(resized_img, (5, 5), 0)
    
    # Áp dụng thuật toán Canny để tách biên
    edges = cv2.Canny(blurred_img, 100, 200)
    
    # Hiển thị ảnh gốc và ảnh tách biên
    cv2.imshow("Original Image", resized_img)
    cv2.imshow("Edge Detection", edges)
    
    # Tùy chọn lưu ảnh
    if messagebox.askyesno("Lưu ảnh", "Bạn có muốn lưu ảnh đã tách biên không?"):
        save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg")])
        if save_path:
            cv2.imwrite(save_path, edges)
            print("Ảnh đã được lưu tại:", save_path)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Hàm để mở cửa sổ chọn file ảnh
def open_file():
    root = Tk()
    root.withdraw()  # Ẩn cửa sổ Tkinter chính
    file_path = filedialog.askopenfilename(title="Chọn ảnh", filetypes=[("Image files", "*.jpg;*.png;*.jpeg;*.bmp")])
    if file_path:
        # Nhập kích thước cố định từ người dùng
        fixed_width = simpledialog.askinteger("Kích thước", "Nhập chiều rộng cố định (px):", minvalue=100, maxvalue=2000, initialvalue=500)
        detect_edges(file_path, fixed_width)

# Tạo giao diện với nút để mở ảnh
def create_app():
    window = Tk()
    window.title("Edge Detection App")
    window.geometry("300x100")
    
    open_button = Button(window, text="Mở ảnh và Tách biên", command=open_file)
    open_button.pack(pady=20)
    
    window.mainloop()

# Chạy ứng dụng
create_app()
