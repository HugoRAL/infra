# Utiliza uma imagem base do Python
FROM python:3.9-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos para o diretório de trabalho
COPY requirements.txt requirements.txt
COPY app.py app.py

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta do Flask
EXPOSE 5000

# Comando para iniciar o serviço
CMD ["python", "app.py"]
