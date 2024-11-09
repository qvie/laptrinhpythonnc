import tkinter as tk
from tkinter import ttk  # Thư viện cho ComboBox

from db import db, Role, User

# Hàm lưu bản dịch vào cơ sở dữ liệu
def save_translation_to_db(source_language, target_language, input_text, translated_text):
    try:
        # Tạo logic lưu dữ liệu vào database (tùy chỉnh thêm nếu cần)
        print(f"Đã lưu bản dịch từ {source_language} sang {target_language}: {translated_text[:50]}...")
    except Exception as e:
        print(f"Đã xảy ra lỗi khi lưu bản dịch: {e}")

from translator import translate_text

# Thiết lập cửa sổ GUI
window = tk.Tk()
window.title("Trình dịch ngôn ngữ")

# Nhãn và ô nhập liệu cho văn bản
input_label = tk.Label(window, text="Nhập văn bản:")
input_label.pack()

input_box = tk.Text(window, height=5, width=50)  # Ô nhập nhiều dòng
input_box.pack()

# Chọn ngôn ngữ nguồn
source_label = tk.Label(window, text="Chọn ngôn ngữ nguồn:")
source_label.pack()

source_lang = ttk.Combobox(window)
source_lang['values'] = ["English", "Vietnamese", "Chinese (Simplified)", "Japanese", "Korean", "Thai", "Lao", "Spanish (Argentina)", "Portuguese (Brazil)"]
source_lang.current(1)  # Mặc định là Tiếng Anh (English)
source_lang.pack()

# Chọn ngôn ngữ đích
target_label = tk.Label(window, text="Chọn ngôn ngữ đích:")
target_label.pack()

target_lang = ttk.Combobox(window)
target_lang['values'] = ["English", "Vietnamese", "Chinese (Simplified)", "Japanese", "Korean", "Thai", "Lao", "Spanish (Argentina)", "Portuguese (Brazil)"]
target_lang.current(0)  # Mặc định là Tiếng Việt (Vietnamese)
target_lang.pack()

# Nút dịch
def on_translate():
    input_text = input_box.get("1.0", "end-1c")
    source_language = source_lang.get()
    target_language = target_lang.get()
    
    # Dịch văn bản
    translated_text = translate_text(source_language, target_language, input_text)
    
    # Hiển thị kết quả dịch
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, translated_text)
    
    # Lưu vào cơ sở dữ liệu
    save_translation_to_db(source_language, target_language, input_text, translated_text)

translate_button = tk.Button(window, text="Dịch", command=on_translate)
translate_button.pack()

# Nhãn và ô đầu ra cho văn bản đã dịch
output_label = tk.Label(window, text="Văn bản đã dịch:")
output_label.pack()

output_box = tk.Text(window, height=5, width=50)  # Ô đầu ra nhiều dòng
output_box.pack()

# Bắt đầu vòng lặp Tkinter
window.mainloop()
