FROM node:18 as build

WORKDIR 'app/'

COPY package*.json ./
RUN npm install

COPY .  . 

RUN npm run build
RUN python -m http.server 5500


