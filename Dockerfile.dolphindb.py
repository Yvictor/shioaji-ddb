FROM centos:latest

ARG VER=64_V1.30.05

RUN yum install -y unzip curl bzip2

WORKDIR /opt/ddb
RUN curl -LO https://www.dolphindb.com/downloads/DolphinDB_Linux$VER.zip && \
    unzip DolphinDB_Linux$VER.zip && \
    curl -LO https://raw.githubusercontent.com/dolphindb/DolphinDBModules/master/ta/src/ta.dos && \
    mkdir /opt/ddb/server/modules && mv ta.dos /opt/ddb/server/modules/ta.dos && \
    chmod 755 /opt/ddb/server/dolphindb && \
    echo "" >> /opt/ddb/server/dolphindb.cfg && \
    echo "persistenceDir=dbcache" >> /opt/ddb/server/dolphindb.cfg && \
    echo "subPort=8808" >> /opt/ddb/server/dolphindb.cfg && \
    echo "maxPubConnections=128" >> /opt/ddb/server/dolphindb.cfg && \
    echo "perfMonitoring=1" >> /opt/ddb/server/dolphindb.cfg && \
    echo "newValuePartitionPolicy=add" >> /opt/ddb/server/dolphindb.cfg && \
    echo "maxPartitionNumPerQuery=1000000" >> /opt/ddb/server/dolphindb.cfg && \
    echo "globalDynamicLib=/usr/local/lib/libpython3.7m.so" >> /opt/ddb/server/dolphindb.cfg && \
    echo "./dolphindb -console 0" >> cmd && \
    chmod 755 cmd && \
    curl -sSL https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -o /tmp/miniconda.sh && \
    bash /tmp/miniconda.sh -bfp /usr/local/ && \
    rm -rf /tmp/miniconda.sh && \
    conda install -y python=3.7 && \
    conda clean --all --yes && \
    pip install dolphindb talib-binary==0.4.17 && \
    rpm -e --nodeps curl bzip2 && \
    yum clean all

WORKDIR /opt/ddb/server

CMD ["/bin/bash", "/opt/ddb/cmd"]