FROM mhart/alpine-node
MAINTAINER DUONG Dinh Cuong <cuong3ihut@gmail.com>

COPY . /data
WORKDIR /data
RUN mkdir -p /usr/local/.node-red
VOLUME  /usr/local/.node-red

ENV DEVICE_ID= SECRET_KEY= SELF_ACTIVATION=NO INSTALL_DOCKER=NO

# bower requires this configuration parameter to allow bower install using root.
RUN echo '{ "allow_root": true }'>.bowerrc

# node-sass doesn't support Alpine, so we need the build toolchain.
RUN apk --update add curl git ca-certificates python build-base &&\	
    rm -rf /var/lib/apt/lists/* &&\
    rm -rf /var/cache/apk/* &&\
    rm -rf /data

EXPOSE 1880
ENTRYPOINT ["node"]
CMD ["/usr/bin/node-red"]

