# Use a imagem oficial do Python
FROM python:3.9-slim

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie os arquivos do repositório para o contêiner
COPY . /app/

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Defina a variável de ambiente PYTHONPATH para garantir que a pasta 'src' seja reconhecida
ENV PYTHONPATH="${PYTHONPATH}:/app/src"

# Comando para rodar o bot (iniciando com python -m)
CMD ["python3", "-m", "src.app"]
