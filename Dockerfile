FROM gliderlabs/alpine
COPY ./build/linux/powerstrip-slowreq /bin/powerstrip-slowreq
ENV PORT 80
ENV POWERSTRIP_ADAPTOR slowreq
EXPOSE 80
CMD ["/bin/powerstrip-slowreq"]
