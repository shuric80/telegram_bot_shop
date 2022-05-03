FROM python-3.8-slim

ENV PYTHONBUFFERED 1

WORKDIR /app
COPY . /app

RUN python -m pip install --upgrade pip && pip install --no-cache-dir --no-deps -r /app/requirements.txt

CMD ['python', 'main']