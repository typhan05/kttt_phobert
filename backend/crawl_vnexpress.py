# -*- coding: utf-8 -*-
import os
import re
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# Danh sách 12 chuyên mục cần crawl từ VnExpress
categories = {
    "thoi-su": "https://vnexpress.net/thoi-su",
    "the-gioi": "https://vnexpress.net/the-gioi",
    "kinh-doanh": "https://vnexpress.net/kinh-doanh",
    "giai-tri": "https://vnexpress.net/giai-tri",
    "the-thao": "https://vnexpress.net/the-thao",
    "cong-nghe": "https://vnexpress.net/cong-nghe",
    "khoa-hoc": "https://vnexpress.net/khoa-hoc",
    "suc-khoe": "https://vnexpress.net/suc-khoe",
    "phap-luat": "https://vnexpress.net/phap-luat",
    "giao-duc": "https://vnexpress.net/giao-duc",
    "doi-song": "https://vnexpress.net/doi-song",
    "du-lich": "https://vnexpress.net/du-lich",
}

# Thư mục lưu trữ dữ liệu
base_dir = "data"
os.makedirs(base_dir, exist_ok=True)

# Hàm loại bỏ ký tự đặc biệt trong tiêu đề để đặt tên file
def sanitize_filename(title):
    title = title.lower()  # Chuyển về chữ thường
    title = re.sub(r"[^\w\s]", "", title)  # Xóa ký tự đặc biệt
    title = re.sub(r"\s+", "-", title)  # Thay dấu cách bằng dấu "-"
    return title[:50]  # Giới hạn tên file tối đa 50 ký tự

# Hàm lấy danh sách bài viết từ một chuyên mục
def get_article_links(category_url, num_pages=3):
    article_links = []
    for page in range(1, num_pages + 1):
        url = f"{category_url}-p{page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        for article in soup.find_all("article"):
            link = article.find("a", href=True)
            if link and link["href"].startswith("https"):
                article_links.append(link["href"])
    
    return list(set(article_links))  # Loại bỏ trùng lặp

# Hàm lấy nội dung bài viết
def get_article_content(article_url):
    try:
        response = requests.get(article_url)
        soup = BeautifulSoup(response.text, "html.parser")

        title = soup.find("h1").text.strip() if soup.find("h1") else "khong-co-tieu-de"
        paragraphs = soup.find_all("p")
        content = "\n".join([p.get_text() for p in paragraphs if p.get_text().strip()])

        return title, content
    except Exception as e:
        print(f"Lỗi khi crawl {article_url}: {e}")
        return None, None

# Crawl dữ liệu từ các chuyên mục
for category, url in categories.items():
    print(f"Đang crawl chuyên mục: {category}...")
    article_links = get_article_links(url, num_pages=3)

    # Tạo thư mục chuyên mục nếu chưa có
    category_dir = os.path.join(base_dir, category)
    os.makedirs(category_dir, exist_ok=True)

    for article_url in tqdm(article_links, desc=f"Crawl {category}"):
        title, content = get_article_content(article_url)
        if content:
            safe_title = sanitize_filename(title)
            file_path = os.path.join(category_dir, f"{safe_title}.txt")
            
            # Tránh trùng lặp tên file
            count = 1
            while os.path.exists(file_path):
                file_path = os.path.join(category_dir, f"{safe_title}-{count}.txt")
                count += 1

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"{title}\n\n{content}")

print("Hoàn thành crawl dữ liệu!")
