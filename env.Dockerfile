FROM ubuntu:20.04

RUN apt-get -q update && \
    apt-get -q install -y \
    python3 python3-pip 

COPY . /home/ReGen
WORKDIR /home/ReGen

RUN pip3 install --upgrade pip && \
    pip3 install -r /home/ReGen/requirements.txt

CMD ["/bin/bash"]