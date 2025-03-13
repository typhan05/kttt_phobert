# Khai Thác Thông Tin

Xây dựng một hệ thống truy hồi thông tin/máy
tìm kiếm đơn giản – với giao diện dạng web sử dụng mô hình
PhoBERT

## Tech Stack

**Client:** React, TailwindCSS

**Server:** Python, PhoBERT Model VinAI

## Installation

\*\* Backend

- [Cài đặt Anaconda (môi trường để chạy Python)](https://www.anaconda.com/download/)
- [Cài đặt Python](https://www.python.org/downloads/)

\*\* Frontend

- [Cài đặt Nodejs](https://nodejs.org/en) - Node version v22.6.0 - v23.9.0
- [Cài đặt Yarn](https://classic.yarnpkg.com/lang/en/docs/install/#windows-stable) - Yarn version >=1.22.19

## Running Tests

Start Backend

```bash
  cd backend
  conda create -n ten_moi_truong python=3.12
  conda activate ten_moi_truong
  pip install -r requirements.txt
```

B1: Crawl dữ liệu từ trang báo **VNEXPRESS**

```bash
  python crawl_vnexpress.py
```

=> Dữ liệu sau khi cralw về sẽ nằm trong thư mục **data**

B2: Đọc dữ liệu đã cralw về, chuyển thành vector và lưu lại file .npy (Đã có sẵn nếu máy yếu thì bỏ qua ^\_~)

```bash
  python preprocess.py
```

=> Sau khi nén dữ liệu xong thì sẽ có 2 file **document_vectors.npy**, **document_index.npy**

B3: Start Server API Backend

```bash
  uvicorn main:app --reload
```

=> Server Backend start http://localhost:8000/docs

Start Frontend

```bash
  cd frontend
  yarn install
  yarn dev
```

Lưu Ý: Sửa file _.env.example_ => _.env_ và bỏ comment **NEXT_PUBLIC_BASE_URL** để call backend api

=> Server Frontend start http://localhost:3000
