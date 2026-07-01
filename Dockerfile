FROM python:3.12-slim

# Не создаём .pyc файлы и не буферизуем вывод — удобнее смотреть логи
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Сначала копируем только requirements — чтобы кешировался слой с зависимостями
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Теперь копируем сам код
COPY main.py .

# Запускаем от непривилегированного пользователя — хорошая практика
RUN useradd --create-home appuser
USER appuser

CMD ["python", "main.py"]