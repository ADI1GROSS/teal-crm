# 1. השתמש בגרסת Python גדולה יותר (לא slim) שמגיעה עם תמיכה טובה יותר.
# הבחירה ב-3.11-slim-buster/bullseye היא לרוב טובה, אבל נשתמש ב-Bullseye כדי לוודא שיש תמיכה עדכנית.
FROM python:3.11-slim-bullseye

# 2. הגדרת משתני סביבה
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y \
    # תלויות קריטיות לבנייה:
    libxml2-dev \
    libxslt1-dev \
    libffi-dev \
    pkg-config \
    # תלויות גרפיקה וגופנים (Pango & Cairo):
    libcairo2-dev \
    libpango1.0-dev \
    libgdk-pixbuf2.0-dev \
    # תלויות רינדור/תמיכת תמונה:
    libjpeg-dev \
    zlib1g-dev \
    # הוספת חבילת גופנים כללית (Critical for Hebrew/non-Latin):
    fonts-noto-cjk \
    # 💡 זה אמור לכסות את כל התלויות של WeasyPrint
    # ניקוי:
    && apt-get clean && rm -rf /var/lib/apt/lists/*
# 4. הגדרת סביבת העבודה (שאר הקוד הקיים)
WORKDIR /usr/src/app

# 5. העתקת קבצי הפרויקט
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 6. חשיפת הפורט ופקודת ההפעלה
EXPOSE 8000

CMD ["gunicorn", "tealcrm.wsgi:application", "--bind", "0.0.0.0:8000"]