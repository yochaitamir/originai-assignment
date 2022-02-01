FROM node
WORKDIR  /
COPY package.json yarn.lock ./
COPY src ./src
COPY public ./public
RUN yarn install
RUN ["yarn", "build"]
CMD ["yarn","start"]