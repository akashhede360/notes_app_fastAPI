FROM node:18 as build

WORKDIR 'notes-app\Front-end'

COPY package*.json ./
RUN npm install

COPY .  . 

RUN npm run build
RUN python -m http.server 5500

