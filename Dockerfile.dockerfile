# Python 3.11 slim sürümünden başla
FROM python:3.11-slim

# Sistemde pikepdf için gerekli olan qpdf bağımlılığını kur
RUN apt-get update && apt-get install -y qpdf gcc g++ libglib2.0-dev && rm -rf /var/lib/apt/lists/*

# Çalışma klasörü oluştur
WORKDIR /app

# Dosyaları kopyala
COPY . /app

# Python kütüphanelerini yükle
RUN pip install --no-cache-dir -r requirements.txt

# Port belirle
EXPOSE 8000

# Uygulamayı başlat
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
