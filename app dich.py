import tkinter as tk
import requests

def translate_text():
    # Lấy văn bản từ ô nhập liệu
    input_text = input_box.get("1.0", "end-1c")

    # Thiết lập các tham số cho API dịch thuật
    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        "client": "gtx",  # Khách hàng (Google Translate)
        "sl": "en",  # Ngôn ngữ nguồn (Tiếng Anh)
        "tl": "vi",  # Ngôn ngữ đích (Tiếng Việt)
        "dt": "t",  # Loại dữ liệu cần lấy (dịch)
        "q": input_text  # Văn bản cần dịch
    }

    # Gửi yêu cầu đến API
    response = requests.get(url, params=params)
    response_data = response.json()  # Chuyển đổi phản hồi sang định dạng JSON

    # Lấy kết quả dịch
    translated_text = response_data[0][0][0]

    # Hiển thị văn bản đã dịch trong ô đầu ra
    output_box.delete("1.0", tk.END)  # Xóa nội dung cũ
    output_box.insert(tk.END, translated_text)  # Chèn văn bản đã dịch

# Thiết lập cửa sổ GUI
window = tk.Tk()
window.title("Trình dịch Tiếng Anh sang Tiếng Việt")

# Nhãn và ô nhập liệu cho văn bản
input_label = tk.Label(window, text="Nhập văn bản tiếng Anh:")
input_label.pack()

input_box = tk.Text(window, height=5, width=50)  # Ô nhập nhiều dòng
input_box.pack()

# Nút dịch
translate_button = tk.Button(window, text="Dịch", command=translate_text)
translate_button.pack()

# Nhãn và ô đầu ra cho văn bản đã dịch
output_label = tk.Label(window, text="Văn bản đã dịch sang tiếng Việt:")
output_label.pack()

output_box = tk.Text(window, height=5, width=50)  # Ô đầu ra nhiều dòng
output_box.pack()

# Bắt đầu vòng lặp Tkinter
window.mainloop()