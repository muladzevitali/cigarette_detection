FROM node:12.10.0

# set working directory
WORKDIR /usr/src/frontend

# install and cache app dependencies
COPY package.json .
RUN npm install --silent
RUN npm install react-scripts -g --silent
RUN npm install pm2 -g

ENV PATH /usr/src/frontend/node_modules/.bin:$PATH
COPY . .

RUN npm run-script build .env.production
CMD ["pm2", "serve", "build", "--name" , "cigarette_detection", "--port", "5091" ,"--no-daemon"]