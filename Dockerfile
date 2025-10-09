FROM node:20-alpine AS frontend-build
WORKDIR /frontend
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM python:3.10-alpine AS production
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install build deps for wheels (may be larger)
RUN apk add --no-cache build-base libffi-dev openssl-dev musl-dev linux-headers \
 && apk add --no-cache --virtual .fetch-deps curl

COPY requirements.txt .
RUN pip install -r requirements.txt
WORKDIR /app
COPY .  .
COPY --from=frontend-build /frontend/dist /app/frontend
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
