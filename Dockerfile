FROM ruby:2.7
LABEL maintainer="Micheal Waltz <ecliptik@gmail.com>"

#Listen on port 4000
EXPOSE 4000

#Set our workdir
WORKDIR /app

COPY Gemfile .
COPY Gemfile.lock .

#Install build packages
RUN apt-get update && apt-get install -y \
          build-essential \
          ca-certificates
RUN bundle install --system

#Run jekyll
ENTRYPOINT ["bundle"]
CMD ["exec", "jekyll", "serve", "--host=0.0.0.0"]
