import os
import faiss
import numpy as np
import pymongo
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGODB_URL", "mongodb://localhost:27017")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/images", StaticFiles(directory="data/images"), name="images")

# 1. Hubungkan ke Database & Index
client = pymongo.MongoClient(MONGO_URI)
collection = client["meme_engine_db"]["memes"]
index = faiss.read_index("./data/index/meme_faiss.index")

# 2. Inisialisasi Model Multilingual Teks
print("Memuat model Multilingual CLIP untuk pencarian teks...")
text_model = SentenceTransformer('clip-ViT-B-32-multilingual-v1')

# 3. Endpoint Pencarian (HYBRID SEARCH)
@app.get("/search")
def search_meme(query: str, top_k: int = 4):
    query_arr = np.array([text_model.encode([query])[0]], dtype=np.float32)
    faiss.normalize_L2(query_arr)
    distances, indices = index.search(query_arr, top_k * 2)
    
    raw_results = []
    
    for i, faiss_id in enumerate(indices[0]):
        if faiss_id != -1:
            meme_data = collection.find_one({"faiss_id": int(faiss_id)}, {"_id": 0})
            if meme_data:
                # Skor A: Kemiripan Visual dari CLIP (makin mendekati 1 makin baik)
                visual_score = float(distances[0][i])
                
                # Skor B: Pencocokan Teks (OCR)
                text_boost = 0.0
                if "meme_text" in meme_data and meme_data["meme_text"]:
                    query_words = query.lower().split()
                    meme_text_lower = meme_data["meme_text"].lower()
                    
                    # Beri bonus skor jika ada kata penting yang cocok
                    for word in query_words:
                        if len(word) > 2 and word in meme_text_lower:
                            text_boost += 0.15 # Tambahan skor 15% per kata cocok
                
                # Penggabungan Skor (Hybrid)
                final_score = visual_score + text_boost
                
                meme_data["score"] = final_score
                meme_data["visual_score"] = visual_score
                meme_data["text_boost"] = text_boost
                meme_data["image_url"] = f"http://localhost:8000/images/{meme_data['filename']}"
                
                raw_results.append(meme_data)
                
    # Urutkan ulang berdasarkan skor hibrida tertinggi, lalu potong sesuai top_k
    sorted_results = sorted(raw_results, key=lambda x: x["score"], reverse=True)[:top_k]
                
    return {"query": query, "results": sorted_results}