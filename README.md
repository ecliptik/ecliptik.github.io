# ecliptik.github.io

Personal tech blog hosted on GitHub Pages and deployed via Cloudflare Pages.

**Site:** https://www.ecliptik.com

- Theme: [solar-theme-jekyll](https://github.com/mattvh/solar-theme-jekyll)
- Tags: [github-jekyll-tag](https://longqian.me/2017/02/09/github-jekyll-tag/)

## Running Jekyll Locally with Docker

This repository includes Docker support for local development and testing before deploying to production.

### Quick Start

Start the Jekyll development server:

```bash
docker compose up -d
```

Access the site at:
- http://localhost:4000
- http://jezebel:4000 (or any hostname on your network)

View logs:

```bash
docker compose logs -f jekyll
```

Stop the server:

```bash
docker compose down
```

### Rebuilding After Changes

If you modify `Gemfile` or need a clean build:

```bash
docker compose down
docker compose build --no-cache
docker compose up -d
```

### Development Configuration

The Docker setup uses both `_config.yml` and `_config_dev.yml` to enable relative URL redirects, allowing access via any hostname (localhost, tailnet hosts, etc.).

For more details, see [CLAUDE.md](CLAUDE.md).
