FROM ruby:2.4.1-alpine
LABEL maintainer="Micheal Waltz <ecliptik@gmail.com>"

#Listen on port 4000
EXPOSE 4000

#Set our workdir
WORKDIR /app

COPY Gemfile .
COPY Gemfile.lock .

#Install build packages
RUN apk --no-cache add \
        --virtual build-dependencies \
          build-base \
          libffi-dev \
          libxml2-dev \
          libxslt-dev \
          ruby-dev && \
    apk --no-cache add \
          ca-certificates \
          libffi \
          libxml2 \
          libxslt \
          zlib && \
    bundle install --system && \
    apk del build-dependencies

#Run jekyll
ENTRYPOINT ["bundle"]
CMD ["exec", "jekyll", "serve", "--host=0.0.0.0"]
