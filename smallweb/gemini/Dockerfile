FROM golang:1.21-alpine

# Install molly-brown using go install
RUN go install tildegit.org/solderpunk/molly-brown@latest

# Create gemini user and directories
RUN adduser -D -u 1000 gemini
RUN mkdir -p /var/gemini /gemini/certs /gemini/logs

# Set permissions (certs will be mounted from host)
RUN chown -R gemini:gemini /var/gemini /gemini

USER gemini
WORKDIR /var/gemini

EXPOSE 1965

CMD ["/go/bin/molly-brown", "-c", "/gemini/molly.conf"]
