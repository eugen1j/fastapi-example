FROM python:3.9.9

EXPOSE 8000

ENV PYTHONUNBUFFERED 1

RUN pip install --no-cache-dir --upgrade pip

COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

WORKDIR /app
COPY . /app

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker", "app.web:app"]
