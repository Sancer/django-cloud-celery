# Usamos una imagen base de Python 3.10
FROM python:3.10-slim

ENV POETRY_VERSION=1.7.0
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Instalar Poetry con pip
RUN pip install "poetry==$POETRY_VERSION"

# No crear un entorno virtual ya que Docker ya es un entorno aislado
ENV POETRY_VIRTUALENVS_CREATE=false

# Copiar el archivo de dependencias de Poetry al directorio de trabajo
COPY pyproject.toml poetry.lock* /app/

# Instalar las dependencias del proyecto utilizando Poetry
RUN poetry install --no-root --no-dev

# Copiar el resto del proyecto al directorio de trabajo
COPY . /app

# Instrucción para ejecutar el servidor de Django al iniciar el contenedor
CMD python manage.py runserver 0.0.0.0:$PORT


