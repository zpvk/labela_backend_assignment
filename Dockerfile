FROM python:3.10
LABEL author='Label A'

WORKDIR /app

# Environment
RUN apt-get update && apt-get install -y bash vim nano postgresql-client \
    && pip install --upgrade pip \
    && pip install --no-cache-dir flake8==3.8.4 uWSGI

# Copy requirements and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the codebase into the container
COPY . .

RUN ./manage.py collectstatic --noinput

# Ops Parameters
ENV WORKERS=2 \
    PORT=8000 \
    PYTHONUNBUFFERED=1 \
    DB_NAME=postgres \
    DB_USER=postgres \
    DB_PASSWORD=postgres \
    DB_HOST=db \
    DB_PORT=5432

EXPOSE ${PORT}

# Make the wait-for-postgres.sh script executable

COPY ./wait-for-db.sh ./wait-for-db.sh
RUN chmod +x ./wait-for-db.sh

CMD /wait-for-postgres.sh db set -xe; \
    python3 manage.py collectstatic --noinput --clear; \
    python3 manage.py makemigrations; \
    python3 manage.py migrate --noinput; \
    python3 manage.py loaddata fixtures/db_data.json; \
    DJANGO_SUPERUSER_PASSWORD=admin python3 manage.py createsuperuser --username 'admin' --email 'admin@email.com'; \
    python3 manage.py runserver 0.0.0.0:${PORT}

