# Usa a imagem oficial da Microsoft que já tem Python e Chrome instalados
FROM mcr.microsoft.com/playwright/python:v1.46.0-jammy

# Define a pasta de trabalho
WORKDIR /app

# Copia os arquivos do seu GitHub para o servidor
COPY . .

# Instala o Flask e o servidor Gunicorn
RUN pip install flask gunicorn

# Comando para rodar o app na porta correta do Render
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
