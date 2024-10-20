# Usa uma imagem base do Python
FROM python:3.9-slim

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia o arquivo requirements.txt e instala as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o conteúdo para o contêiner
COPY . .

# Expõe a porta 5000
EXPOSE 5003

# Comando para iniciar a aplicação Flask
CMD ["python", "app.py"]
