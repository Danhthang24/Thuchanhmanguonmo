import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import Label, Entry, Button, messagebox

# Hàm vẽ tín hiệu dựa trên dữ liệu nhập từ người dùng
def plot_signals():
    try:
        # Lấy dữ liệu nhập từ các trường
        signal1Frequency = float(entry_signal1.get())
        signal2Frequency = float(entry_signal2.get())
        filterFrequency = float(entry_filter.get())  # Tần số cần giữ lại
        x_range = float(entry_xrange.get())  # Khoảng thời gian cho trục x

        # Tính tần số lấy mẫu tối thiểu (theo nguyên lý Nyquist)
        samplingFrequency = 2 * max(signal1Frequency, signal2Frequency) * 2  # Tăng gấp đôi để an toàn
        samplingInterval = 1 / samplingFrequency

        # Khoảng thời gian bắt đầu và kết thúc của tín hiệu
        beginTime = 0
        endTime = 10

        # Các điểm thời gian
        time = np.arange(beginTime, endTime, samplingInterval)

        # Tạo hai sóng sine
        amplitude1 = np.sin(2 * np.pi * signal1Frequency * time)
        amplitude2 = np.sin(2 * np.pi * signal2Frequency * time)

        # Tổng của hai sóng sine
        amplitude = amplitude1 + amplitude2

        # Xóa các đồ thị trước đó nếu có
        for ax in axis:
            ax.clear()

        # Biểu diễn miền thời gian của các sóng sine
        axis[0].set_title(f'Sóng sine với tần số {signal1Frequency} Hz')
        axis[0].plot(time, amplitude1)
        axis[0].set_xlabel('Thời gian')
        axis[0].set_ylabel('Biên độ')
        axis[0].set_xlim(0, x_range)  # Thiết lập trục x dựa trên giá trị nhập

        axis[1].set_title(f'Sóng sine với tần số {signal2Frequency} Hz')
        axis[1].plot(time, amplitude2)
        axis[1].set_xlabel('Thời gian')
        axis[1].set_ylabel('Biên độ')
        axis[1].set_xlim(0, x_range)  # Thiết lập trục x dựa trên giá trị nhập

        # Sóng sine kết hợp (miền thời gian)
        axis[2].set_title(f'Sóng sine với tần số kết hợp ({signal1Frequency} Hz + {signal2Frequency} Hz)')
        axis[2].plot(time, amplitude)
        axis[2].set_xlabel('Thời gian')
        axis[2].set_ylabel('Biên độ')
        axis[2].set_xlim(0, x_range)  # Thiết lập trục x dựa trên giá trị nhập

        # Miền tần số (Biến đổi Fourier)
        fourierTransform = np.fft.fft(amplitude) / len(amplitude)  # Chuẩn hóa biên độ
        frequencies = np.fft.fftfreq(len(amplitude), d=samplingInterval)

        # Bộ lọc băng tần: Chỉ giữ lại tần số do người dùng chỉ định
        tolerance = 0.1  # Cho phép khoảng dao động nhẹ quanh tần số mục tiêu
        fourierTransform[np.abs(frequencies - filterFrequency) > tolerance] = 0

        # Biểu diễn miền tần số sau khi lọc
        axis[3].set_title(f'Biến đổi Fourier sau khi lọc (chỉ giữ {filterFrequency} Hz)')
        axis[3].plot(frequencies[:len(frequencies)//2], np.abs(fourierTransform[:len(fourierTransform)//2]))
        axis[3].set_xlabel('Tần số')
        axis[3].set_ylabel('Biên độ')

        # Hiển thị và làm mới đồ thị
        plt.draw()

    except ValueError:
        messagebox.showerror("Lỗi nhập liệu", "Vui lòng nhập các giá trị số hợp lệ cho tất cả tần số và khoảng thời gian trục x.")

# Tạo cửa sổ chính
window = tk.Tk()
window.title("Máy vẽ tín hiệu")

# Thêm nhãn và trường nhập liệu cho Tần số Tín hiệu 1
Label(window, text="Nhập tần số cho Tín hiệu 1 (Hz):").grid(row=0, column=0)
entry_signal1 = Entry(window)
entry_signal1.grid(row=0, column=1)

# Thêm nhãn và trường nhập liệu cho Tần số Tín hiệu 2
Label(window, text="Nhập tần số cho Tín hiệu 2 (Hz):").grid(row=1, column=0)
entry_signal2 = Entry(window)
entry_signal2.grid(row=1, column=1)

# Thêm nhãn và trường nhập liệu cho Tần số lọc
Label(window, text="Nhập tần số cần lọc (Hz):").grid(row=2, column=0)
entry_filter = Entry(window)
entry_filter.grid(row=2, column=1)

# Thêm nhãn và trường nhập liệu cho khoảng thời gian trục x
Label(window, text="Nhập khoảng thời gian cho trục x (giây):").grid(row=3, column=0)
entry_xrange = Entry(window)
entry_xrange.grid(row=3, column=1)

# Thêm nút để kích hoạt hàm vẽ tín hiệu
Button(window, text="Vẽ tín hiệu", command=plot_signals).grid(row=4, column=1)

# Khởi tạo đồ thị
figure, axis = plt.subplots(4, 1)
plt.subplots_adjust(hspace=1)
plt.ion()  # Kích hoạt chế độ tương tác để cập nhật đồ thị
plt.show()  # Hiển thị cửa sổ đồ thị ban đầu

# Bắt đầu vòng lặp sự kiện Tkinter
window.mainloop()
