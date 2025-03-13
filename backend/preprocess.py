import os
import torch
import numpy as np
from transformers import AutoModel, AutoTokenizer

# Load PhoBERT model & tokenizer
phobert = AutoModel.from_pretrained("vinai/phobert-base")
tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")

# Hàm đọc tất cả bài viết trong thư mục `data/chude/`
def load_documents(folder_path):
    documents = []  # Lưu danh sách (chủ đề, bài viết, nội dung)
    for chude in os.listdir(folder_path):
        chude_path = os.path.join(folder_path, chude)
        if os.path.isdir(chude_path):  # Chỉ xử lý thư mục
            for filename in os.listdir(chude_path):
                if filename.endswith(".txt"):  # Chỉ lấy file .txt
                    file_path = os.path.join(chude_path, filename)
                    with open(file_path, "r", encoding="utf-8") as file:
                        documents.append((chude, filename, file.read().strip()))
    return documents

# Hàm lấy embedding từ PhoBERT
def get_embedding(text):
    tokens = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=256)
    with torch.no_grad():
        outputs = phobert(**tokens)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

# Load dữ liệu từ `data/`
folder_path = "data"
documents = load_documents(folder_path)

# Chuyển văn bản thành vector
print("⏳ Mã hóa lại tài liệu, vui lòng chờ...")
document_vectors = np.array([get_embedding(text) for _, _, text in documents])
document_index = np.array([(chude, filename) for chude, filename, _ in documents])

# Lưu vào file .npy
np.save("document_vectors.npy", document_vectors)
np.save("document_index.npy", document_index)

print(f"✅ Đã mã hoá {len(documents)} văn bản!!!")
