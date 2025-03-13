import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import torch
import numpy as np
from scipy.spatial.distance import cosine
from transformers import AutoModel, AutoTokenizer

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)

# Load PhoBERT model & tokenizer
phobert = AutoModel.from_pretrained("vinai/phobert-base")
tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")

# Tải vector từ file .npy
document_vectors = np.load("document_vectors.npy")
document_index = np.load("document_index.npy", allow_pickle=True)

# Đường dẫn thư mục chứa dữ liệu
DATA_FOLDER = "data"

# Hàm lấy embedding từ PhoBERT
def get_embedding(text):
    tokens = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=256)
    with torch.no_grad():
        outputs = phobert(**tokens)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

# Hàm tìm kiếm tài liệu liên quan
def search_similar_documents(query, top_k=5):
    try:
        query_embedding = get_embedding(query)
        similarities = [1 - cosine(query_embedding, doc_emb) for doc_emb in document_vectors]
        sorted_indices = np.argsort(similarities)[::-1]  # Sắp xếp theo độ tương đồng giảm dần
        results = [{"chude": document_index[i][0], "filename": document_index[i][1], "score": float(similarities[i])} for i in sorted_indices[:top_k]]
        
        return {
            "status": 200,
            "result": results,
            "message": "Success"
        }
    except Exception as e:
        return {
            "status": 500,
            "result": [],
            "message": str(e)
        }

# API endpoint nhận query và trả về kết quả tìm kiếm
@app.get("/api/search/")
async def search(query: str, top_k: int = 5):
    return search_similar_documents(query, top_k)

# API tải file theo filename
@app.get("/api/download")
async def download_file(filename: str):
    # Đường dẫn đầy đủ đến file
    file_path = os.path.join(DATA_FOLDER, filename)
    
    # Kiểm tra file có tồn tại không
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(file_path, filename=os.path.basename(file_path))

# Chạy API với Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
