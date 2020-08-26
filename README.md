# ecliptik.github.io
Github Page

- Theme: [solar-theme-jekyll](https://github.com/mattvh/solar-theme-jekyll)
- Tags: [github-jekyll-tag](https://longqian.me/2017/02/09/github-jekyll-tag/)

## Running Jekyll Locally in a Docker Container

This repository contains a [Dockerfile](Dockerfile) to easily standup a Jekyll instance of this Github-pages site. This makes testing site updates locally within a stable Docker enviromnent before pushing to Github and without having to worry about installing all the necessary dependicies on your system.

Build a Jekyll container image with the necessary dependencies,

```
docker build -t jekyll .
```

Run a container using this repository as the document root. The volume mount must be read-write, otherwise Bundler and Jekyll will complain.

```
docker run -d -p 4000:4000 -v $(pwd):/app jekyll
```

Access the site at

> http://localhost:4000
