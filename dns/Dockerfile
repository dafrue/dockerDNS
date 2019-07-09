# Use an official Python runtime as a parent image
FROM alpine:3.4

RUN apk add --no-cache bind bind-tools tcpdump

ADD bind9 /etc/default/
ADD named.conf /etc/bind/
ADD named.conf.root /etc/bind/

RUN mkdir /etc/bind/zones
RUN mkdir /var/cache/bind
RUN mkdir /logs

WORKDIR /logs

EXPOSE 53

CMD named -4 -c /etc/bind/named.conf -f & tcpdump -i eth0 -n -w $NSLOGNAME port 53
