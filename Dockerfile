# Использование официального образа Python 3.10 в качестве базового
FROM python:3.10

# Установка рабочей директории
WORKDIR /app

# Копирование всех файлов текущего каталога в рабочую директорию
COPY . /app

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Запуск Python-приложения
CMD [ "python", "main.py" ]