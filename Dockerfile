FROM node:20 AS build
WORKDIR /app
ARG MODE=${MODE}

COPY package.json webpack.config.cjs ./
COPY app/static/js ./app/static/js
COPY app/static/images/ ./app/static/images/

RUN npm install && npm run build

FROM python:3.12-slim
WORKDIR /app

COPY . .
COPY --from=build /app/app/static/js/dist/bundle.js /app/app/static/js/dist/bundle.js

RUN pip install -r requirements.txt

COPY create_superuser.py /app/create_superuser.py
COPY wait_for_neo4j.py /app/wait_for_neo4j.py
RUN chmod +x /app/wait_for_neo4j.py

CMD ["sh", "-c", "python /app/wait_for_neo4j.py && python manage.py migrate && python /app/create_superuser.py && python manage.py runserver 0.0.0.0:80"]
