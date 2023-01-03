FROM bids/base_validator

ENV ANTSPATH="/opt/ants-2.3.4/" \
    PATH="/opt/ants-2.3.4:$PATH"

RUN apt-get update -qq \
    && apt-get install -y -q --no-install-recommends \
           ca-certificates \
           curl \
    && rm -rf /var/lib/apt/lists/* \
    && echo "Downloading ANTs ..." \
    && mkdir -p /opt/ants-2.3.4 \
    && curl -fsSL https://dl.dropbox.com/s/gwf51ykkk5bifyj/ants-Linux-centos6_x86_64-v2.3.4.tar.gz \
    | tar -xz -C /opt/ants-2.3.4 --strip-components 1


RUN apt-get update && \
    apt-get install -y python3 python3-pip wget unzip && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN wget https://ndownloader.figshare.com/files/3133832 -O oasis.zip && unzip oasis.zip -d /opt && rm -rf oasis.zip

RUN pip3 install pybids

COPY run.py /opt/run.py
RUN chmod a+x /opt/run.py

COPY version /opt/version

ENTRYPOINT ["/opt/run.py"]
