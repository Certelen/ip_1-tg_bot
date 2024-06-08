FROM python:3.11-slim

WORKDIR /app

COPY ./backend ./

RUN pip3 install -r requirements.txt --no-cache-dir

CMD ["uvicorn", "backend.asgi:application", "--host", "0.0.0.0" ,"--port" ,"8000"]
