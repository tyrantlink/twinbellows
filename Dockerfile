FROM python:3.11
WORKDIR /app
COPY . .
RUN python3.11 -m pip install --no-cache-dir -r requirements.txt
CMD ["python3.11","-u","main.py"]