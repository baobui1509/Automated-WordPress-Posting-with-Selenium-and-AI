import tkinter as tk
from tkinter import filedialog
import csv
import json
# from generate_articles_gemini_API import *
from generate_articles_gpt_API import *

# Đường dẫn đến tệp lưu trữ dữ liệu
SAVE_FILE_PATH = "saved_content.json"
prompt1_content = ''
prompt2_content = ''
prompt3_content = ''
prompt4_content = ''

def save_content():
    """Lưu nội dung của các Textarea vào tệp JSON"""
    content = {
        "prompt1": text_area1.get("1.0", tk.END).strip(),
        "prompt2": text_area2.get("1.0", tk.END).strip(),
        "prompt3": text_area3.get("1.0", tk.END).strip(),
        "prompt4": text_area4.get("1.0", tk.END).strip(),
        "number": number_var.get(),
        "image": image_number_var.get(),
        "category": category_var.get().strip(),
        "get_image": checkbox_var1.get(),
        "publish": checkbox_var2.get()
    }
    try:
        with open(SAVE_FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(content, f, ensure_ascii=False, indent=4)
        print("Dữ liệu đã được lưu.")
    except Exception as e:
        print(f"Lỗi khi lưu dữ liệu: {e}")

def load_content():
    """Tải nội dung đã lưu từ tệp JSON"""
    try:
        with open(SAVE_FILE_PATH, "r", encoding="utf-8") as f:
            content = json.load(f)
            text_area1.insert(tk.END, content.get("prompt1", ""))
            text_area2.insert(tk.END, content.get("prompt2", ""))
            text_area3.insert(tk.END, content.get("prompt3", ""))
            text_area4.insert(tk.END, content.get("prompt4", ""))
            number_var.set(content.get("number", 1))
            image_number_var.set(content.get("image", 0))
            category_var.set(content.get("category", ""))
            checkbox_var1.set(content.get("get_image"))
            checkbox_var2.set(content.get("publish"))
        print("Dữ liệu đã được tải.")
    except FileNotFoundError:
        print("Tệp lưu trữ không tồn tại. Chưa có dữ liệu trước đó.")
    except Exception as e:
        print(f"Lỗi khi tải dữ liệu: {e}")

def handle_action():
    """Xử lý khi bấm nút"""
    # Lấy nội dung từ Textarea
    prompt1_content = text_area1.get("1.0", tk.END).strip()
    prompt2_content = text_area2.get("1.0", tk.END).strip()
    prompt3_content = text_area3.get("1.0", tk.END).strip()
    prompt4_content = text_area4.get("1.0", tk.END).strip()

    # Lấy giá trị của checkbox
    checkbox1_status = "được chọn" if checkbox_var1.get() else "không được chọn"
    checkbox2_status = "được chọn" if checkbox_var2.get() else "không được chọn"

    # Lấy giá trị số
    google_results_number = number_var.get()

    # Lưu nội dung vào tệp khi bấm nút
    save_content()

    # Hiển thị nội dung lấy được
    result_label.config(
        text=f"Prompt 1: {prompt1_content}\n"
             f"Prompt 2: {prompt2_content}\n"
             f"Prompt 3: {prompt3_content}\n"
             f"Prompt 4: {prompt4_content}\n"
             f"Checkbox 1: {checkbox1_status}\n"
             f"Checkbox 2: {checkbox2_status}\n"
             f"Số đã nhập: {google_results_number}\n"
             f"CategoryL {category_var.get()}"
    )
    print("Các từ khóa trong file:", keywords) 
    print('google_results_number: ', google_results_number)

    main()

def adjust_text_area_size(text_area):
    """Tự động điều chỉnh kích thước của TextArea khi văn bản vượt quá kích thước ban đầu"""
    # Lấy số dòng của nội dung hiện tại
    lines = text_area.get("1.0", tk.END).splitlines()
    num_lines = len(lines) - 1  # Loại bỏ dòng cuối (dòng trống của END)

    # Điều chỉnh chiều cao của TextArea dựa trên số dòng
    if num_lines > 5:
        text_area.config(height=num_lines + 2)  # Tăng chiều cao của TextArea

def choose_file():
    """Chọn file từ máy tính và đọc nội dung CSV"""
    file_path = filedialog.askopenfilename(title="Chọn file", filetypes=[("CSV files", "*.csv")])
    if file_path:
        file_label.config(text=f"File đã chọn: {file_path}")
        # Đọc nội dung của file CSV
        try:
            with open(file_path, newline='', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row:  # Kiểm tra nếu dòng không rỗng
                        keywords.append(row[0])  # Lưu keyword vào danh sách
            # print("Các từ khóa trong file:", keywords)  # In ra các từ khóa

            # Nếu muốn hiển thị danh sách từ khóa trong giao diện
            # file_content_label.config(text=f"Các từ khóa trong file:\n{', '.join(keywords)}")
        except Exception as e:
            file_content_label.config(text=f"Lỗi khi đọc file: {e}")
    else:
        file_label.config(text="Không chọn file nào.")


# Tạo cửa sổ giao diện
root = tk.Tk()
root.title("ANH BẢO BÙI")

# Chọn file CSV
file_button = tk.Button(root, text="Chọn file CSV", command=choose_file)
file_button.pack(pady=5)

# Nhãn hiển thị thông tin file
file_label = tk.Label(root, text="Chưa chọn file nào.")
file_label.pack(pady=5)

# Prompt 1
tk.Label(root, text="Prompt 1:").pack(pady=5)
text_area1 = tk.Text(root, height=5, width=40)
text_area1.pack(pady=5)

# Prompt 2
tk.Label(root, text="Prompt 2:").pack(pady=5)
text_area2 = tk.Text(root, height=5, width=40)
text_area2.pack(pady=5)

# Prompt 3
tk.Label(root, text="Prompt 3:").pack(pady=5)
text_area3 = tk.Text(root, height=5, width=40)
text_area3.pack(pady=5)

# Prompt 4
tk.Label(root, text="Prompt 4:").pack(pady=5)
text_area4 = tk.Text(root, height=5, width=40)
text_area4.pack(pady=5)

# Số lượng URL
number_frame = tk.Frame(root)
number_frame.pack(pady=5)
tk.Label(number_frame, text="Số lượng URL:").pack(side="left", padx=5)
number_var = tk.IntVar(value=1)
number_input = tk.Spinbox(number_frame, from_=1, to=100, textvariable=number_var, width=10)
number_input.pack(side="left", padx=5)

# Số lượng image
image_number_frame = tk.Frame(root)
image_number_frame.pack(pady=5)
tk.Label(image_number_frame, text="Số lượng image:").pack(side="left", padx=5)
image_number_var = tk.IntVar(value=1)
image_number_input = tk.Spinbox(image_number_frame, from_=1, to=100, textvariable=image_number_var, width=10)
image_number_input.pack(side="left", padx=5)

# Nhập category 
category_frame = tk.Frame(root)
category_frame.pack(pady=5)
tk.Label(category_frame, text="Category:").pack(side="left", padx=5)
category_var = tk.StringVar()
category_entry = tk.Entry(category_frame, textvariable=category_var, width=15)
category_entry.pack(side="left", padx=5)



# Lắng nghe sự kiện thay đổi nội dung trong các TextArea để điều chỉnh kích thước
text_area1.bind("<KeyRelease>", lambda event: adjust_text_area_size(text_area1))
text_area2.bind("<KeyRelease>", lambda event: adjust_text_area_size(text_area2))
text_area3.bind("<KeyRelease>", lambda event: adjust_text_area_size(text_area3))
text_area4.bind("<KeyRelease>", lambda event: adjust_text_area_size(text_area4))

# Frame chứa checkbox
checkbox_frame = tk.Frame(root)
checkbox_frame.pack(pady=5)

checkbox_var1 = tk.BooleanVar()
checkbox1 = tk.Checkbutton(checkbox_frame, text="Lấy ảnh", variable=checkbox_var1)
checkbox1.pack(side="left", padx=5)

checkbox_var2 = tk.BooleanVar()
checkbox2 = tk.Checkbutton(checkbox_frame, text="Đăng bài", variable=checkbox_var2)
checkbox2.pack(side="left", padx=5)

# Nút thực hiện chức năng
action_button = tk.Button(root, text="Chạy", command=handle_action)
action_button.pack(pady=10)

# Kết quả xử lý
result_label = tk.Label(root, text="Kết quả sẽ hiển thị ở đây", wraplength=300, justify="left")
result_label.pack(pady=10)

# Tải lại nội dung đã lưu khi ứng dụng khởi động
root.after(100, load_content)

# Chạy vòng lặp giao diện
root.mainloop()

