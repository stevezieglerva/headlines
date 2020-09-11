FROM ubuntu

USER root 

# Install Python
RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

RUN apt-get install -y curl wget

# Install Hugo
RUN curl -L -o hugo.deb https://github.com/gohugoio/hugo/releases/download/v0.70.0/hugo_0.70.0_Linux-64bit.deb
RUN dpkg -i hugo.deb


# Install AWS CLI
RUN pip install awscli

# Copy directory files for Hugo site
COPY ./ ./
RUN ls -la headlines_site/

# Install python dependencies
RUN pip install -r requirements.txt

RUN chmod +x build.sh


CMD /build.sh
