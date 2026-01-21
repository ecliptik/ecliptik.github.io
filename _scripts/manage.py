#!/usr/bin/env python3

"""
manage.py - Unified Jekyll Blog Management Tool

A consolidated Python CLI tool for managing blog posts, tags, year archives,
and small web protocols (gopher/gemini) for the Jekyll blog.

Usage:
    python3 _scripts/manage.py post [-t TITLE] [-c CATEGORY] [-d DESCRIPTION] [--tags TAG1 TAG2...]
    python3 _scripts/manage.py tags
    python3 _scripts/manage.py years
    python3 _scripts/manage.py gopher
    python3 _scripts/manage.py gemini
    python3 _scripts/manage.py minify
    python3 _scripts/manage.py all

Run from repository root directory.
"""

import argparse
import glob
import os
import sys
from datetime import datetime
import re


# ============================================================================
# Configuration
# ============================================================================

POST_DIR = '_posts/'
TAG_DIR = 'tag/'
YEAR_PAGES_DIR = '_pages/years/'

COMMON_CATEGORIES = ['linux', 'devops', 'macos', 'retro', 'smolweb']

CANONICAL_TAGS = {
    # Operating Systems
    'macos', 'linux', 'windows',
    # Classic Computing
    'macintosh', '512ke', 'macplus',
    # Containers & Orchestration
    'docker', 'kubernetes', 'containers',
    # Cloud Providers
    'aws', 'gcp', 'azure',
    # DevOps & Tools
    'devops', 'ci-cd', 'git',
    # Shell & Terminal
    'terminal', 'bash', 'zsh',
    # Networking
    'networking',
    # Web
    'smolweb', 'gemini', 'gopher'
}


# ============================================================================
# Utility Functions
# ============================================================================

def slugify(text):
    """Convert text to URL-friendly slug."""
    # Convert to lowercase and replace spaces with hyphens
    slug = text.lower().strip()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug


def get_existing_tags():
    """Get list of existing tags from tag directory."""
    if not os.path.exists(TAG_DIR):
        return set()

    tag_files = glob.glob(TAG_DIR + '*.md')
    tags = set()
    for tag_file in tag_files:
        tag_name = os.path.basename(tag_file).replace('.md', '')
        tags.add(tag_name)
    return tags


def validate_tags(tags):
    """Validate tags and warn about new ones."""
    existing_tags = get_existing_tags()
    new_tags = []

    for tag in tags:
        if tag not in existing_tags and tag not in CANONICAL_TAGS:
            new_tags.append(tag)

    if new_tags:
        print(f"\n⚠️  Warning: New tags detected: {', '.join(new_tags)}")
        print("   Existing similar tags:")
        for new_tag in new_tags:
            similar = [t for t in existing_tags if new_tag in t or t in new_tag]
            if similar:
                print(f"   - For '{new_tag}': {', '.join(similar)}")

        response = input("\nContinue with these new tags? [y/N]: ")
        if response.lower() != 'y':
            return False

    return True


def parse_frontmatter(filename):
    """Parse frontmatter from a post file."""
    try:
        with open(filename, 'r', encoding='utf8') as f:
            frontmatter = {}
            in_frontmatter = False

            for line in f:
                line = line.strip()

                if line == '---':
                    if not in_frontmatter:
                        in_frontmatter = True
                    else:
                        break
                elif in_frontmatter:
                    if line.startswith('tags:'):
                        tags = line.replace('tags:', '').strip().split()
                        frontmatter['tags'] = tags
                    elif ':' in line:
                        key, value = line.split(':', 1)
                        frontmatter[key.strip()] = value.strip()

            return frontmatter
    except Exception as e:
        print(f"Error parsing {filename}: {e}")
        return {}


# ============================================================================
# Post Creation Command
# ============================================================================

def create_post(args):
    """Create a new blog post with complete frontmatter."""

    # Get title (CLI or interactive)
    if args.title:
        title = args.title
    else:
        print("\n=== Create New Blog Post ===\n")
        title = input("Title: ").strip()
        if not title:
            print("Error: Title is required")
            return 1

    # Get category (CLI or interactive)
    if args.category:
        category = args.category
    else:
        print(f"\nCommon categories: {', '.join(COMMON_CATEGORIES)}")
        category = input("Category: ").strip()
        if not category:
            print("Error: Category is required")
            return 1

    # Get description (CLI or interactive)
    if args.description:
        description = args.description
    else:
        print("\nDescription (1-2 sentences for SEO and social media):")
        description = input("> ").strip()
        if not description:
            print("Error: Description is required")
            return 1

    # Get tags (CLI or interactive)
    if args.tags:
        tags = args.tags
    else:
        print("\nTags (space-separated, lowercase):")
        print("Common tags: linux docker kubernetes macos terminal bash zsh")
        tags_input = input("> ").strip()
        if not tags_input:
            print("Error: At least one tag is required")
            return 1
        tags = tags_input.split()

    # Validate tags
    if not validate_tags(tags):
        print("Post creation cancelled.")
        return 1

    # Generate filename and paths
    today = datetime.now()
    year = today.strftime('%Y')
    date_prefix = today.strftime('%Y-%m-%d')
    slug = slugify(title)
    filename = f"{date_prefix}-{slug}.md"

    # Create year directory if it doesn't exist
    year_dir = os.path.join(POST_DIR, year)
    os.makedirs(year_dir, exist_ok=True)

    filepath = os.path.join(year_dir, filename)

    # Check if file already exists
    if os.path.exists(filepath):
        print(f"Error: File already exists: {filepath}")
        return 1

    # Generate frontmatter
    tags_str = ' '.join(tags)
    frontmatter = f"""---
layout: post
title: {title}
description: {description}
category: {category}
tags: {tags_str}
redirect_from: /{slug}/
---

"""

    # Write file
    try:
        with open(filepath, 'w', encoding='utf8') as f:
            f.write(frontmatter)

        print(f"\n✅ Created: {filepath}")
        print(f"   Slug: /{slug}/")
        print(f"   Redirect: /{slug}/ -> /blog/{year}/{slug}/")
        return 0

    except Exception as e:
        print(f"Error creating post: {e}")
        return 1


# ============================================================================
# Tag Generation Command
# ============================================================================

def generate_tags(args):
    """Generate tag pages from post frontmatter."""

    print("\n=== Generating Tag Pages ===\n")

    # Find all post files
    filenames = glob.glob(POST_DIR + '**/*.md', recursive=True)
    filenames += glob.glob(POST_DIR + '**/*.html', recursive=True)

    print(f"Scanning {len(filenames)} post files...")

    # Collect all tags
    total_tags = []
    for filename in filenames:
        frontmatter = parse_frontmatter(filename)
        if 'tags' in frontmatter:
            total_tags.extend(frontmatter['tags'])

    # Get unique tags
    unique_tags = set(total_tags)

    # Remove old tag files
    old_tags = glob.glob(TAG_DIR + '*.md')
    removed_count = len(old_tags)
    for tag_file in old_tags:
        os.remove(tag_file)

    # Create tag directory if it doesn't exist
    os.makedirs(TAG_DIR, exist_ok=True)

    # Generate new tag files
    for tag in sorted(unique_tags):
        tag_filename = TAG_DIR + tag + '.md'
        with open(tag_filename, 'w', encoding='utf8') as f:
            content = f"""---
layout: tagpage
title: "Tag: {tag}"
tag: {tag}
description: "Blog posts tagged with {tag} covering technical topics, tutorials, and experiences"
---
"""
            f.write(content)

    print(f"✅ Generated {len(unique_tags)} tag pages")
    print(f"   Removed {removed_count} old tag pages")

    # Report new tags not in canonical list
    new_tags = unique_tags - CANONICAL_TAGS
    if new_tags:
        print(f"\n⚠️  Tags not in canonical list: {', '.join(sorted(new_tags))}")

    return 0


# ============================================================================
# Year Archive Generation Command
# ============================================================================

def generate_years(args):
    """Generate year archive pages."""

    print("\n=== Generating Year Archive Pages ===\n")

    # Find all year directories in _posts/
    if not os.path.exists(POST_DIR):
        print(f"Error: {POST_DIR} directory not found")
        return 1

    years = set()
    for item in os.listdir(POST_DIR):
        item_path = os.path.join(POST_DIR, item)
        if os.path.isdir(item_path) and item.isdigit() and len(item) == 4:
            years.add(item)

    if not years:
        print("No year directories found in _posts/")
        return 0

    print(f"Found years: {', '.join(sorted(years))}")

    # Create year pages directory if it doesn't exist
    os.makedirs(YEAR_PAGES_DIR, exist_ok=True)

    # Generate year archive pages
    created = []
    for year in sorted(years):
        filename = f"blog-{year}.md"
        filepath = os.path.join(YEAR_PAGES_DIR, filename)

        # Check if already exists
        if os.path.exists(filepath):
            continue

        # Create year archive page
        content = f"""---
layout: yeararchive
permalink: /blog/{year}/
year: "{year}"
title: "Blog {year}"
description: "Blog posts from {year} covering technical topics, tutorials, and experiences"
---
"""

        try:
            with open(filepath, 'w', encoding='utf8') as f:
                f.write(content)
            created.append(year)
        except Exception as e:
            print(f"Error creating {filepath}: {e}")

    if created:
        print(f"✅ Created year archives: {', '.join(created)}")
    else:
        print("✅ All year archives up to date")

    return 0


# ============================================================================
# Gopher/Gemini Commands (Stubs)
# ============================================================================

def generate_gopher(args):
    """Generate gopher content from Jekyll blog posts."""
    try:
        from gopher_generator import GopherConfig, GopherGenerator

        # Create configuration from arguments
        config = GopherConfig.from_args(args)

        # Create generator and run
        generator = GopherGenerator(config)
        generator.generate_all()

        return 0

    except ImportError as e:
        print(f"Error: Could not import gopher_generator: {e}")
        print("Make sure gopher_generator.py is in the _scripts directory")
        return 1
    except Exception as e:
        print(f"Error during gopher generation: {e}")
        import traceback
        traceback.print_exc()
        return 1


def generate_gemini(args):
    """Generate gemini content."""
    print("\n=== Gemini Generation ===\n")

    try:
        from gemini_generator import GeminiConfig, GeminiGenerator

        # Create config from arguments
        config = GeminiConfig(
            host=getattr(args, 'host', 'localhost'),
            port=getattr(args, 'port', 1965),
            base_url=getattr(args, 'base_url', None),
            force=getattr(args, 'force', False)
        )

        # If base_url wasn't provided, construct from host/port
        if not config.base_url:
            config.base_url = f"gemini://{config.host}:{config.port}/"

        # Create generator and run
        generator = GeminiGenerator(config)
        generator.generate_all()

        return 0

    except Exception as e:
        print(f"Error during gemini generation: {e}")
        import traceback
        traceback.print_exc()
        return 1


# ============================================================================
# Minification Command
# ============================================================================

def minify_css(content):
    """Minify CSS content by removing comments and unnecessary whitespace."""
    # Remove CSS comments /* ... */
    content = re.sub(r'/\*[^*]*\*+(?:[^/*][^*]*\*+)*/', '', content)

    # Remove leading/trailing whitespace from each line
    content = '\n'.join(line.strip() for line in content.split('\n'))

    # Remove empty lines
    content = re.sub(r'\n+', '\n', content)

    # Remove whitespace around special characters
    content = re.sub(r'\s*([{}:;,>+~\[\]])\s*', r'\1', content)

    # Remove whitespace before opening brace
    content = re.sub(r'\s+{', '{', content)

    # Collapse multiple spaces into one
    content = re.sub(r' +', ' ', content)

    # Remove newlines (keep everything on fewer lines)
    content = content.replace('\n', '')

    return content


def minify_js(content):
    """Minify JavaScript content by removing comments and unnecessary whitespace."""
    # Remove single-line comments (// ...)
    # But preserve URLs (http://, https://)
    content = re.sub(r'(?<!:)//[^\n]*', '', content)

    # Remove multi-line comments /* ... */
    # But preserve license comments /*! ... */
    lines = content.split('\n')
    result = []
    in_comment = False

    for line in lines:
        if '/*!' in line:
            # Keep license comments
            result.append(line)
            continue

        if '/*' in line and '*/' not in line:
            in_comment = True
            # Keep the part before the comment
            result.append(line.split('/*')[0])
            continue
        elif '*/' in line:
            in_comment = False
            # Keep the part after the comment
            result.append(line.split('*/', 1)[1] if len(line.split('*/', 1)) > 1 else '')
            continue
        elif in_comment:
            continue
        else:
            result.append(line)

    content = '\n'.join(result)

    # Remove leading/trailing whitespace from each line
    content = '\n'.join(line.strip() for line in content.split('\n'))

    # Remove empty lines
    content = re.sub(r'\n+', '\n', content)

    # Collapse multiple spaces into one (but preserve strings)
    # This is a simple approach; a full JS minifier would parse the AST
    content = re.sub(r' +', ' ', content)

    return content


def minify_assets(args):
    """Minify CSS and JavaScript files."""
    print("\n=== Minifying Assets ===\n")

    css_files = [
        ('assets/css/console.css', 'assets/css/console.min.css')
    ]

    js_files = [
        ('assets/js/lazy-images.js', 'assets/js/lazy-images.min.js'),
        ('assets/js/theme-toggle.js', 'assets/js/theme-toggle.min.js'),
        ('assets/js/search-init.js', 'assets/js/search-init.min.js'),
        ('assets/js/image-captions.js', 'assets/js/image-captions.min.js'),
        ('assets/js/tooltip.js', 'assets/js/tooltip.min.js'),
    ]

    total_saved = 0

    # Minify CSS files
    print("Minifying CSS files...")
    for source, dest in css_files:
        if not os.path.exists(source):
            print(f"⚠️  Skipping {source} (not found)")
            continue

        with open(source, 'r', encoding='utf8') as f:
            original = f.read()

        minified = minify_css(original)

        with open(dest, 'w', encoding='utf8') as f:
            f.write(minified)

        original_size = len(original)
        minified_size = len(minified)
        saved = original_size - minified_size
        percent = (saved / original_size) * 100
        total_saved += saved

        print(f"  ✅ {source}")
        print(f"     {original_size:,} bytes → {minified_size:,} bytes ({percent:.1f}% reduction)")

    # Minify JS files
    print("\nMinifying JavaScript files...")
    for source, dest in js_files:
        if not os.path.exists(source):
            print(f"⚠️  Skipping {source} (not found)")
            continue

        with open(source, 'r', encoding='utf8') as f:
            original = f.read()

        minified = minify_js(original)

        with open(dest, 'w', encoding='utf8') as f:
            f.write(minified)

        original_size = len(original)
        minified_size = len(minified)
        saved = original_size - minified_size
        percent = (saved / original_size) * 100
        total_saved += saved

        print(f"  ✅ {source}")
        print(f"     {original_size:,} bytes → {minified_size:,} bytes ({percent:.1f}% reduction)")

    print(f"\n✅ Total savings: {total_saved:,} bytes ({total_saved/1024:.1f} KB)")
    print("\nNote: Update your layouts to reference .min.css and .min.js files")

    return 0


# ============================================================================
# All Command
# ============================================================================

def run_all(args):
    """Run tags and years generation."""
    print("\n=== Running All Updates ===\n")

    # Run tags
    result = generate_tags(args)
    if result != 0:
        return result

    # Run years
    result = generate_years(args)
    if result != 0:
        return result

    print("\n✅ All updates complete")
    return 0


# ============================================================================
# Main CLI
# ============================================================================

def main():
    """Main entry point for the CLI."""

    parser = argparse.ArgumentParser(
        description='Unified Jekyll blog management tool',
        epilog='Run from repository root directory'
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Post command
    post_parser = subparsers.add_parser('post', help='Create a new blog post')
    post_parser.add_argument('-t', '--title', help='Post title')
    post_parser.add_argument('-c', '--category', help='Post category')
    post_parser.add_argument('-d', '--description', help='Post description (SEO)')
    post_parser.add_argument('--tags', nargs='+', help='Post tags (space-separated)')
    post_parser.set_defaults(func=create_post)

    # Tags command
    tags_parser = subparsers.add_parser('tags', help='Generate tag pages')
    tags_parser.set_defaults(func=generate_tags)

    # Years command
    years_parser = subparsers.add_parser('years', help='Generate year archive pages')
    years_parser.set_defaults(func=generate_years)

    # Gopher command
    gopher_parser = subparsers.add_parser('gopher', help='Generate gopher content')
    gopher_parser.add_argument('--base-url', help='Gopher base URL (default: gopher://gopher.club:70/1/users/ecliptik/)')
    gopher_parser.add_argument('--host', help='Gopher host (default: gopher.club)')
    gopher_parser.add_argument('--port', type=int, help='Gopher port (default: 70)')
    gopher_parser.add_argument('--columns', type=int, help='Column width for text wrapping (default: 70)')
    gopher_parser.add_argument('--force', action='store_true', help='Force regeneration of all files')
    gopher_parser.set_defaults(func=generate_gopher)

    # Gemini command
    gemini_parser = subparsers.add_parser('gemini', help='Generate gemini content')
    gemini_parser.add_argument('--base-url', help='Gemini base URL (overrides host/port)')
    gemini_parser.add_argument('--host', default='localhost', help='Gemini host (default: localhost)')
    gemini_parser.add_argument('--port', type=int, default=1965, help='Gemini port (default: 1965)')
    gemini_parser.add_argument('--force', action='store_true', help='Force regeneration of all files')
    gemini_parser.set_defaults(func=generate_gemini)

    # Minify command
    minify_parser = subparsers.add_parser('minify', help='Minify CSS and JavaScript files')
    minify_parser.set_defaults(func=minify_assets)

    # All command
    all_parser = subparsers.add_parser('all', help='Run tags and years generation')
    all_parser.set_defaults(func=run_all)

    # Parse arguments
    args = parser.parse_args()

    # Check if command was provided
    if not args.command:
        parser.print_help()
        return 1

    # Check if running from repository root
    if not os.path.exists('_config.yml'):
        print("Error: Must run from repository root directory")
        print("       (directory containing _config.yml)")
        return 1

    # Run the command
    try:
        return args.func(args)
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
