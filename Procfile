web: uvicorn app.web:app --host 0.0.0.0 --port $PORT --limit-concurrency 50
worker: periodiq app.worker & dramatiq app.worker -t 10 -p 2 & wait -n
release: alembic upgrade head
