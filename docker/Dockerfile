FROM ubuntu:groovy
USER root
RUN rm -rf /usr/local/bin/mn /usr/local/bin/mnexec \
    /usr/local/lib/python*/*/*mininet* \
    /usr/local/bin/ovs-* /usr/local/sbin/ovs-* \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y \
       apt-utils \
       mininet \
       gcc \
    #    python \
       python3-minimal \
       python3-pip \
       iputils-ping \
       iproute2 \
       curl \
       net-tools \
       python3-setuptools \
       locales \
       libhdf5-dev \
       libhdf5-serial-dev \
    #    python3-h5py \
       python3-pandas \
       python3-matplotlib \
       vim \
       bc \
       psmisc \
    && apt install python3-pip \
    && python3 -m pip install --upgrade pip \
    && pip3 install Jupyter \
    && python3 -m pip install matplotlib \
    && python3 -m pip install tensorflow==2.4.2 \
    && python3 -m pip install keras-rl \
    && python3 -m pip install keras-rl2==1.0.4 \
    && pip3 install mininet \
    && update-rc.d openvswitch-switch defaults
WORKDIR /var/www
COPY www/* /var/www
# Set the locale
RUN sed -i -e 's/# en_US ISO-8859-1/en_US ISO-8859-1/' /etc/locale.gen && \
    locale-gen
ENV LANG en_US
ENV LANGUAGE en_US:en
ENV LC_ALL en_US
WORKDIR /notebooks
COPY notebooks/images/* /notebooks/images/
COPY notebooks/*.ipynb /notebooks/
WORKDIR /App
COPY . /App
WORKDIR /notebooks
CMD service openvswitch-switch start && jupyter notebook --ip 0.0.0.0 --allow-root
