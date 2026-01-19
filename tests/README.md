# Gopher Testing

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
docker compose -f docker-compose.gopher.yml up -d
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
docker compose -f docker-compose.gopher.yml down
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
docker compose -f docker-compose.gopher.yml logs -f gopher
```
