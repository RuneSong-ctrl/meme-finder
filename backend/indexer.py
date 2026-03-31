import os
import faiss
import numpy as np
import pymongo
import easyocr
from PIL import Image
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
MONGO_URI = os.getenv("MONGODB_URL", "mongodb://localhost:27017")

# 1. Konfigurasi Database (MongoDB)
print("Menghubungkan ke MongoDB...")
client = pymongo.MongoClient(MONGO_URI)
db = client["meme_engine_db"]
collection = db["memes"]
collection.delete_many({}) 

# 2. Inisialisasi Model CLIP (Versi Standar untuk Gambar)
print("Memuat model CLIP standar untuk memproses gambar...")
model = SentenceTransformer('clip-ViT-B-32')

# 3. Inisialisasi OCR (EasyOCR)
print("Memuat model EasyOCR untuk membaca teks pada meme...")
reader = easyocr.Reader(['id', 'en'], gpu=False)

# 4. Inisialisasi FAISS Index
embedding_dim = 512 
index = faiss.IndexFlatIP(embedding_dim)

# 5. Proses Ekstraksi Fitur & OCR (Indexing)
image_folder = "./data/images"
index_folder = "./data/index"
os.makedirs(index_folder, exist_ok=True)

image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
print(f"Ditemukan {len(image_files)} gambar untuk di-index.")

for idx, filename in enumerate(image_files):
    filepath = os.path.join(image_folder, filename)
    
    try:
        image = Image.open(filepath).convert("RGB")
    except Exception as e:
        print(f"Gagal membuka gambar {filename}: {e}")
        continue

    print(f"\nMemproses [{idx+1}/{len(image_files)}]: {filename}")
    
    # --- PROSES A: Ekstraksi Vektor Gambar (CLIP) ---
    embedding_arr = np.array([model.encode([image])[0]], dtype=np.float32)
    faiss.normalize_L2(embedding_arr)
    index.add(embedding_arr)
    
    # --- PROSES B: Ekstraksi Teks Meme (OCR) ---
    print("  -> Mengekstrak teks dari gambar...")
    # detail=0 berarti kita hanya mengambil teksnya saja, tanpa koordinat posisinya
    ocr_result = reader.readtext(filepath, detail=0) 
    extracted_text = " ".join(ocr_result)
    
    if extracted_text.strip() != "":
        print(f"  -> Teks ditemukan: '{extracted_text}'")
    else:
        print("  -> Tidak ada teks yang terdeteksi.")
    
    # --- PROSES C: Menyimpan ke MongoDB ---
    metadata = {
        "faiss_id": idx, 
        "filename": filename,
        "filepath": filepath,
        "meme_text": extracted_text  
    }
    collection.insert_one(metadata)

# 6. Simpan FAISS Index secara lokal
faiss_filepath = os.path.join(index_folder, "meme_faiss.index")
faiss.write_index(index, faiss_filepath)

print("\n=== Proses Indexing Selesai! ===")
print(f"Total vektor di FAISS: {index.ntotal}")
print(f"File index disimpan di: {faiss_filepath}")