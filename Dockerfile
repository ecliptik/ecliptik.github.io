FROM public.ecr.aws/docker/library/ruby:3.2.2
LABEL maintainer="Micheal Waltz <dockerfile@ecliptik.com>"

#Set our workdir
WORKDIR /app

COPY Gemfile .
COPY Gemfile.lock .

#Install build packages
RUN apt-get update && apt-get install -y \
          build-essential \
          ca-certificates
RUN bundle config set system 'true'
RUN bundle install

#Run jekyll
ENTRYPOINT ["bundle"]
CMD ["exec", "jekyll", "serve", "--no-watch", "--host=0.0.0.0"]
