# Gopher Deployment Guide

Quick reference for deploying gopher content to production.

## Local Testing (Default)

```bash
# 1. Generate for localhost:7070
python3 _scripts/manage.py gopher

# 2. Start Docker test server
docker compose -f docker-compose.gopher.yml up -d

# 3. Test with bombadillo
bombadillo gopher://localhost:7070

# 4. Test with netcat
echo "" | nc localhost 7070
echo "/blog" | nc localhost 7070

# 5. Stop server
docker compose -f docker-compose.gopher.yml down
```

## Tailscale Testing

Test from other devices on your Tailscale network:

```bash
# 1. Generate for Tailscale hostname
python3 _scripts/manage.py gopher --host jezebel --port 7070

# 2. Start Docker test server
docker compose -f docker-compose.gopher.yml up -d

# 3. Test from laptop or other Tailscale device
bombadillo gopher://jezebel:7070
echo "" | nc jezebel 7070

# 4. Stop server
docker compose -f docker-compose.gopher.yml down
```

Replace `jezebel` with your Tailscale hostname.

## Production Deployment to SDF.org

### Step 1: Generate for Production

```bash
# Generate with production host/port
python3 _scripts/manage.py gopher --host gopher.club --port 70

# Verify output uses gopher.club:70
head -20 _gopher/gophermap
# Should show: localhost → gopher.club, 7070 → 70
```

### Step 2: Upload to SDF

```bash
# Upload _gopher directory to SDF gopher directory
scp -r _gopher/* username@sdf.org:gopher/

# Or use rsync for incremental updates
rsync -avz --delete _gopher/ username@sdf.org:gopher/
```

### Step 3: Set Permissions

```bash
# SSH to SDF
ssh username@sdf.org

# Ensure gopher directory is readable
chmod -R a+rX ~/gopher/

# Verify structure
ls -la ~/gopher/
```

### Step 4: Test Production

```bash
# Test from local machine
echo "" | nc gopher.club 70

# Or with bombadillo
bombadillo gopher://gopher.club:70/1/users/ecliptik/

# Or with lynx
lynx gopher://gopher.club:70/1/users/ecliptik/
```

## Configuration Reference

### Default (Local Testing)
- **Host:** localhost
- **Port:** 7070
- **Base URL:** gopher://localhost:7070/
- **Command:** `python3 _scripts/manage.py gopher`

### Production (SDF.org)
- **Host:** gopher.club
- **Port:** 70
- **Base URL:** gopher://gopher.club:70/1/users/ecliptik/
- **Command:** `python3 _scripts/manage.py gopher --host gopher.club --port 70`

## Generated Content

- **30 posts** - Markdown posts (2015-2026) as 70-column plaintext
- **63 tags** - Tag pages with gophermaps
- **8 years** - Year archives (2011, 2015, 2017, 2021-2025)
- **2 pages** - about.txt, contact.txt

## Troubleshooting

### Wrong host/port in gophermaps
```bash
# Regenerate with correct flags
python3 _scripts/manage.py gopher --host gopher.club --port 70 --force

# Verify
grep "gopher.club" _gopher/gophermap
```

### Links point to localhost
```bash
# You forgot to use --host and --port flags
# Regenerate for production
python3 _scripts/manage.py gopher --host gopher.club --port 70
```

### SDF permissions issues
```bash
ssh username@sdf.org
chmod -R a+rX ~/gopher/
```

## Workflow Summary

```bash
# 1. Edit blog posts
vim _posts/2025/2025-01-28-Post.md

# 2. Generate for production
python3 _scripts/manage.py gopher --host gopher.club --port 70

# 3. Deploy to SDF
rsync -avz --delete _gopher/ username@sdf.org:gopher/

# 4. Test
echo "" | nc gopher.club 70
```

## Directory Structure

```
_gopher/
├── gophermap              # Root index
├── about.txt
├── contact.txt
├── blog/
│   ├── gophermap          # Blog index
│   ├── 2025/
│   │   ├── gophermap      # 2025 archive
│   │   └── *.txt          # Posts
│   └── 2024/
│       └── ...
└── tags/
    ├── gophermap          # Tag index
    ├── kubernetes/
    │   └── gophermap
    └── linux/
        └── gophermap
```

## See Also

- `_scripts/README.md` - Full documentation
- `tests/README.md` - Testing guide
- `CLAUDE.md` - AI assistant reference
