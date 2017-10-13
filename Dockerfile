FROM neurodebian:zesty-non-free

RUN apt-get update && \
    apt-get install -y ants=2.2.0-1~nd17.04+1 python3 python3-pip wget unzip && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
ENV ANTSPATH=/usr/lib/ants/
ENV PATH=$ANTSPATH:$PATH

## Install the validator
RUN apt-get update && \
    apt-get install -y curl && \
    curl -sL https://deb.nodesource.com/setup_8.x | bash - && \
    apt-get remove -y curl && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
	
RUN wget https://ndownloader.figshare.com/files/3133832 -O oasis.zip && unzip oasis.zip -d /opt && rm -rf oasis.zip

RUN pip3 install https://github.com/INCF/pybids/archive/800d15053952991c9cd4a00cf0039288d489ca12.zip

RUN npm install -g bids-validator

COPY run.py /opt/run.py

COPY version /opt/version

ENTRYPOINT ["/opt/run.py"]