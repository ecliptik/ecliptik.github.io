# Gemini Capsule Deployment Guide

Quick reference for generating and deploying Gemini capsule content to SDF.org.

## Prerequisites

- Python 3.x
- SDF.org account with gemini service access
- SSH key configured for SDF.org

## Local Testing

### 1. Generate Gemini Content (Local)

```bash
# Generate for local testing (localhost:1965)
python3 _scripts/manage.py gemini

# Force regeneration
python3 _scripts/manage.py gemini --force
```

### 2. Verify Generation

```bash
# Run verification script
bash tests/verify_gemini.sh

# Expected output:
# - 30 posts
# - 63 tag pages
# - 8 year archives (2011, 2015, 2017, 2021-2025)
# - All gemtext syntax checks pass
```

### 3. Generate TLS Certificates (First Time Only)

```bash
# Generate self-signed certificates for local testing
./.docker/gemini/certs/generate-certs.sh

# Or manually:
cd .docker/gemini/certs
openssl req -x509 -newkey rsa:2048 \
    -keyout key.pem \
    -out cert.pem \
    -days 365 \
    -nodes \
    -config openssl.cnf \
    -extensions v3_req
```

**Note:** Certificates are not committed to git for security. You only need to generate them once (valid for 365 days).

### 4. Test with Docker

```bash
# Start molly-brown server
docker compose -f docker-compose.gemini.yml up -d

# View logs
docker compose -f docker-compose.gemini.yml logs -f

# Test with gemini client (choose one):
# - Using a command-line client
echo "" | openssl s_client -connect localhost:1965 -quiet

# - Using bombadillo
bombadillo gemini://localhost:1965/

# - Using amfora
amfora gemini://localhost:1965/

# - Using lagrange (GUI)
lagrange gemini://localhost:1965/

# Stop server
docker compose -f docker-compose.gemini.yml down
```

## Tailscale Testing

The Docker container is configured with hostname `jezebel` for testing from other Tailscale devices.

```bash
# Container is already configured for jezebel hostname
# No need to regenerate gemini content

# Start Docker test server
docker compose -f docker-compose.gemini.yml up -d

# Test from laptop or other Tailscale device
# Using bombadillo
bombadillo gemini://jezebel:1965/

# Using amfora
amfora gemini://jezebel:1965/

# Using lagrange (GUI)
lagrange gemini://jezebel:1965/

# Using openssl
echo "" | openssl s_client -connect jezebel:1965 -servername jezebel -quiet

# Stop server
docker compose -f docker-compose.gemini.yml down
```

**Note:** The TLS certificates include `jezebel` and `jezebel.hale-gopher.ts.net` in the Subject Alternative Names, so they will validate correctly when accessed via Tailscale hostname.

## Production Deployment (SDF.org)

### 1. Generate for Production

```bash
# Generate with SDF.org configuration
python3 _scripts/manage.py gemini \
  --host sdf.org \
  --port 1965 \
  --base-url "gemini://sdf.org/ecliptik/"

# Verify before upload
bash tests/verify_gemini.sh
```

### 2. Upload to SDF.org

```bash
# Upload via rsync (recommended)
rsync -avz --delete _gemini/ username@sdf.org:gemini/

# OR upload via scp
scp -r _gemini/* username@sdf.org:gemini/
```

### 3. Set Permissions

```bash
# SSH to SDF
ssh username@sdf.org

# Set proper permissions
chmod -R a+rX ~/gemini/

# Verify files
ls -la ~/gemini/
```

### 4. Test Production

```bash
# Test from your local machine
amfora gemini://sdf.org/ecliptik/

# Or use a browser extension/GUI client
```

## Gemini Capsule Structure

```
_gemini/
├── index.gmi                 # Root page with ASCII art & navigation
├── about.gmi                 # About page
├── contact.gmi               # Contact page
├── blog/
│   ├── index.gmi             # Year list
│   ├── 2025/
│   │   ├── index.gmi         # 2025 posts list
│   │   ├── Post-Title-1.gmi
│   │   └── Post-Title-2.gmi
│   ├── 2024/
│   │   └── index.gmi
│   └── ...
└── tags/
    ├── index.gmi             # Tag list
    ├── linux.gmi             # Tag page
    ├── kubernetes.gmi
    └── ...
```

## URL Patterns

- **Root:** `gemini://sdf.org/ecliptik/`
- **About:** `gemini://sdf.org/ecliptik/about.gmi`
- **Blog Index:** `gemini://sdf.org/ecliptik/blog/`
- **Year Archive:** `gemini://sdf.org/ecliptik/blog/2025/`
- **Post:** `gemini://sdf.org/ecliptik/blog/2025/Post-Title.gmi`
- **Tags Index:** `gemini://sdf.org/ecliptik/tags/`
- **Tag Page:** `gemini://sdf.org/ecliptik/tags/linux.gmi`

## Gemtext Format Notes

- **Links:** `=> URL optional text`
- **Headings:** `#` (h1), `##` (h2), `###` (h3)
- **Lists:** `* Item text`
- **Quotes:** `> Quote text`
- **Code:** ` ``` language ... ``` `
- **NO line wrapping** - gemini clients handle wrapping

## Key Differences from Gopher

| Aspect | Gopher | Gemini |
|--------|--------|--------|
| Protocol | RFC1436 | Gemini Protocol |
| Format | Plaintext + Gophermaps | Gemtext (.gmi) |
| Links | Tab-separated selectors | `=> url text` |
| Headers | N/A (plaintext) | `#` `##` `###` |
| Line wrapping | 70 columns (Pandoc) | None (client-side) |
| Port | 70 (prod), 7070 (test) | 1965 (standard) |
| Extension | .txt | .gmi |
| Index files | gophermap | index.gmi |
| Test server | Python gopher server | molly-brown (Go) |

## Common Commands

```bash
# Quick workflow
python3 _scripts/manage.py gemini
bash tests/verify_gemini.sh
rsync -avz --delete _gemini/ username@sdf.org:gemini/

# With Docker testing
python3 _scripts/manage.py gemini
docker compose -f docker-compose.gemini.yml up -d
amfora gemini://localhost:1965/
docker compose -f docker-compose.gemini.yml down

# Production deployment
python3 _scripts/manage.py gemini \
  --host sdf.org \
  --base-url "gemini://sdf.org/ecliptik/"
bash tests/verify_gemini.sh
rsync -avz --delete _gemini/ username@sdf.org:gemini/
```

## Troubleshooting

### No content generated

```bash
# Check for errors
python3 _scripts/manage.py gemini 2>&1 | less

# Force regeneration
python3 _scripts/manage.py gemini --force
```

### Docker container won't start

```bash
# Check logs
docker compose -f docker-compose.gemini.yml logs

# Rebuild
docker compose -f docker-compose.gemini.yml down
docker compose -f docker-compose.gemini.yml build --no-cache
docker compose -f docker-compose.gemini.yml up -d
```

### Permissions errors on SDF.org

```bash
# SSH and fix
ssh username@sdf.org
chmod -R a+rX ~/gemini/
find ~/gemini -type d -exec chmod 755 {} \;
find ~/gemini -type f -exec chmod 644 {} \;
```

### Markdown artifacts in gemtext

```bash
# Check verification warnings
bash tests/verify_gemini.sh

# Review specific file
less _gemini/blog/2025/Post-Title.gmi
```

## Reference Links

- **Gemini Protocol:** [gemini.circumlunar.space](gemini://gemini.circumlunar.space/)
- **SDF.org Gemini:** [sdf.org/gemini](https://sdf.org/?tutorials/gemini)
- **Gemini Clients:** [Are we gemini yet?](https://portal.mozz.us/gemini/gemini.circumlunar.space/clients.gmi)
- **Molly-brown Server:** [tildegit.org/solderpunk/molly-brown](https://tildegit.org/solderpunk/molly-brown)

## See Also

- `_scripts/README.md` - Full manage.py documentation
- `tests/README.md` - Testing documentation
- `GOPHER_DEPLOY.md` - Gopher deployment guide
- `CLAUDE.md` - AI assistant project guide
