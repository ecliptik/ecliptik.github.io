FROM ruby:2.0
MAINTAINER Micheal Waltz <ecliptik@gmail.com>

#Listen on port 4000
EXPOSE 4000

#Set our workdir
WORKDIR /app

#Add Gemfile
ADD Gemfile /app/Gemfile

#Install Deps
RUN ["gem", "install", "bundler"]
RUN ["bundle", "install", "--standalone"]

#Run jekyll
CMD []
ENTRYPOINT ["bundler", "exec", "jekyll", "serve"]
