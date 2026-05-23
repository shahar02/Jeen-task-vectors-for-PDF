import os
import json
import pdfplumber
from google import genai
from dotenv import load_dotenv
import psycopg2

# ───── טוען מפתחות מקובץ .env ─────
load_dotenv()
API_KEY      = os.getenv("GEMINI_API_KEY")
POSTGRES_URL = os.getenv("POSTGRES_URL")

client = genai.Client(api_key=API_KEY)

# ───── שלב 1: חילוץ טקסט מ-PDF ─────
def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

# ───── שלב 2: חיתוך לצנקס ─────
def chunk_fixed_size(text, chunk_size=300, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

# ───── שלב 3: Embedding מגמיני ─────
def get_embedding(text):
    result = client.models.embed_content(
        model="gemini-embedding-2",
        contents=text
    )
    return result.embeddings[0].values

# ───── שלב 4: שמירה ב-PostgreSQL ─────
def save_to_db(chunks, embeddings, filename, strategy):
    conn = psycopg2.connect(POSTGRES_URL)
    cur  = conn.cursor()

    # יצירת טבלה אם לא קיימת
    cur.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id            SERIAL PRIMARY KEY,
            chunk_text    TEXT,
            embedding     JSONB,
            filename      TEXT,
            split_strategy TEXT,
            created_at    TIMESTAMP DEFAULT NOW()
        )
    """)

    # הכנסת כל צנקס
    for chunk, emb in zip(chunks, embeddings):
        cur.execute("""
            INSERT INTO documents (chunk_text, embedding, filename, split_strategy)
            VALUES (%s, %s, %s, %s)
        """, (chunk, json.dumps(emb), filename, strategy))

    conn.commit()
    cur.close()
    conn.close()
    print(f"נשמרו {len(chunks)} צנקס בהצלחה!")

# ───── הרצה ראשית ─────
if __name__ == "__main__":
    file_path = "מטלת בית Solutions - .pdf"
    strategy  = "fixed"

    print("שלב 1: קורא קובץ...")
    text = extract_text_from_pdf(file_path)
    print(f"חולץ {len(text)} תווים")

    print("שלב 2: חותך לחנקס...")
    chunks = chunk_fixed_size(text)
    print(f"נוצרו {len(chunks)} צנקס")

    print("שלב 3: שולח לגמיני...")
    embeddings = [get_embedding(c) for c in chunks]
    print(f"התקבלו {len(embeddings)} embeddings")

    print("שלב 4: שומר ב-PostgreSQL...")
    save_to_db(chunks, embeddings, file_path, strategy)

    print("\n✅ הכל הושלם בהצלחה!")