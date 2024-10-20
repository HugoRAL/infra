# Usando a imagem oficial do Python
FROM python:3.10

# Define o diretório de trabalho
WORKDIR /app

# Copia o requirements.txt e instala as dependências
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação
COPY . .

# Expõe a porta em que a aplicação vai rodar
EXPOSE 5001

# Comando para rodar a aplicação
CMD ["python", "app.py"]
