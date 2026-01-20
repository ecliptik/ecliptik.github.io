# Small Web Protocols

This directory contains deployment infrastructure for serving the blog over alternative small web protocols.

## Protocols

### Gemini (`gemini/`)

Modern protocol for gemtext documents over TLS.

- **Server:** molly-brown (Go-based)
- **Port:** 1965
- **Production:** `gemini://sdf.org/ecliptik/`
- **Local Testing:** `gemini://jezebel:1965/` (Tailscale)
- **Content:** 30 posts, 63 tags, 8 year archives

**Quick Start:**
```bash
# Generate content
python3 _scripts/manage.py gemini

# Generate TLS certificates (first time only)
./smallweb/gemini/config/certs/generate-certs.sh

# Start server
docker compose -f smallweb/gemini/docker-compose.yml up -d

# Test
amfora gemini://jezebel:1965/

# Stop
docker compose -f smallweb/gemini/docker-compose.yml down
```

See `gemini/DEPLOY.md` for full deployment documentation.

### Gopher (`gopher/`)

Classic 1991 protocol for text and file distribution.

- **Server:** Python gopher server
- **Port:** 7070 (local), 70 (production)
- **Production:** `gopher://gopher.club:70/1/users/ecliptik/`
- **Local Testing:** `gopher://jezebel:7070/` (Tailscale)
- **Content:** 30 posts, 63 tags, 8 year archives

**Quick Start:**
```bash
# Generate content (local)
python3 _scripts/manage.py gopher

# Generate content (Tailscale)
python3 _scripts/manage.py gopher --host jezebel --port 7070

# Start server
docker compose -f smallweb/gopher/docker-compose.yml up -d

# Test
bombadillo gopher://jezebel:7070

# Stop
docker compose -f smallweb/gopher/docker-compose.yml down
```

See `gopher/DEPLOY.md` for full deployment documentation.

## Directory Structure

```
smallweb/
├── README.md (this file)
├── gemini/
│   ├── DEPLOY.md              # Deployment guide
│   ├── Dockerfile             # molly-brown server
│   ├── docker-compose.yml     # Docker stack
│   └── config/
│       ├── molly.conf         # Server configuration
│       ├── certs/             # TLS certificates (not committed)
│       │   ├── openssl.cnf    # Certificate config
│       │   ├── generate-certs.sh
│       │   └── README.md
│       └── logs/              # Server logs (not committed)
└── gopher/
    ├── DEPLOY.md              # Deployment guide
    ├── Dockerfile             # Python gopher server
    ├── docker-compose.yml     # Docker stack
    └── gopher_server.py       # RFC1436-compliant server
```

## Content Generation

Both protocols share the same content generation framework:

- **Core abstractions:** `_scripts/smallweb_core.py`
  - PostScanner, TagAggregator, YearOrganizer
  - SmallWebConverter abstract base class
- **Protocol-specific generators:**
  - Gopher: `_scripts/gopher_generator.py`
  - Gemini: `_scripts/gemini_generator.py`
- **Output directories:** `_gopher/`, `_gemini/` (auto-generated, not committed)

## Testing

All Docker stacks are configured for Tailscale hostname `jezebel` to allow testing from remote devices on the Tailscale network.

**From laptop or other device:**
```bash
# Gemini
amfora gemini://jezebel:1965/
lagrange gemini://jezebel.hale-gopher.ts.net:1965/

# Gopher
bombadillo gopher://jezebel:7070
echo "" | nc jezebel 7070
```

## Production Deployment

### Gemini → SDF.org

```bash
python3 _scripts/manage.py gemini --host sdf.org --port 1965 --base-url "gemini://sdf.org/ecliptik/"
bash tests/verify_gemini.sh
rsync -avz --delete _gemini/ username@sdf.org:gemini/
```

### Gopher → SDF.org/gopher.club

```bash
python3 _scripts/manage.py gopher --host gopher.club --port 70
bash tests/verify_gopher.sh
rsync -avz --delete _gopher/ username@sdf.org:gopher/
```

## Documentation

- **Main docs:** `CLAUDE.md` (AI assistant guide)
- **Scripts:** `_scripts/README.md`
- **Testing:** `tests/README.md`
- **Deployment:** `gemini/DEPLOY.md`, `gopher/DEPLOY.md`
