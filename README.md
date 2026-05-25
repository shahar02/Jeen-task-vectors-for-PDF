# מודול פייתון ליצירת וקטורים למסמך

מודול Python שממש תהליך יצירת vectors למסמך.
הקוד קולט קובץ PDF או DOCX, מחלץ טקסט, מחלק למקטעים,
יוצר Embeddings באמצעות Gemini API ושומר הכל ב-PostgreSQL.

---

## דרישות טרם הרצה

- Python 3.11 ומעלה
- PostgreSQL 18
- מפתח Gemini API מ-aistudio.google.com

---

## התקנה

1. שכפלו את הפרויקט:
git clone https://github.com/shahar02/Jeen-task-vectors-for-PDF.git

2. התקינו ספריות:
pdfplumber
python-docx
google-genai
psycopg2-binary
pgvector
python-dotenv

3. צרו קובץ .env בתיקיית הפרויקט:
GEMINI_API_KEY=המפתח_שלכם
POSTGRES_URL=postgresql://postgres:הסיסמה_שלכם@localhost:5432/postgres

---

## שימוש

python index_documents.py "שם_הקובץ.pdf"
python index_documents.py "שם_הקובץ.docx"

---


## השלבים שהקוד עושה

1. קליטת קובץ PDF או DOCX כקלט
2. חילוץ טקסט נקי מהקובץ
3. חלוקה למקטעים — גודל קבוע 300 תווים עם חפיפה של 50
4. יצירת Embedding ב-Gemini — המרה לוקטור של 3072 מספרים
5. שמירה ב-PostgreSQL יחד עם הטקסט המקורי

---

## אבטחת מידע

מפתחות ה-API ופרטי החיבור נשמרים בקובץ .env בלבד.
קובץ זה אינו משותף ב-GitHub — מוגדר ב-.gitignore.
