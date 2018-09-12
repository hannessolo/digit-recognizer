FROM ubuntu

WORKDIR /usr/src/app

RUN apt-get update -y && apt-get install curl sudo -y
RUN apt-get install gnupg gnupg2 gnupg1 -y

# install node
RUN curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -
RUN sudo apt-get install -y nodejs

COPY package*.json ./
RUN npm install

# install tensorflow
RUN sudo apt-get install python3-pip python3-dev python-virtualenv -y && pip3 install --upgrade pip
RUN cd ~ && virtualenv --system-site-packages -p python3 venv
RUN cd ~ && pip3 install --upgrade tensorflow
RUN cd /usr/src/app

COPY . .

EXPOSE 8080
CMD ["/bin/bash", "-c", "source ~/venv/bin/activate && npm start"]