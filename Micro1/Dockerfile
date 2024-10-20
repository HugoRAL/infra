# Usa uma imagem oficial do Python
FROM python:3.9-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos necessários para o diretório de trabalho
COPY requirements.txt requirements.txt
COPY app.py .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Exponha a porta que o Flask vai rodar
EXPOSE 5000

# Comando para rodar a aplicação
CMD ["python", "app.py"]