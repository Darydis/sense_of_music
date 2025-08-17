FROM python:3.11-slim
WORKDIR /app

# системные зависимости по вкусу
RUN pip install --no-cache-dir --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
# порт подхватывает платформа
EXPOSE ${PORT}

CMD ["bash", "start.sh"]
