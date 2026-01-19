# CLAUDE.md - AI Assistant Guide

Personal tech blog (20+ years): cloud, DevOps, retro computing, small web protocols.

**Site:** https://www.ecliptik.com | **Stack:** Jekyll 4.4.1, Ruby 3.4.4, Docker | **Deploy:** Cloudflare Pages

---

## Project Structure

```
_config.yml, _config_dev.yml   # Jekyll config (dev uses both for relative redirects)
_layouts/, _includes/          # HTML templates and components
_pages/, _pages/years/         # Site pages and year archives
_posts/YYYY/                   # Blog posts by year (*.md and *.html from 2004+)
_scripts/                      # tag_generator.py, updatesmallweb.sh
_gemini/, _gopher/             # Auto-generated (DO NOT MODIFY)
tag/                           # Auto-generated tag pages
assets/                        # css, js, images
```

---

## Critical Rules

**URLs:** `/blog/YYYY/post-title/` format. New posts in `_posts/YYYY/YYYY-MM-DD-Title.md`. Existing posts have `redirect_from:` for backward compatibility.

**Tags (VERY IMPORTANT):**
- ALWAYS check `_scripts/README.md` first
- Lowercase only (`kubernetes` not `Kubernetes`)
- Use canonical names: `macos`, `512ke`, `networking`, `terminal`, `smolweb`
- After changes: `python3 _scripts/tag_generator.py` (from repo root)
- Should have ~78 tags total

**Never Modify:**
- `_posts/*.html` (2004-2011 historical HTML)
- `_gemini/`, `_gopher/` (auto-generated)
- CNAME (Cloudflare handles DNS)

**CSS Reference:**
- Development: `_layouts/default.html` uses `console.css` (unminified)
- Production: Switch to `console.min.css` before deployment

---

## Development

**Docker (Recommended):**
```bash
docker compose up -d              # Start (localhost:4000)
docker compose logs -f jekyll     # View logs
docker compose down               # Stop
docker compose build --no-cache   # Rebuild after Gemfile changes
```

**Manual:** `bundle install && bundle exec jekyll serve --watch`

**CSS Workflow:** Edit `assets/css/console.css` then minify:
```bash
python3 << 'EOF'
import re
with open('assets/css/console.css', 'r') as f:
    css = f.read()
css = re.sub(r'/\*.*?\*/', '', css, flags=re.DOTALL)
css = re.sub(r'\s+', ' ', css)
css = re.sub(r'\s*{\s*', '{', css)
css = re.sub(r'\s*}\s*', '}', css)
css = re.sub(r'\s*:\s*', ':', css)
css = re.sub(r'\s*;\s*', ';', css)
css = re.sub(r'\s*,\s*', ',', css)
css = re.sub(r';\s*}', '}', css)
css = re.sub(r'}', '}\n', css)
with open('assets/css/console.min.css', 'w') as f:
    f.write(css.strip())
EOF
```

---

## Common Tasks

**New Post:** `_scripts/newpost.sh "Post Title"`

**Frontmatter Template:**
```yaml
---
layout: post
title: Your Post Title
description: Brief description for SEO and social media
category: linux
tags: linux kubernetes docker terminal  # Use canonical tags!
---
```

**Modify Tags:** Edit frontmatter → verify canonical tags → `python3 _scripts/tag_generator.py` → commit

**Images:** Place in `assets/images/posts/` or `assets/images/{category}/`

**Update Small Web:** `_scripts/updatesmallweb.sh -t all`

---

## Git Workflow

Branches: `feature/`, `cleanup/`, `fix/` → `main`

**NEVER `git push` OR `git merge`** - User handles all pushes and merges

**No GPG signing:** Use `git commit --no-gpg-sign` or `git commit -m`

**Commit Format:**
```
Category: Brief description

- Change 1
- Change 2

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

---

## Rules & Best Practices

**DON'T:**
- Use `git push` or `git merge` (user handles all pushes and merges)
- Convert HTML posts to Markdown
- Modify auto-generated files
- Create duplicate/variant tags
- Add GitHub Actions
- Load search.json on page load
- Run tag_generator.py from _scripts/ directory

**DO:**
- Read `_scripts/README.md` before tag work
- Test locally with Docker before commits
- Use canonical lowercase tags
- Edit console.css (unminified) during development
- Minify and switch to console.min.css before production deployment
- Ask user about structural changes, new dependencies, major theme changes

---

## Recent Improvements (2026-01)

**URL Structure:** Year-based directories (`_posts/YYYY/`), permalinks changed to `/blog/:year/:title/`, 67 posts with redirect_from

**Performance:** Removed animate.css (57KB), lazy-loaded search (~114KB), minified CSS, font-display: swap. **Result:** ~60KB reduction, 30-40% faster load

**SEO & Social Media:**
- All posts have meta descriptions and BlogPosting schema
- Tag pages indexed (removed noindex, added descriptions)
- Open Graph + Twitter Cards with auto image extraction
- Year archive pages with clickable breadcrumb navigation (`~/blog/2025/post-slug`)

**Theme Updates (WIP - feature/accent-light-links branch):**
- Link styling: Body/content links use `--accent-light` (purple), header/footer use `--accent` (blue)
- All links bold in body/content for better visibility
- Hover: Inverse colors (bg/text swap), no underlines throughout
- Header/footer text: Bold for improved hierarchy
- Terminal cursor: Wider (12px) and taller (1.2em) animation
- Theme toggle: No background shade on hover

---

## Troubleshooting

**Build issues:** `docker compose logs jekyll` then rebuild: `docker compose down && docker compose build --no-cache && docker compose up -d`

**Missing tags:** `python3 _scripts/tag_generator.py` (should generate ~78)

**Dev redirects broken:** Ensure `_config_dev.yml` exists

---

## Quick Reference

**Commands:**
```bash
docker compose up -d                    # Start dev
python3 _scripts/tag_generator.py       # Regenerate tags
_scripts/updatesmallweb.sh -t all       # Update Gemini/Gopher
```

**Key Files:** `_scripts/README.md` (tags), `_config.yml` (Jekyll), `_config_dev.yml` (dev overrides)

**Ask User About:** Structural changes, new dependencies, major theme mods, deployment config
