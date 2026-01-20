# Small Web Protocol Testing

Testing guides for Gopher and Gemini capsule generation and deployment.

## Gopher Testing

## Quick Start

### Generate Gopher Content for Testing
```bash
# Default generates for localhost:7070 (Docker testing)
python3 _scripts/manage.py gopher
```

### Generate for Production Deployment
```bash
# For SDF.org gopher.club
python3 _scripts/manage.py gopher --host gopher.club --port 70
```

### Verify Generation
```bash
bash tests/verify_gopher.sh
```

### Start Docker Test Stack
```bash
docker compose -f smallweb/gopher/docker-compose.yml up -d
```

### Test with Netcat
```bash
# Test root gophermap
echo "" | nc localhost 7070

# Test blog index
echo "/blog" | nc localhost 7070

# Test a specific post
echo "/blog/2025/2025-01-28-A-Macintosh-Story.txt" | nc localhost 7070

# Test tags
echo "/tags" | nc localhost 7070

# Test a specific tag
echo "/tags/macintosh" | nc localhost 7070
```

### Test with Curl (if curl supports gopher)
```bash
# Note: curl gopher support varies by platform
curl gopher://localhost:7070/
```

### Test with Lynx Browser
```bash
lynx gopher://localhost:7070
```

### Stop Docker Stack
```bash
docker compose -f smallweb/gopher/docker-compose.yml down
```

## Expected Results

- **30 posts**: All markdown posts from 2015-2026
- **63 tags**: Tag pages for all tags in markdown posts
- **8 year archives**: Years 2011, 2015, 2017, 2021, 2022, 2023, 2024, 2025
- **2 static pages**: about.txt, contact.txt
- **RFC1436-compliant gophermaps**: Proper type codes and formatting

## Gophermap Type Codes

- `0` = Text file
- `1` = Directory/menu
- `i` = Information line (non-selectable)
- `h` = HTML link (URL: prefix)
- `g` = GIF image
- `I` = Generic image (PNG, JPG)

## Server Details

The Docker test stack uses a custom Python gopher server (RFC1436-compliant):
- **Port**: 7070 (non-privileged port, easier for testing)
- **Image**: python:3.11-slim with custom gopher_server.py
- **Features**: Directory listings, gophermap parsing, text file serving

### Why Port 7070?
Port 70 is the standard gopher port but requires root privileges. The test server uses port 7070 to:
- Avoid needing root/sudo
- Work in non-privileged Docker containers
- Prevent conflicts with system gopher servers

## Troubleshooting

### Port 7070 Already in Use
```bash
# Find process using port 7070
sudo lsof -i :7070

# Or change port in docker-compose.gopher.yml
ports:
  - "8070:7070"

# Then access with:
echo "" | nc localhost 8070
```

### Regenerate All Content
```bash
python3 _scripts/manage.py gopher --force
```

### View Gopher Server Logs
```bash
docker compose -f smallweb/gopher/docker-compose.yml logs -f gopher
```

---

## Gemini Testing

### Quick Start

#### Generate Gemini Content for Testing
```bash
# Default generates for localhost:1965 (Docker testing)
python3 _scripts/manage.py gemini
```

#### Generate for Production Deployment
```bash
# For SDF.org
python3 _scripts/manage.py gemini --host sdf.org --port 1965 --base-url "gemini://sdf.org/ecliptik/"
```

#### Verify Generation
```bash
bash tests/verify_gemini.sh
```

#### Start Docker Test Stack
```bash
docker compose -f smallweb/gemini/docker-compose.yml up -d
```

#### Test with Gemini Clients

**Using openssl (basic test):**
```bash
echo "" | openssl s_client -connect localhost:1965 -quiet
```

**Using bombadillo (terminal client):**
```bash
bombadillo gemini://localhost:1965/
```

**Using amfora (terminal client):**
```bash
amfora gemini://localhost:1965/
```

**Using lagrange (GUI client):**
```bash
lagrange gemini://localhost:1965/
```

**Test specific pages:**
```bash
# Test root
amfora gemini://localhost:1965/

# Test blog index
amfora gemini://localhost:1965/blog/

# Test year archive
amfora gemini://localhost:1965/blog/2025/

# Test specific post
amfora gemini://localhost:1965/blog/2025/Switching-to-Ghostty.gmi

# Test tags
amfora gemini://localhost:1965/tags/

# Test specific tag
amfora gemini://localhost:1965/tags/kubernetes.gmi

# Test static pages
amfora gemini://localhost:1965/about.gmi
amfora gemini://localhost:1965/contact.gmi
```

#### Stop Docker Stack
```bash
docker compose -f smallweb/gemini/docker-compose.yml down
```

### Expected Results

- **30 posts**: All markdown posts from 2015-2026
- **63 tags**: Tag pages for all tags in markdown posts
- **8 year archives**: Years 2011, 2015, 2017, 2021, 2022, 2023, 2024, 2025
- **2 static pages**: about.gmi, contact.gmi
- **Valid gemtext format**: Links, headings, lists, code blocks

### Gemtext Syntax

- **Links:** `=> URL optional text`
- **Headings:** `#` (h1), `##` (h2), `###` (h3)
- **Lists:** `* Item text`
- **Quotes:** `> Quote text`
- **Preformatted:** ` ``` alt text ... ``` `
- **Text:** Plain lines (no markup)

### Server Details

The Docker test stack uses molly-brown gemini server:
- **Port**: 1965 (standard gemini port)
- **Image**: Built from golang:1.21-alpine with molly-brown
- **TLS**: Self-signed certificate (auto-generated in Dockerfile)
- **Features**: Gemtext serving, directory listings, RFC-compliant

### Gemini Clients

**Terminal Clients:**
- **amfora** - Feature-rich, user-friendly
- **bombadillo** - Multi-protocol browser (gopher, gemini, finger)
- **av-98** - Python-based, minimal

**GUI Clients:**
- **lagrange** - Modern, polished interface
- **kristall** - Qt-based
- **geminaut** - Windows-focused

**Installation (examples):**
```bash
# Debian/Ubuntu
sudo apt install amfora

# MacOS
brew install amfora lagrange

# Build from source (amfora)
go install github.com/makeworld-the-better-one/amfora@latest
```

### Troubleshooting

#### Certificate Warnings
The Docker test server uses a self-signed certificate. Gemini clients will warn you about this - it's safe to accept for local testing.

#### Port 1965 Already in Use
```bash
# Find process using port 1965
sudo lsof -i :1965

# Or change port in docker-compose.gemini.yml
ports:
  - "11965:1965"

# Then access with:
amfora gemini://localhost:11965/
```

#### Regenerate All Content
```bash
python3 _scripts/manage.py gemini --force
```

#### View Gemini Server Logs
```bash
docker compose -f smallweb/gemini/docker-compose.yml logs -f gemini
```

#### Verification Warnings
The verification script may show warnings about:
- **Markdown link syntax** - Likely from table formatting in about.gmi (acceptable)
- **HTML tags** - Likely from table formatting (acceptable)
- **Extra year directories** - Jekyll year directories not part of gemini content (acceptable)

These warnings don't affect functionality.

### Comparison: Gopher vs Gemini

| Aspect | Gopher | Gemini |
|--------|--------|--------|
| Protocol | RFC1436 | Gemini Protocol |
| Format | Plaintext + Gophermaps | Gemtext (.gmi) |
| Links | Tab-separated selectors | `=> url text` |
| Headers | N/A (plaintext) | `#` `##` `###` |
| Lists | N/A (plaintext) | `* item` |
| Line wrapping | 70 columns (Pandoc) | None (client-side) |
| Images | Text references + URLs | `=> image.jpg alt` |
| Conversion tool | Pandoc → plaintext | Custom parser → gemtext |
| Port | 70 (prod), 7070 (test) | 1965 (standard) |
| Extension | .txt | .gmi |
| Index files | gophermap | index.gmi |
| Test server | Python gopher server | molly-brown (Go) |
| TLS | No | Yes (required) |

### See Also

- `GEMINI_DEPLOY.md` - Full deployment guide
- `_scripts/README.md` - manage.py documentation
- `_scripts/gemini_generator.py` - Implementation details
- `GOPHER_DEPLOY.md` - Gopher deployment guide
