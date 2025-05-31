FROM python:3.11-slim

WORKDIR /app

COPY src/main.py requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

ENV LFS_STORAGE_PATH=/data/lfs

VOLUME ["/data/lfs"]

EXPOSE 5000

CMD ["python", "main.py"]
