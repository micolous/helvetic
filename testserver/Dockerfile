FROM alpine:3.8
RUN apk add --no-cache python2 py2-bottle py2-crcmod; addgroup helv; adduser -D -G helv helv
ADD testserver.py /opt/

USER helv
EXPOSE 8000/tcp
CMD ["/opt/testserver.py", "0.0.0.0", "8000"]
