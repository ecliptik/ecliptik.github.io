# Blog Management Scripts

This directory contains tools for managing the Jekyll blog at [ecliptik.com](https://www.ecliptik.com), including post creation, tag generation, year archives, and small web protocols (gopher/gemini).

## Unified Management Tool: manage.py

The primary tool for all blog management tasks. A consolidated Python CLI that replaces multiple scattered bash scripts.

**Always run from repository root:**

```bash
python3 _scripts/manage.py [command] [options]
```

### Commands

#### Create New Post

Create a new blog post with complete frontmatter including description and redirect_from fields.

**Interactive mode (recommended for first use):**
```bash
python3 _scripts/manage.py post
```

You'll be prompted for:
- Title (required)
- Category (e.g., linux, devops, macos, retro, smolweb)
- Description (1-2 sentences for SEO and social media)
- Tags (space-separated, lowercase)

**CLI mode (faster for experienced users):**
```bash
python3 _scripts/manage.py post -t "My Post Title" -c linux -d "Brief description" --tags linux docker kubernetes
```

**What it does:**
- Creates post in `_posts/YYYY/YYYY-MM-DD-Title.md`
- Generates complete frontmatter with all required fields
- Validates tags against existing tags (warns on new tags)
- Creates `redirect_from` field for backward compatibility

#### Generate Tags

Scan all posts and generate tag pages in `tag/` directory.

```bash
python3 _scripts/manage.py tags
```

**What it does:**
1. Recursively scans `_posts/**/*.md` and `_posts/**/*.html`
2. Extracts tags from frontmatter
3. Removes old tag files
4. Generates new tag pages with descriptions
5. Reports count and warns about non-canonical tags

**Expected output:** ~78 tags (as of 2026-01)

#### Generate Year Archives

Create year archive pages for all years with posts.

```bash
python3 _scripts/manage.py years
```

**What it does:**
1. Scans `_posts/` for year subdirectories (e.g., 2024, 2025, 2026)
2. Creates missing year archive pages in `_pages/years/`
3. Generates pages with permalink `/blog/YYYY/`

#### Update Everything

Run both tags and years generation in one command.

```bash
python3 _scripts/manage.py all
```

**Use this after:**
- Creating new posts
- Modifying post tags
- Moving posts to new years

#### Minify Assets

Minify CSS and JavaScript files to reduce page load size.

```bash
python3 _scripts/manage.py minify
```

**What it does:**
1. Minifies `assets/css/console.css` → `assets/css/console.min.css`
2. Minifies JavaScript files:
   - `assets/js/theme-toggle.js` → `assets/js/theme-toggle.min.js`
   - `assets/js/search-init.js` → `assets/js/search-init.min.js`
   - `assets/js/image-captions.js` → `assets/js/image-captions.min.js`
   - `assets/js/tooltip.js` → `assets/js/tooltip.min.js`
3. Reports file size reductions (typically ~30-40%)

**Note:** Layouts already reference minified files. Run this command after editing source CSS/JS files.

**Typical savings:** ~12KB reduction (from ~41KB to ~29KB)

#### Generate Gopher Content

Generate RFC1436-compliant gopher content from Jekyll blog posts.

**Local Testing (default):**
```bash
# Generate for localhost:7070 (Docker testing)
python3 _scripts/manage.py gopher
```

**Production Deployment:**
```bash
# Generate for SDF.org gopher.club
python3 _scripts/manage.py gopher --host gopher.club --port 70

# Or with base URL
python3 _scripts/manage.py gopher \
  --host gopher.club \
  --port 70 \
  --base-url "gopher://gopher.club:70/1/users/ecliptik/"
```

**What it does:**
1. Converts markdown posts to plaintext (70 columns) using Pandoc
2. Generates gophermaps for navigation (root, blog, tags, years)
3. Creates year archives and tag pages
4. Converts static pages (about, contact)
5. Adds image references with URLs
6. Configures host/port in all gophermap links

**Output:** `_gopher/` directory with:
- 30 plaintext posts in `blog/YYYY/*.txt`
- 63 tag pages with gophermaps
- 8 year archive pages
- Root gophermap with site navigation

**Options:**
```bash
python3 _scripts/manage.py gopher --force              # Regenerate all
python3 _scripts/manage.py gopher --columns 80         # Custom width
python3 _scripts/manage.py gopher --host example.com   # Custom host
python3 _scripts/manage.py gopher --port 7070          # Custom port
```

**Local Testing:**
```bash
# Generate for localhost (default)
python3 _scripts/manage.py gopher

# Verify generation
bash tests/verify_gopher.sh

# Start Docker test server
docker compose -f smallweb/gopher/docker-compose.yml up -d

# Test with netcat
echo "" | nc localhost 7070

# Test with bombadillo
bombadillo gopher://localhost:7070

# Stop server
docker compose -f smallweb/gopher/docker-compose.yml down
```

**Deploy to SDF.org:**
```bash
# 1. Generate for production
python3 _scripts/manage.py gopher --host gopher.club --port 70

# 2. Upload to SDF
scp -r _gopher/* username@sdf.org:gopher/

# 3. Test production
echo "" | nc gopher.club 70
```

See `tests/README.md` for detailed testing documentation.

#### Generate Gemini Content (Coming Soon)

```bash
python3 _scripts/manage.py gemini  # Planned
```

Will use shared abstractions from gopher generator for Gemini capsule generation.

### Help

View help for any command:

```bash
python3 _scripts/manage.py --help
python3 _scripts/manage.py post --help
```

### Tag Naming Conventions

To maintain consistency and prevent tag sprawl, follow these guidelines:

#### General Rules

1. **Lowercase only** - Use `kubernetes` not `Kubernetes`
2. **Descriptive** - Tags should be clear and meaningful
3. **No duplicates** - Check existing tags before creating new ones
4. **Singular form** - Use `container` not `containers` (exceptions: `macos`, `kubernetes`)
5. **Hyphenated compound words** - Use `cloud-native` not `cloudnative`

#### When to Create New Tags vs. Use Existing

**Create a new tag when:**
- The topic is genuinely distinct from existing tags
- Multiple posts will use this tag
- It represents a significant technology or concept

**Use existing tags when:**
- A similar tag already exists (e.g., use `macos` instead of creating `mac` or `osx`)
- The topic is a minor variation of an existing tag
- You're unsure - check the canonical tag list below first

#### Canonical Tags

These are the primary tags for common topics. Always use these instead of variations:

**Operating Systems:**
- `macos` - Modern macOS systems (not: `mac`, `osx`)
- `linux` - Linux operating systems
- `windows` - Windows operating systems

**Classic Computing:**
- `macintosh` - Vintage Macintosh computers (general)
- `512ke` - Macintosh 512Ke specifically (not: `512k`)
- `macplus` - Macintosh Plus

**Containers & Orchestration:**
- `docker` - Docker containers
- `kubernetes` - Kubernetes orchestration
- `containers` - General containerization

**Cloud Providers:**
- `aws` - Amazon Web Services
- `gcp` - Google Cloud Platform
- `azure` - Microsoft Azure

**DevOps & Tools:**
- `devops` - DevOps practices
- `ci-cd` - Continuous Integration/Deployment
- `git` - Version control

**Shell & Terminal:**
- `terminal` - Terminal emulators and usage (not: `shell`)
- `bash` - Bash shell specifically
- `zsh` - Zsh shell specifically

**Networking:**
- `networking` - Network-related topics (not: `network`)

**Web:**
- `smolweb` - Small/indie web (not: `smallweb`)
- `gemini` - Gemini protocol
- `gopher` - Gopher protocol

### After Making Tag Changes

Whenever you modify tags in post frontmatter:

1. **Update the post** - Edit the `tags:` line in the post's YAML frontmatter
2. **Regenerate tags** - Run `python3 _scripts/tag_generator.py` from repository root
3. **Verify** - Check that old tag files are removed and new ones are created
4. **Commit** - Include both the post changes and regenerated tag files in your commit

### Tag Consolidation History

#### 2026-01 - Initial Consolidation
- `mac`, `osx` → `macos`
- `512k` → `512ke`
- `network` → `networking`
- `shell` → `terminal`
- `smallweb` → `smolweb`
- **Result:** Reduced from 86 to 78 tags

### Checking for Tag Sprawl

To find potential duplicate tags:

```bash
# List all tags
ls tag/*.md | sed 's/tag\///' | sed 's/\.md//' | sort

# Search for specific patterns
grep -r "tags:" _posts/ | grep -i "macos\|mac\|osx"
```

### Best Practices

1. **Review existing tags first** - Use `ls tag/` to see what's already there
2. **Be conservative** - Fewer, well-chosen tags are better than many overlapping ones
3. **Document decisions** - Update this README when establishing new canonical tags
4. **Regular cleanup** - Periodically review tags for consolidation opportunities

## Deprecated Scripts

Old bash scripts have been moved to `_scripts/deprecated/` and replaced by `manage.py`.

**Do not use these scripts for new work:**

- `newpost.sh` → Use `python3 _scripts/manage.py post`
- `tag_generator.py` → Use `python3 _scripts/manage.py tags`
- `updatesmallweb.sh` → Continue using until `manage.py gopher/gemini` are ready
- `markdown2sw.sh` → Will be replaced by future `manage.py gopher/gemini`
- `md2gophermap.sh` → Will be replaced by future `manage.py gopher`

See `_scripts/deprecated/README.md` for migration guide and details.

## Small Web Protocols

Results can be seen at:
- **Gopher:** [gopher://gopher.club:70/1/users/ecliptik](gopher://gopher.club:70/1/users/ecliptik)
- **Gemini:** [gemini://gmi.ecliptik.com](gemini://gmi.ecliptik.com)

These tools were inspired by [Making a Gopherhole](https://johngodlee.github.io/2019/11/20/gopher.html).

### Gopher Protocol (Implemented)

Generate gopher content with `python3 _scripts/manage.py gopher`:
- RFC1436-compliant gophermaps
- Markdown to plaintext conversion (Pandoc, 70 columns)
- Image references with URLs
- Year archives and tag navigation
- Docker test stack included

See above for detailed usage and `tests/README.md` for testing.

### Gemini Protocol (Implemented)

Generate gemini capsule content from Jekyll posts.

**Basic usage (localhost testing):**
```bash
python3 _scripts/manage.py gemini
```

**Production deployment (SDF.org):**
```bash
python3 _scripts/manage.py gemini --host sdf.org --port 1965 --base-url "gemini://sdf.org/ecliptik/"
```

**Options:**
- `--host HOST` - Gemini host (default: localhost)
- `--port PORT` - Gemini port (default: 1965)
- `--base-url URL` - Full base URL (overrides host/port)
- `--force` - Force regeneration of all files

**What it does:**
- Scans `_posts/` for markdown posts (30 posts)
- Converts markdown to gemtext format (.gmi files)
- Generates gemini capsule in `_gemini/` directory
- Creates year archives (8 years: 2011, 2015, 2017, 2021-2025)
- Creates tag pages (63 tags)
- Creates navigation indexes (root, blog, tags)
- Converts static pages (about, contact)

**Key features:**
- Native gemtext format (not plaintext like gopher)
- NO line wrapping (gemini clients handle it)
- Link syntax: `=> URL optional text`
- Heading syntax: `#` (h1), `##` (h2), `###` (h3)
- Preserves ASCII art header from `_gemini/_layouts/gem_header`
- Reuses abstractions from `smallweb_core.py`

**Output structure:**
```
_gemini/
├── index.gmi                 # Root page with navigation
├── about.gmi                 # Static pages
├── contact.gmi
├── blog/
│   ├── index.gmi             # Year list
│   ├── 2025/
│   │   ├── index.gmi         # Posts in 2025
│   │   └── *.gmi             # Individual posts
│   └── ...
└── tags/
    ├── index.gmi             # Tag list
    ├── linux.gmi             # Tag pages
    └── ...
```

**Testing:**
```bash
# Verify generation
bash tests/verify_gemini.sh

# Test with Docker
docker compose -f smallweb/gemini/docker-compose.yml up -d
amfora gemini://localhost:1965/
docker compose -f smallweb/gemini/docker-compose.yml down
```

**Deploy to SDF.org:**
```bash
# Generate for production
python3 _scripts/manage.py gemini --host sdf.org --base-url "gemini://sdf.org/ecliptik/"

# Upload
rsync -avz --delete _gemini/ username@sdf.org:gemini/

# Set permissions
ssh username@sdf.org 'chmod -R a+rX ~/gemini/'
```

**See also:**
- `GEMINI_DEPLOY.md` - Full deployment guide
- `tests/README.md` - Testing documentation
- `_scripts/gemini_generator.py` - Implementation details
