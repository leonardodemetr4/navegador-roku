# Usa a imagem da Microsoft que já vem com o Chrome
FROM mcr.microsoft.com/playwright/python:v1.45.0-jammy

# Define a pasta de trabalho
WORKDIR /app

# Copia o arquivo de requisitos primeiro para instalar as bibliotecas
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o resto dos arquivos
COPY . .

# Comando para rodar o servidor na porta que o Render exige (10000)
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
