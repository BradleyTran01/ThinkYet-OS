# ThinkYet OS (Hermes Function Calling - Việt hóa)

Đây là kho mã nguồn của **ThinkYet OS** (được fork và phát triển dựa trên Hermes Large Language Model). ThinkYet OS hỗ trợ thực thi gọi hàm (function calling) và định dạng JSON theo schema đã cung cấp.

## 🛠️ Cài đặt

Để cài đặt các thư viện cần thiết, hãy chạy lệnh sau:

```bash
pip install -r requirements.txt
```

## 🚀 Hướng dẫn sử dụng

### 1. Gọi hàm (Function Calling)

Để chạy thử nghiệm gọi hàm với một câu truy vấn, sử dụng lệnh:

```bash
python functioncall.py --query "Tôi cần biết giá cổ phiếu hiện tại của Tesla (TSLA)"
```

### 2. Chế độ xuất dữ liệu JSON (JSON Mode)

Để chạy thử nghiệm xuất dữ liệu định dạng JSON:

```bash
python jsonmode.py --query "Vui lòng trả về một đối tượng JSON đại diện cho nhân vật Goku trong bộ phim 7 viên ngọc rồng?"
```

#### Tham số dòng lệnh (Command Line Arguments)

- `--model_path`: Đường dẫn tới mô hình (Mặc định: "NousResearch/Hermes-2-Pro-Llama-3-8B").
- `--chat_template`: Template trò chuyện định dạng prompt (Mặc định: "chatml").
- `--num_fewshot`: Tùy chọn thêm ví dụ mẫu (few-shot) (Mặc định: None).
- `--load_in_4bit`: Tùy chọn tải mô hình định dạng 4-bit với bitsandbytes (Mặc định: "False").
- `--query`: Câu hỏi / Truy vấn mẫu để gọi hàm (Mặc định: "Tôi cần biết giá cổ phiếu hiện tại của Tesla (TSLA)").
- `--max_depth`: Số lần lặp lại tối đa (Mặc định: 5).

## 💡 Thêm hàm tùy chỉnh (Custom Functions)

Bạn có thể bổ sung các hàm tùy chỉnh của riêng bạn trong tệp `functions.py`. Tệp này chứa các hàm khai báo công cụ được tích hợp sẵn.
