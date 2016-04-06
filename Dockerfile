FROM alpine
MAINTAINER Micheal Waltz <ecliptik@gmail.com>

#Listen on port 4000
EXPOSE 4000

#Set APP_DIR
ENV APP_DIR /app

#Set our workdir
WORKDIR ${APP_DIR}

#Install runtime packages
RUN apk --no-cache add \
          ca-certificates \
          ruby \
          ruby-bundler \
          ruby-io-console \
          ruby-json \
          libffi \
          libxml2 \
          libxslt \
          zlib

# Copy Gemfile for gem install
RUN mkdir -p ${APP_DIR}
WORKDIR ${APP_DIR}
COPY Gemfile ${APP_DIR}

#Install build packages
RUN apk --no-cache add \
        --virtual build-dependencies \
          build-base \
          libffi-dev \
          libxml2-dev \
          libxslt-dev \
          ruby-dev && \
    bundle config build.nokogiri --use-system-libraries && \
    bundle package --all && \
    bundle install --local --system && \
    apk del build-dependencies

#Run jekyll
ENTRYPOINT ["bundle"]
CMD ["exec", "jekyll", "serve", "--host=0.0.0.0"]
