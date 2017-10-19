FROM node:8

RUN npm -g config set user root

RUN npm install --quiet --no-progress -g http-server
RUN npm install --quiet --no-progress -g @angular/cli

RUN mkdir /app
COPY ./ /app

WORKDIR /app

RUN npm install --prod --quiet --no-progress
RUN npm uninstall --save-dev angular-cli
RUN npm install --save-dev @angular/cli@latest
RUN ng build --prod --aot
RUN mv ./dist /dist
RUN rm -rf /app
RUN npm cache clean --force

WORKDIR /dist

EXPOSE 4200

CMD ["http-server", "-p", "4200", "-a", "0.0.0.0"]