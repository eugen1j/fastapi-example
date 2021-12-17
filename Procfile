web: uvicorn app.web:app --host 0.0.0.0 --port $PORT --limit-concurrency 50
queue: dramatiq app.worker -t 10 -p 2
cron: periodiq app.worker
release: alembic upgrade head
