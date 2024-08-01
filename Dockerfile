FROM python:3.11

WORKDIR /app
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -v git+https://github.com/Mayuri-Chan/pyrofork
RUN pip install --no-cache-dir -v -r requirements.txt

COPY . .
EXPOSE 8080
CMD ["python3", "main.py"]
