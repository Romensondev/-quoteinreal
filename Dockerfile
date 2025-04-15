# Dockerfile

# Imagem base com Python
FROM python:3.10-slim

# Evita prompts interativos durante build
ENV DEBIAN_FRONTEND=noninteractive

# Define diretório de trabalho dentro do container
WORKDIR /app

# Copia os arquivos do app para dentro do container
COPY . /app

# Atualiza pip e instala dependências
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir dash yfinance pandas plotly

# Expõe a porta padrão do Dash
EXPOSE 8050

# Comando para rodar o app
CMD ["python", "app.py"]
