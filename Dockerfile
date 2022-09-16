# Docker file for ocr_tool ChRIS plugin app
#
# Build with
#
#   docker build -t <name> .
#
# For example if building a local version, you could do:
#
#   docker build -t local/pl-ocr_tool .
#
# In the case of a proxy (located at 192.168.13.14:3128), do:
#
#    docker build --build-arg http_proxy=http://192.168.13.14:3128 --build-arg UID=$UID -t local/pl-ocr_tool .
#
# To run an interactive shell inside this container, do:
#
#   docker run -ti --entrypoint /bin/bash local/pl-ocr_tool
#
# To pass an env var HOST_IP to container, do:
#
#   docker run -ti -e HOST_IP=$(ip route | grep -v docker | awk '{if(NF==11) print $9}') --entrypoint /bin/bash local/pl-ocr_tool
#

FROM python:3.9.1-slim-buster
LABEL maintainer="codificat <pep@redhat.com>"

WORKDIR /usr/local/src

RUN apt update && apt-get -y install tesseract-ocr
# install languages (separete layer to allow for updating without having to rebuild everything)

RUN apt-get -y install tesseract-ocr-nld tesseract-ocr-spa

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN mkdir test_txt
RUN pip install .

CMD ["ocr_tool", "--help"]
