import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Đọc dữ liệu từ file CSV
df = pd.read_csv("Student_Performance.csv")

# Tìm các giá trị thống kê cơ bản
thong_ke_co_ban = df.describe()  # Thống kê bao gồm min, max, mean, std, v.v.
print("Thống kê cơ bản của dữ liệu:")
print(thong_ke_co_ban)

# Tìm giá trị lớn nhất, nhỏ nhất, và trung bình của từng cột
print("\nGiá trị lớn nhất của từng cột:")
print(df.max())

print("\nGiá trị nhỏ nhất của từng cột:")
print(df.min())

print("\nGiá trị trung bình của từng cột:")
print(df.mean())

# Vẽ các đồ thị phân bố
plt.figure(figsize=(12, 8))
for i, column in enumerate(df.columns, 1):
    plt.subplot(2, 3, i)
    sns.histplot(df[column], kde=True, bins=20)
    plt.title(f'Phân bố của {column}')
plt.tight_layout()
plt.show()

# Vẽ đồ thị tương quan giữa các biến
plt.figure(figsize=(10, 6))
sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
plt.title("Ma trận tương quan giữa các biến")
plt.show()
