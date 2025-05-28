import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import pandas as pd

root = tk.Tk()
root.title("CSV Uploader Application")
root.geometry("600x600")

title_label = tk.Label(root, text="CSV Uploader", font=("Arial", 18))
title_label.pack(pady=10)

data_frame = tk.Text(root, wrap="none", height=20, width=70)
data_frame.pack(pady=10)

df = None
current_df = None  

def upload_csv():
    global df, current_df
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        try:
            df = pd.read_csv(file_path)
            current_df = df.copy()
            data_frame.delete("1.0", tk.END)
            data_frame.insert(tk.END, df.head().to_string(index=False))
            messagebox.showinfo("Thành công", "Đã tải file CSV thành công!")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc file: {e}")

def sort_csv():
    global df, current_df
    if df is None:
        messagebox.showwarning("Chưa có dữ liệu", "Vui lòng tải file CSV trước.")
        return
    col_name = simpledialog.askstring("Sắp xếp", "Nhập tên cột để sắp xếp:")
    if col_name and col_name in df.columns:
        try:
            sorted_df = df.sort_values(by=col_name)
            current_df = sorted_df
            data_frame.delete("1.0", tk.END)
            data_frame.insert(tk.END, sorted_df.head().to_string(index=False))
            messagebox.showinfo("Thành công", f"Đã sắp xếp theo cột '{col_name}'")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Sắp xếp thất bại: {e}")
    else:
        messagebox.showerror("Lỗi", "Tên cột không tồn tại.")

def search_by_name():
    global df, current_df
    if df is None:
        messagebox.showwarning("Chưa có dữ liệu", "Vui lòng tải file CSV trước.")
        return
    name = simpledialog.askstring("Tìm kiếm", "Nhập tên cần tìm:")
    if name:
        try:
            filtered_df = df[df["Tên"].str.contains(name, case=False, na=False)]
            if filtered_df.empty:
                messagebox.showinfo("Kết quả", "Không tìm thấy kết quả.")
            else:
                current_df = filtered_df
                data_frame.delete("1.0", tk.END)
                data_frame.insert(tk.END, filtered_df.to_string(index=False))
        except Exception as e:
            messagebox.showerror("Lỗi", f"Tìm kiếm thất bại: {e}")

def show_original():
    global df, current_df
    if df is None:
        messagebox.showwarning("Chưa có dữ liệu", "Vui lòng tải file CSV trước.")
        return
    try:
        current_df = df.copy()
        data_frame.delete("1.0", tk.END)
        data_frame.insert(tk.END, df.head(100).to_string(index=False))
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể hiển thị dữ liệu: {e}")

def export_csv():
    global current_df
    if current_df is None:
        messagebox.showwarning("Chưa có dữ liệu", "Vui lòng tải hoặc xử lý dữ liệu trước.")
        return

    save_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                              filetypes=[("CSV files", "*.csv")],
                                              title="Lưu dữ liệu thành file CSV")
    if save_path:
        try:
            current_df.to_csv(save_path, index=False)
            messagebox.showinfo("Thành công", f"Đã lưu dữ liệu ra file:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu file: {e}")

buttons = [
    ("Tải file CSV", upload_csv),
    ("Sắp xếp dữ liệu", sort_csv),
    ("Tìm kiếm theo Tên", search_by_name),
    ("Xem lại toàn bộ", show_original),
    ("Xuất dữ liệu ra file CSV", export_csv),
]

for text, command in buttons:
    tk.Button(root, text=text, command=command).pack(pady=5)

root.mainloop()
