FROM python:3.12

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir fastapi uvicorn pydantic requests openenv-core

CMD ["python", "-m", "uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]