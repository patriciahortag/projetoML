# Use a imagem base do Python
FROM python:3.9

# Instale as dependências do Python
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Instale o cliente do MySQL
RUN apt-get update && apt-get install -y default-mysql-client

# Copie o código fonte para o diretório de trabalho no contêiner
COPY . /app
COPY main.py /app/main.py

# Defina o diretório de trabalho
WORKDIR /app

# Execute o comando para iniciar o programa em Python
CMD ["python", "main.py"]
