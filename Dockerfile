# Usando a versão 1.46.0 que combina com o seu código
FROM mcr.microsoft.com/playwright/python:v1.46.0-jammy

WORKDIR /app

# Instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código
COPY . .

# Comando de início
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
