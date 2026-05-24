FROM python:3.14
WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY book_service ./book_service
RUN cd book_service && python ./setup_db.py

EXPOSE 3000

CMD ["python", "-m", "book_service.grpc_server"]
