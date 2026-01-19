#!/usr/bin/env python3

"""
gopher_generator.py - Gopher Protocol Content Generator

Generates RFC1436-compliant gopher content from Jekyll blog posts.
Uses gophermaps for navigation and converts markdown to plaintext.

Built on shared abstractions from smallweb_core.py for code reuse
with future Gemini generator.

Usage:
    python3 _scripts/manage.py gopher [--force] [--base-url URL] [--host HOST] [--port PORT]
"""

import os
import re
import subprocess
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

# Import shared abstractions
from smallweb_core import (
    SmallWebConverter,
    PostScanner,
    TagAggregator,
    YearOrganizer,
    PostMetadata,
    NavigationContext
)


# ============================================================================
# Configuration
# ============================================================================

@dataclass
class GopherConfig:
    """Configuration for gopher generation."""
    base_url: str = "gopher://gopher.club:70/1/users/ecliptik/"
    host: str = "gopher.club"
    port: int = 70
    columns: int = 70
    max_recent_posts: int = 10
    output_dir: str = "_gopher"
    posts_dir: str = "_posts"
    pages_dir: str = "_pages"
    force: bool = False

    @classmethod
    def from_args(cls, args):
        """Create config from command-line arguments."""
        config = cls()
        if hasattr(args, 'base_url') and args.base_url:
            config.base_url = args.base_url
        if hasattr(args, 'host') and args.host:
            config.host = args.host
        if hasattr(args, 'port') and args.port:
            config.port = args.port
        if hasattr(args, 'columns') and args.columns:
            config.columns = args.columns
        if hasattr(args, 'force') and args.force:
            config.force = args.force
        return config


# Add gopher-specific properties to PostMetadata
def _add_gopher_properties():
    """Add gopher-specific properties to PostMetadata."""
    @property
    def gopher_filename(self) -> str:
        """Generate gopher filename (plaintext)."""
        return f"{self.date_str}-{self.slug}.txt"

    @property
    def gopher_path(self) -> str:
        """Generate gopher path relative to root."""
        return f"/blog/{self.year}/{self.gopher_filename}"

    PostMetadata.gopher_filename = gopher_filename
    PostMetadata.gopher_path = gopher_path

_add_gopher_properties()


# ============================================================================
# Gopher Converter
# ============================================================================

class GopherConverter(SmallWebConverter):
    """Convert content to gopher plaintext format."""

    def convert_post(self, metadata: PostMetadata, content: str) -> str:
        """Convert a post to gopher plaintext format (implements SmallWebConverter)."""
        if metadata.is_markdown:
            plaintext = self.markdown_to_plaintext(metadata.filepath, metadata)
        else:
            plaintext = self.html_to_plaintext(metadata.filepath, metadata)

        # Add metadata header
        plaintext = self.add_metadata_header(plaintext, metadata)

        # Clean content
        plaintext = self.clean_content(plaintext)

        return plaintext

    def build_index(self, posts: List[PostMetadata], title: str) -> str:
        """Build an index gophermap (implements SmallWebConverter)."""
        builder = GophermapBuilder(self.config)
        builder.add_info_line(title)
        builder.add_separator()
        builder.add_info_line()

        # Add posts
        for post in posts:
            link_title = f"{post.date_str} {post.title}"
            builder.add_text_link(link_title, post.gopher_path)

        return builder.build()

    def format_link(self, title: str, path: str) -> str:
        """Format a gopher link (implements SmallWebConverter)."""
        return f"0{title}\t{path}\t{self.config.host}\t{self.config.port}"

    def add_metadata_header(self, content: str, metadata: PostMetadata) -> str:
        """Add metadata header to post content."""
        separator = "_" * 70
        header = f"""{separator}
title: {metadata.title}
tags: {' '.join(metadata.tags)}
date: {metadata.date_str}
{separator}

"""
        return header + content

    def markdown_to_plaintext(self, source: str, metadata: PostMetadata) -> str:
        """Convert markdown to plaintext using Pandoc."""
        try:
            # Read source content
            with open(source, 'r', encoding='utf8') as f:
                content = f.read()

            # Extract images before conversion for better processing
            images = self.extract_images(content)

            # Remove frontmatter
            content = self._remove_frontmatter(content)

            # Use Pandoc to convert to plaintext
            # --wrap=auto wraps at specified column width
            # --columns sets the wrap width
            result = subprocess.run(
                ['pandoc', '-f', 'markdown', '-t', 'plain',
                 '--wrap=auto', f'--columns={self.config.columns}'],
                input=content,
                capture_output=True,
                text=True,
                encoding='utf8'
            )

            if result.returncode != 0:
                print(f"Error converting {source}: {result.stderr}")
                return content

            plaintext = result.stdout

            # Post-process to clean up image references
            plaintext = self._process_image_references(plaintext, images)

            return plaintext

        except FileNotFoundError:
            print("Error: Pandoc not installed. Install with: apt install pandoc")
            return ""
        except Exception as e:
            print(f"Error converting {source}: {e}")
            return ""

    def html_to_plaintext(self, source: str, metadata: PostMetadata) -> str:
        """Convert HTML to plaintext (stub for Phase 2)."""
        # TODO: Implement HTML conversion with BeautifulSoup
        print(f"Note: HTML conversion not yet implemented for {source}")
        return f"[HTML post conversion coming soon]\n\nSee: https://www.ecliptik.com{metadata.gopher_path}"

    def _process_image_references(self, content: str, images: List[tuple]) -> str:
        """Post-process plaintext to clean up image references."""
        # Remove Jekyll/Kramdown attributes like {: width="60%"}
        content = re.sub(r'\{:.*?\}', '', content)

        # Remove leftover markdown link reference markers
        content = re.sub(r'\]\(([^\)]+)\)', '', content)

        # Clean up standalone square brackets around alt text
        # These are leftover from pandoc conversion
        content = re.sub(r'\[([^\]]+)\]\s*\n', r'[Image: \1]\n', content)

        # Add image references with URLs at the end if we have images
        if images:
            image_refs = []
            for i, (alt, path) in enumerate(images, 1):
                # Convert relative paths to full URLs
                if path.startswith('/'):
                    url = f"https://www.ecliptik.com{path}"
                elif path.startswith('http'):
                    url = path
                else:
                    url = f"https://www.ecliptik.com/{path}"

                # Only add if alt text exists
                if alt:
                    image_refs.append(f"  [{i}] {alt}: {url}")

            # Append image references if any exist
            if image_refs:
                separator = "_" * 70
                content += f"\n\n{separator}\nImages:\n" + '\n'.join(image_refs) + f"\n{separator}\n"

        return content

    def _remove_frontmatter(self, content: str) -> str:
        """Remove YAML frontmatter from content."""
        lines = content.split('\n')
        in_frontmatter = False
        result_lines = []

        for i, line in enumerate(lines):
            if line.strip() == '---':
                if not in_frontmatter and i == 0:
                    in_frontmatter = True
                    continue
                elif in_frontmatter:
                    in_frontmatter = False
                    continue
            elif not in_frontmatter:
                result_lines.append(line)

        return '\n'.join(result_lines)


# ============================================================================
# Gophermap Builder
# ============================================================================

class GophermapBuilder:
    """Build RFC1436-compliant gophermaps."""

    def __init__(self, config: GopherConfig):
        self.config = config
        self.lines = []

    def add_info_line(self, text: str = ""):
        """Add information line (non-selectable)."""
        # Info lines don't need host/port
        self.lines.append(f"i{text}")
        return self

    def add_separator(self, char: str = "_", length: int = 70):
        """Add separator line."""
        separator = char * length
        self.lines.append(f"i{separator}")
        return self

    def add_text_link(self, title: str, path: str):
        """Add text file link."""
        self.lines.append(f"0{title}\t{path}\t{self.config.host}\t{self.config.port}")
        return self

    def add_directory_link(self, title: str, path: str):
        """Add directory/menu link."""
        self.lines.append(f"1{title}\t{path}\t{self.config.host}\t{self.config.port}")
        return self

    def add_html_link(self, title: str, url: str):
        """Add HTML/web link."""
        self.lines.append(f"h{title}\tURL:{url}\t{self.config.host}\t{self.config.port}")
        return self

    def add_image_link(self, title: str, path: str, image_type: str = "I"):
        """Add image link (g=GIF, I=generic image)."""
        self.lines.append(f"{image_type}{title}\t{path}\t{self.config.host}\t{self.config.port}")
        return self

    def build(self) -> str:
        """Build final gophermap content."""
        return '\n'.join(self.lines) + '\n'

    def clear(self):
        """Clear all lines."""
        self.lines = []
        return self


# ============================================================================
# Navigation Builder
# ============================================================================

class NavigationBuilder:
    """Build breadcrumb navigation for gopher."""

    @staticmethod
    def build_breadcrumb(current_path: str, context: str = "") -> List[str]:
        """Build breadcrumb navigation links."""
        breadcrumbs = []

        # Always include home
        breadcrumbs.append("~ (home)")

        # Parse path components
        parts = current_path.strip('/').split('/')

        # Build path hierarchy
        if len(parts) >= 1 and parts[0] == 'blog':
            breadcrumbs.append("~/blog")

            if len(parts) >= 2 and parts[1].isdigit():
                year = parts[1]
                breadcrumbs.append(f"~/blog/{year}")

            if len(parts) >= 3:
                # Post name (truncate if too long)
                post_name = parts[2].replace('.txt', '')
                if len(post_name) > 40:
                    post_name = post_name[:37] + "..."
                breadcrumbs.append(f"~/blog/{parts[1]}/{post_name}")

        elif len(parts) >= 1 and parts[0] == 'tags':
            breadcrumbs.append("~/tags")

            if len(parts) >= 2:
                tag = parts[1]
                breadcrumbs.append(f"~/tags/{tag}")

        return breadcrumbs


# ============================================================================
# Gopher Generator (Main Orchestrator)
# ============================================================================

class GopherGenerator:
    """Main orchestrator for gopher content generation."""

    def __init__(self, config: GopherConfig):
        self.config = config
        self.converter = GopherConverter(config)
        self.scanner = PostScanner(config.posts_dir)
        self.posts: List[PostMetadata] = []

    def generate_all(self):
        """Generate all gopher content."""
        print("\n=== Gopher Generation ===\n")
        print(f"Output directory: {self.config.output_dir}")
        print(f"Base URL: {self.config.base_url}")
        print(f"Columns: {self.config.columns}")
        print()

        # Scan posts using shared PostScanner
        print("Scanning posts...")
        self.posts = self.scanner.scan_posts()
        markdown_posts = [p for p in self.posts if p.is_markdown]
        html_posts = [p for p in self.posts if not p.is_markdown]

        print(f"  Found {len(self.posts)} total posts")
        print(f"  - {len(markdown_posts)} markdown posts (2015-2026)")
        print(f"  - {len(html_posts)} HTML posts (2006-2011, not yet supported)")
        print()

        # Create output directory
        os.makedirs(self.config.output_dir, exist_ok=True)

        # Generate content (markdown posts only for now)
        print("Generating content...")
        self.generate_posts(markdown_posts)
        print()

        print("Generating navigation...")
        self.generate_year_archives(markdown_posts)
        self.generate_tag_pages(markdown_posts)
        self.generate_root_gophermap(markdown_posts)
        print()

        print("Generating static pages...")
        self.generate_pages()
        print()

        # Use shared organizers for statistics
        years = YearOrganizer.get_years(markdown_posts)
        tags = TagAggregator.collect_tags(markdown_posts)

        print("✅ Gopher generation complete!")
        print(f"\nGenerated content in: {self.config.output_dir}/")
        print(f"  - {len(markdown_posts)} posts")
        print(f"  - {len(years)} year archives")
        print(f"  - {len(tags)} tag pages")

    def generate_posts(self, posts: List[PostMetadata]):
        """Generate plaintext files for all posts."""
        for post in posts:
            # Create year directory
            year_dir = os.path.join(self.config.output_dir, 'blog', post.year)
            os.makedirs(year_dir, exist_ok=True)

            # Output path
            output_path = os.path.join(year_dir, post.gopher_filename)

            # Skip if exists and not forcing
            if os.path.exists(output_path) and not self.config.force:
                continue

            # Convert content using SmallWebConverter interface
            content = self.converter.convert_post(post, "")

            # Write output
            try:
                with open(output_path, 'w', encoding='utf8') as f:
                    f.write(content)
                print(f"  ✓ {post.year}/{post.gopher_filename}")
            except Exception as e:
                print(f"  ✗ Error writing {output_path}: {e}")

    def generate_year_archives(self, posts: List[PostMetadata]):
        """Generate year archive gophermaps."""
        # Use shared YearOrganizer
        years = YearOrganizer.get_years(posts)

        for year in years:
            year_posts = [p for p in posts if p.year == year]
            year_posts.sort(key=lambda p: p.date, reverse=True)

            # Create year directory
            year_dir = os.path.join(self.config.output_dir, 'blog', year)
            os.makedirs(year_dir, exist_ok=True)

            # Build gophermap
            builder = GophermapBuilder(self.config)
            builder.add_info_line(f"Blog Posts from {year}")
            builder.add_separator()
            builder.add_info_line()

            # Add breadcrumb
            breadcrumbs = NavigationBuilder.build_breadcrumb(f"/blog/{year}/")
            for crumb in breadcrumbs:
                builder.add_info_line(crumb)
            builder.add_info_line()
            builder.add_separator()
            builder.add_info_line()

            # Add posts
            for post in year_posts:
                title = f"{post.date_str} {post.title}"
                path = f"/blog/{year}/{post.gopher_filename}"
                builder.add_text_link(title, path)

            builder.add_info_line()
            builder.add_separator()

            # Add navigation links
            builder.add_directory_link("« Back to Blog", "/blog")
            builder.add_directory_link("« Home", "/")

            # Write gophermap
            gophermap_path = os.path.join(year_dir, 'gophermap')
            with open(gophermap_path, 'w', encoding='utf8') as f:
                f.write(builder.build())

            print(f"  ✓ Year archive: {year} ({len(year_posts)} posts)")

    def generate_tag_pages(self, posts: List[PostMetadata]):
        """Generate tag page gophermaps."""
        # Use shared TagAggregator
        tags = TagAggregator.collect_tags(posts)

        # Create tags directory
        tags_dir = os.path.join(self.config.output_dir, 'tags')
        os.makedirs(tags_dir, exist_ok=True)

        # Generate tag index
        builder = GophermapBuilder(self.config)
        builder.add_info_line("Tag Index")
        builder.add_separator()
        builder.add_info_line()
        builder.add_info_line("~/tags")
        builder.add_info_line()
        builder.add_separator()
        builder.add_info_line()

        for tag in sorted(tags.keys()):
            post_count = len(tags[tag])
            title = f"{tag} ({post_count})"
            builder.add_directory_link(title, f"/tags/{tag}")

        builder.add_info_line()
        builder.add_separator()
        builder.add_directory_link("« Home", "/")

        # Write tag index
        index_path = os.path.join(tags_dir, 'gophermap')
        with open(index_path, 'w', encoding='utf8') as f:
            f.write(builder.build())

        print(f"  ✓ Tag index ({len(tags)} tags)")

        # Generate individual tag pages
        for tag, tag_posts in tags.items():
            tag_posts.sort(key=lambda p: p.date, reverse=True)

            # Create tag directory
            tag_dir = os.path.join(tags_dir, tag)
            os.makedirs(tag_dir, exist_ok=True)

            # Build gophermap
            builder = GophermapBuilder(self.config)
            builder.add_info_line(f"Posts tagged: {tag}")
            builder.add_separator()
            builder.add_info_line()
            builder.add_info_line(f"~/tags/{tag}")
            builder.add_info_line()
            builder.add_separator()
            builder.add_info_line()

            # Add posts
            for post in tag_posts:
                title = f"{post.date_str} {post.title}"
                path = f"/blog/{post.year}/{post.gopher_filename}"
                builder.add_text_link(title, path)

            builder.add_info_line()
            builder.add_separator()
            builder.add_directory_link("« Back to Tags", "/tags")
            builder.add_directory_link("« Home", "/")

            # Write gophermap
            gophermap_path = os.path.join(tag_dir, 'gophermap')
            with open(gophermap_path, 'w', encoding='utf8') as f:
                f.write(builder.build())

        print(f"  ✓ Tag pages generated")

    def generate_root_gophermap(self, posts: List[PostMetadata]):
        """Generate root gophermap."""
        # Get recent posts
        recent_posts = sorted(posts, key=lambda p: p.date, reverse=True)
        recent_posts = recent_posts[:self.config.max_recent_posts]

        # Build gophermap
        builder = GophermapBuilder(self.config)
        builder.add_info_line("ecliptik's gopherhole")
        builder.add_separator()
        builder.add_info_line()
        builder.add_directory_link("Blog Posts", "/blog")
        builder.add_directory_link("Tags", "/tags")
        builder.add_text_link("About", "/about.txt")
        builder.add_text_link("Contact", "/contact.txt")
        builder.add_info_line()
        builder.add_separator()
        builder.add_info_line()
        builder.add_info_line("Recent Posts:")
        builder.add_info_line()

        # Add recent posts
        for post in recent_posts:
            title = f"{post.date_str} {post.title}"
            path = f"/blog/{post.year}/{post.gopher_filename}"
            builder.add_text_link(title, path)

        builder.add_info_line()
        builder.add_separator()
        builder.add_html_link("ecliptik.com", "https://www.ecliptik.com")

        # Write root gophermap
        gophermap_path = os.path.join(self.config.output_dir, 'gophermap')
        with open(gophermap_path, 'w', encoding='utf8') as f:
            f.write(builder.build())

        print(f"  ✓ Root gophermap")

        # Also create blog index
        blog_dir = os.path.join(self.config.output_dir, 'blog')
        os.makedirs(blog_dir, exist_ok=True)

        builder.clear()
        builder.add_info_line("Blog Posts")
        builder.add_separator()
        builder.add_info_line()
        builder.add_info_line("~/blog")
        builder.add_info_line()
        builder.add_separator()
        builder.add_info_line()

        # Add year archives using shared YearOrganizer
        years = YearOrganizer.get_years(posts)
        for year in sorted(years, reverse=True):
            year_posts = [p for p in posts if p.year == year]
            title = f"{year} ({len(year_posts)} posts)"
            builder.add_directory_link(title, f"/blog/{year}")

        builder.add_info_line()
        builder.add_separator()
        builder.add_directory_link("« Home", "/")

        blog_gophermap = os.path.join(blog_dir, 'gophermap')
        with open(blog_gophermap, 'w', encoding='utf8') as f:
            f.write(builder.build())

        print(f"  ✓ Blog index")

    def generate_pages(self):
        """Generate static pages (about, contact)."""
        pages = [
            ('about.md', 'about.txt'),
            ('contact.md', 'contact.txt')
        ]

        for source_name, output_name in pages:
            source_path = os.path.join(self.config.pages_dir, source_name)

            if not os.path.exists(source_path):
                print(f"  ⚠ Warning: {source_path} not found")
                continue

            # Create temporary metadata for page
            metadata = PostMetadata(
                title=source_name.replace('.md', '').title(),
                date=datetime.now(),
                tags=[],
                category='page',
                description='',
                slug=source_name.replace('.md', ''),
                year='',
                filepath=source_path,
                is_markdown=True
            )

            # Convert content (without metadata header)
            content = self.converter.markdown_to_plaintext(source_path, metadata)
            content = self.converter.clean_content(content)

            # Write output
            output_path = os.path.join(self.config.output_dir, output_name)
            try:
                with open(output_path, 'w', encoding='utf8') as f:
                    f.write(content)
                print(f"  ✓ {output_name}")
            except Exception as e:
                print(f"  ✗ Error writing {output_path}: {e}")
