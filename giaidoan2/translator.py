import requests

# Từ điển ánh xạ giữa tên ngôn ngữ và mã ngôn ngữ
language_codes = {
    "Vietnamese": "vi",
    "English": "en",
    "Chinese (Simplified)": "zh-CN",
    "Japanese": "ja",
    "Korean": "ko",
    "Thai": "th",
    "Lao": "lo",
    "Spanish (Argentina)": "es",
    "Portuguese (Brazil)": "pt-BR"
}

# Hàm dịch văn bản
def translate_text(source_lang, target_lang, input_text):
    # Lấy mã ngôn ngữ từ tên ngôn ngữ
    source_language = language_codes[source_lang]
    target_language = language_codes[target_lang]

    # Thiết lập các tham số cho API dịch thuật
    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        "client": "gtx",  # Khách hàng (Google Translate)
        "sl": source_language,  # Ngôn ngữ nguồn
        "tl": target_language,  # Ngôn ngữ đích
        "dt": "t",  # Loại dữ liệu cần lấy (dịch)
        "q": input_text  # Văn bản cần dịch
    }

    # Gửi yêu cầu đến API
    response = requests.get(url, params=params)
    response_data = response.json()  # Chuyển đổi phản hồi sang định dạng JSON

    # Lấy kết quả dịch
    translated_text = response_data[0][0][0]
    
    return translated_text
