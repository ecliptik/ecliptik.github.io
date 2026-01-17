# Phlog

This directory contains some basic shell scripts to convert markdown posts that jekyll uses to build the html website at [ecliptik.com](https://www.ecliptik.com) to plaintext or a [gophermap](https://en.wikipedia.org/wiki/Gopher_(protocol)#Source_code_of_a_menu) to put onto a phlog on [gopher](https://en.wikipedia.org/wiki/Gopher_(protocol)).

These tools were inspired (and some parts copied) from [Making a Gopherhole](https://johngodlee.github.io/2019/11/20/gopher.html).

Results can be seen at my Gopherhole: [gopher://rawtext.club:70/1~ecliptik/phlog](gopher://rawtext.club:70/1~ecliptik/phlog)

## Tools

### md2gopher.sh

Takes a markdown post and converts it using [pandoc](https://pandoc.org) to plaintext, wrapping file at 70 characters to better fit gopherspace. Uses the header on the source markdown file to create a page title.

Files are output as `txt` to `_posts` subdiretory.

Script can loop through all markdown posts in `../_posts` for bulk conversion

```
for file in ../_posts/*.md; do ./md2gopher.sh ${file}; done
```

### md2gophermap.sh

Similar to `md2gopher.sh`, but will create sub-directories for each post and create a `gophermap` out of the markdown post. This is useful for "embedding" links in a native gophermap.

Has some known bugs like not wrapping code blocks.

Script can loop through all markdown posts in `../_posts` for bulk conversion
```
for file in ../_posts/*.md; do ./md2gophermap.sh ${file}; done
```


### phlogmap.sh

Create a `gophermap` linking the the latest 10 posts in `_posts`. Creates the link based off the `title:` in the post. Uses a template from `_layouts/phlog` to create a header for the file and appends a link to the original HTML blogsource at the end.

## Tag Generator

### tag_generator.py

Creates tag pages for the Jekyll blog based on tags found in post frontmatter.

**Run from the repository root:**

```bash
python3 _scripts/tag_generator.py
```

This will:
1. Scan all posts in `_posts/` for tags
2. Remove old tag files from `tag/`
3. Generate new tag page files in `tag/`

**Important:** Always run this script from the repository root directory, not from within `_scripts/`.

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
