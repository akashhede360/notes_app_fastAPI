#stage build images (install dependecies)
FROM node:20-alpine as build

WORKDIR /app

COPY package*.json ./

RUN npm install
RUN npm run build

#stage Production/Runtime Stage (Minimal image)
FROM python:3.10-alpine as production-stage

COPY  requirements.txt .

RUN pip install -r  requirements.txt

EXPOSE 8000 

CMD ["uvicorn","main:app","--host","0.0.0","--port", "8000"]



