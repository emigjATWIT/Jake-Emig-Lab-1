FROM node:20-alpine
WORKDIR /app
COPY package.json package-lock.json* /app/
RUN npm install --silent --omit=dev
COPY index.js /app/
EXPOSE 4000
CMD ["node", "index.js"]