# Gopher Testing

## Quick Start

### Generate Gopher Content
```bash
python3 _scripts/manage.py gopher
```

### Verify Generation
```bash
bash tests/verify_gopher.sh
```

### Start Docker Test Stack
```bash
docker compose -f docker-compose.gopher.yml up -d
```

### Test with Curl
```bash
# Test root gophermap
curl gopher://localhost:70/

# Test blog index
curl gopher://localhost:70/1/blog

# Test a specific post
curl gopher://localhost:70/0/blog/2025/2025-01-28-A-Macintosh-Story.txt

# Test tags
curl gopher://localhost:70/1/tags

# Test a specific tag
curl gopher://localhost:70/1/tags/macintosh
```

### Test with Lynx Browser
```bash
lynx gopher://localhost:70
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

## Troubleshooting

### Port 70 Already in Use
```bash
# Find process using port 70
sudo lsof -i :70

# Or change port in docker-compose.gopher.yml
ports:
  - "7070:70"

# Then access with:
curl gopher://localhost:7070/
```

### Regenerate All Content
```bash
python3 _scripts/manage.py gopher --force
```

### View Gopher Server Logs
```bash
docker compose -f docker-compose.gopher.yml logs -f gopher
```
