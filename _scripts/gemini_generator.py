#!/usr/bin/env python3

"""
gemini_generator.py - Gemini Capsule Generation for Jekyll Blog

Generates Gemini protocol content from Jekyll markdown posts. Reuses abstractions
from smallweb_core.py for scanning posts, organizing by tags/years, and navigation.

Architecture:
- GeminiConfig: Configuration management
- GemtextBuilder: Build gemtext formatted content
- GeminiConverter: Convert markdown to gemtext (extends SmallWebConverter)
- GeminiGenerator: Main orchestrator

Usage:
    from gemini_generator import GeminiConfig, GeminiGenerator

    config = GeminiConfig(host="sdf.org", port=1965)
    generator = GeminiGenerator(config)
    generator.generate_all()

Gemtext Format:
- Links: => URL optional text
- Headings: # (h1), ## (h2), ### (h3)
- Lists: * Item text
- Quotes: > Quote text
- Preformatted: ``` ... ```
- Text: Plain lines (no markup)

Key Differences from Gopher:
- Native link support (not tab-delimited selectors)
- Native heading support (not plaintext separators)
- NO line wrapping (clients handle it)
- .gmi extension (not .txt)
- index.gmi files (not gophermap)
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
import os
import re
import glob
from datetime import datetime

# Import reusable abstractions
from smallweb_core import (
    SmallWebConverter,
    PostMetadata,
    PostScanner,
    TagAggregator,
    YearOrganizer,
    NavigationContext
)


# ============================================================================
# Configuration
# ============================================================================

@dataclass
class GeminiConfig:
    """Configuration for gemini capsule generation."""
    base_url: str = "gemini://localhost:1965/"
    host: str = "localhost"
    port: int = 1965
    max_recent_posts: int = 10
    output_dir: str = "_gemini"
    posts_dir: str = "_posts"
    pages_dir: str = "_pages"
    force: bool = False
    web_base_url: str = "https://www.ecliptik.com"

    @classmethod
    def from_args(cls, args):
        """
        Create config from CLI arguments.

        Args:
            args: argparse Namespace object

        Returns:
            GeminiConfig instance
        """
        base_url = f"gemini://{args.host}:{args.port}/"
        if hasattr(args, 'base_url') and args.base_url:
            base_url = args.base_url

        return cls(
            base_url=base_url,
            host=args.host,
            port=args.port,
            force=getattr(args, 'force', False),
            output_dir=getattr(args, 'output_dir', '_gemini'),
            posts_dir=getattr(args, 'posts_dir', '_posts'),
            pages_dir=getattr(args, 'pages_dir', '_pages')
        )


# ============================================================================
# Gemtext Builder
# ============================================================================

class GemtextBuilder:
    """
    Build gemtext formatted content.

    Similar to GophermapBuilder but for gemtext format. Provides methods
    to add different gemtext line types: links, headings, lists, etc.
    """

    def __init__(self):
        """Initialize empty gemtext builder."""
        self.lines = []

    def add_heading(self, text: str, level: int = 1):
        """
        Add a heading line.

        Args:
            text: Heading text
            level: Heading level (1-3, corresponds to #, ##, ###)

        Returns:
            self (for chaining)
        """
        if level < 1 or level > 3:
            level = min(max(level, 1), 3)  # Clamp to 1-3

        prefix = '#' * level
        self.lines.append(f"{prefix} {text}")
        return self

    def add_link(self, url: str, text: str = ""):
        """
        Add a link line.

        Args:
            url: Link URL
            text: Optional link text (if empty, URL is used)

        Returns:
            self (for chaining)
        """
        if text:
            self.lines.append(f"=> {url} {text}")
        else:
            self.lines.append(f"=> {url}")
        return self

    def add_text(self, text: str):
        """
        Add a plain text line.

        Args:
            text: Text content

        Returns:
            self (for chaining)
        """
        self.lines.append(text)
        return self

    def add_blank_line(self):
        """
        Add a blank line.

        Returns:
            self (for chaining)
        """
        self.lines.append("")
        return self

    def add_list_item(self, text: str):
        """
        Add a list item line.

        Args:
            text: List item text

        Returns:
            self (for chaining)
        """
        self.lines.append(f"* {text}")
        return self

    def add_quote(self, text: str):
        """
        Add a quote line.

        Args:
            text: Quote text

        Returns:
            self (for chaining)
        """
        self.lines.append(f"> {text}")
        return self

    def add_preformatted(self, content: str, alt_text: str = ""):
        """
        Add preformatted block.

        Args:
            content: Preformatted content
            alt_text: Optional alt text for opening fence

        Returns:
            self (for chaining)
        """
        if alt_text:
            self.lines.append(f"```{alt_text}")
        else:
            self.lines.append("```")
        self.lines.append(content)
        self.lines.append("```")
        return self

    def build(self) -> str:
        """
        Build final gemtext content.

        Returns:
            Gemtext string with newline-separated lines
        """
        return '\n'.join(self.lines)


# ============================================================================
# Gemini Converter
# ============================================================================

class GeminiConverter(SmallWebConverter):
    """
    Convert content to gemtext format.

    Extends SmallWebConverter abstract base class to implement gemini-specific
    conversion logic. Handles markdown to gemtext conversion, post formatting,
    and index page generation.
    """

    def __init__(self, config: GeminiConfig):
        """
        Initialize converter with configuration.

        Args:
            config: GeminiConfig instance
        """
        super().__init__(config)
        self.ascii_header = self._load_ascii_header()
        self.posts_lookup = {}  # URL path -> gemini path lookup

    def set_posts_lookup(self, posts: List[PostMetadata]):
        """
        Build lookup table of web URLs to gemini paths.

        Args:
            posts: List of all post metadata
        """
        self.posts_lookup = {}
        for post in posts:
            # Map both old and new permalink formats to gemini path
            # Old format: /Post-Title/
            # New format: /blog/YYYY/Post-Title/

            # New format permalink
            new_permalink = f"/blog/{post.year}/{post.slug}"
            self.posts_lookup[new_permalink] = post.gemini_path

            # Old format permalink (from redirect_from)
            if post.redirect_from:
                old_permalink = post.redirect_from.rstrip('/')
                self.posts_lookup[old_permalink] = post.gemini_path

    def _load_ascii_header(self) -> str:
        """
        Load ASCII art header template.

        Returns:
            ASCII art header string
        """
        header_path = os.path.join(self.config.output_dir, '_layouts', 'gem_header')
        if os.path.exists(header_path):
            with open(header_path, 'r', encoding='utf-8') as f:
                return f.read().strip()
        else:
            # Fallback ASCII art
            return r"""```
=====================================================================
             ___       __  _ __
  ___  _____/ (_)___  / /_(_) /__
 / _ \/ ___/ / / __ \/ __/ / //_/
/  __/ /__/ / / /_/ / /_/ / ,<
\___/\___/_/_/ .___/\__/_/_/|_|
            /_/
=====================================================================
```"""

    def convert_post(self, metadata: PostMetadata, content: str) -> str:
        """
        Convert a single post to gemtext format.

        Implements abstract method from SmallWebConverter.

        Args:
            metadata: Post metadata
            content: Post content (raw markdown)

        Returns:
            Converted gemtext content with header and metadata
        """
        # Convert markdown to gemtext
        gemtext_content = self.markdown_to_gemtext(content, metadata)

        # Add metadata header
        full_content = self.add_metadata_header(gemtext_content, metadata)

        return full_content

    def build_index(self, posts: List[PostMetadata], title: str) -> str:
        """
        Build an index page listing posts.

        Implements abstract method from SmallWebConverter.

        Args:
            posts: List of post metadata
            title: Index page title

        Returns:
            Gemtext index content
        """
        builder = GemtextBuilder()

        # Add title
        builder.add_heading(title, level=1)
        builder.add_blank_line()

        # List posts
        for post in sorted(posts, key=lambda p: p.date, reverse=True):
            builder.add_link(
                f"/blog/{post.year}/{post.slug}.gmi",
                f"{post.date_str} - {post.title}"
            )

        return builder.build()

    def format_link(self, title: str, path: str) -> str:
        """
        Format a link in gemini syntax.

        Implements abstract method from SmallWebConverter.

        Args:
            title: Link title
            path: Link path

        Returns:
            Formatted gemtext link
        """
        return f"=> {path} {title}"

    def markdown_to_gemtext(self, source: str, metadata: PostMetadata) -> str:
        """
        Convert markdown to gemtext using custom parser.

        Key conversion rules:
        - Headers: # → #, ## → ##, ### → ### (collapse >H3 to H3)
        - Links: [text](url) → => url text
        - Images: ![alt](path) → => https://... alt
        - Lists: -/* → *
        - Code blocks: preserve ```
        - Blockquotes: > → >
        - Emphasis: strip ** * `
        - NO line wrapping (gemini clients handle it)

        Args:
            source: Markdown source content
            metadata: Post metadata (for image path resolution)

        Returns:
            Gemtext formatted content
        """
        # Remove YAML frontmatter
        source = self._remove_frontmatter(source)

        lines = source.split('\n')
        output = []
        in_code_block = False
        code_block_lines = []
        code_block_lang = ""

        for line in lines:
            # Handle code blocks
            if line.strip().startswith('```'):
                if not in_code_block:
                    # Start code block
                    in_code_block = True
                    code_block_lang = line.strip()[3:].strip()
                    code_block_lines = []
                else:
                    # End code block
                    in_code_block = False
                    # Add preformatted block
                    if code_block_lang:
                        output.append(f"```{code_block_lang}")
                    else:
                        output.append("```")
                    output.extend(code_block_lines)
                    output.append("```")
                    code_block_lines = []
                    code_block_lang = ""
                continue

            if in_code_block:
                code_block_lines.append(line)
                continue

            # Convert headers (collapse >H3 to H3)
            if line.startswith('#'):
                match = re.match(r'^(#{1,6})\s+(.+)$', line)
                if match:
                    level = min(len(match.group(1)), 3)  # Max level 3
                    prefix = '#' * level
                    output.append(f"{prefix} {match.group(2)}")
                    continue

            # Convert blockquotes
            if line.startswith('>'):
                output.append(line)
                continue

            # Convert links and images FIRST (before list processing)
            line = self._convert_links_and_images(line, metadata)

            # Convert lists (unordered and ordered) AFTER link conversion
            list_match = re.match(r'^(\s*)([-*+]|\d+\.)\s+(.+)$', line)
            if list_match:
                item_text = list_match.group(3)
                # Strip any remaining markdown from list items
                item_text = self._strip_emphasis(item_text)
                output.append(f"* {item_text}")
                continue

            # Strip emphasis markers
            line = self._strip_emphasis(line)

            # Strip HTML tags
            line = self._strip_html_tags(line)

            # Skip empty lines at start
            if not output and not line.strip():
                continue

            # Add line (no wrapping - gemini clients handle it)
            output.append(line)

        # Remove consecutive duplicate lines (from HTML artifacts)
        cleaned_output = []
        prev_line = None
        for line in output:
            if line != prev_line or line.strip() == "":
                cleaned_output.append(line)
            prev_line = line

        return '\n'.join(cleaned_output)

    def _remove_frontmatter(self, content: str) -> str:
        """Remove YAML frontmatter from content."""
        lines = content.split('\n')
        if lines[0].strip() == '---':
            # Find closing ---
            for i in range(1, len(lines)):
                if lines[i].strip() == '---':
                    return '\n'.join(lines[i+1:])
        return content

    def _convert_links_and_images(self, line: str, metadata: PostMetadata) -> str:
        """
        Convert markdown links and images to gemtext.

        Args:
            line: Line of text
            metadata: Post metadata for path resolution

        Returns:
            Line with converted links
        """
        # Convert images: ![alt](path) → => full_url alt
        def replace_image(match):
            alt = match.group(1)
            path = match.group(2)
            # Convert relative paths to full URLs
            if not path.startswith('http'):
                if path.startswith('/'):
                    full_url = f"{self.config.web_base_url}{path}"
                else:
                    full_url = f"{self.config.web_base_url}/assets/images/{path}"
            else:
                full_url = path
            return f"=> {full_url} {alt}"

        line = re.sub(r'!\[([^\]]*)\]\(([^\)]+)\)', replace_image, line)

        # Remove empty link brackets: [](url) → ""
        line = re.sub(r'\[\]\([^\)]+\)', '', line)

        # Convert links: [text](url) → => url text
        def replace_link(match):
            text = match.group(1)
            url = match.group(2)

            # Check if this is an internal blog post link
            if url.startswith(self.config.web_base_url):
                # Extract path after base URL
                path = url.replace(self.config.web_base_url, '').rstrip('/')

                # Look up gemini path for this post
                if path in self.posts_lookup:
                    gemini_path = self.posts_lookup[path]
                    return f"=> {gemini_path} {text}"

            # External link or not found - keep as-is
            return f"=> {url} {text}"

        line = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', replace_link, line)

        # Convert bare URLs: <https://...> → => https://...
        line = re.sub(r'<(https?://[^>]+)>', r'=> \1', line)

        return line

    def _strip_emphasis(self, line: str) -> str:
        """
        Strip markdown emphasis markers.

        Args:
            line: Line of text

        Returns:
            Line with emphasis stripped
        """
        # Strip bold: **text** → text
        line = re.sub(r'\*\*([^\*]+)\*\*', r'\1', line)
        # Strip italic: *text* → text
        line = re.sub(r'\*([^\*]+)\*', r'\1', line)
        # Strip code: `text` → text
        line = re.sub(r'`([^`]+)`', r'\1', line)
        return line

    def _strip_html_tags(self, line: str) -> str:
        """
        Strip HTML tags from line.

        Args:
            line: Line of text

        Returns:
            Line with HTML tags removed
        """
        # Skip lines that are only HTML tags (figure captions, etc.)
        if re.match(r'^\s*<[^>]+>.*<[^>]+>\s*$', line):
            return ""

        # Remove HTML tags completely
        line = re.sub(r'<[^>]+>', '', line)
        return line

    def add_metadata_header(self, content: str, metadata: PostMetadata) -> str:
        """
        Add ASCII art header and metadata to content.

        Args:
            content: Gemtext content
            metadata: Post metadata

        Returns:
            Content with header prepended
        """
        builder = GemtextBuilder()

        # Add ASCII art
        builder.add_text(self.ascii_header)
        builder.add_blank_line()

        # Add title
        builder.add_heading(metadata.title, level=1)

        # Add metadata line (date and tags)
        tags_str = ' '.join(f"#{tag}" for tag in metadata.tags)
        builder.add_heading(f"{metadata.date_str} | {tags_str}", level=3)
        builder.add_blank_line()

        # Add content
        builder.add_text(content)

        return builder.build()


# ============================================================================
# Gemini Generator
# ============================================================================

class GeminiGenerator:
    """
    Main orchestrator for gemini capsule generation.

    Coordinates post scanning, conversion, and file generation for all
    gemini capsule content (posts, tags, years, indexes, static pages).
    """

    def __init__(self, config: GeminiConfig):
        """
        Initialize generator with configuration.

        Args:
            config: GeminiConfig instance
        """
        self.config = config
        self.converter = GeminiConverter(config)
        self.scanner = PostScanner(config.posts_dir)

    def generate_all(self):
        """Generate all gemini capsule content."""
        print(f"Generating Gemini capsule content...")
        print(f"  Output directory: {self.config.output_dir}")
        print(f"  Base URL: {self.config.base_url}")

        # Create output directory structure
        self._create_directories()

        # Scan posts
        print("\nScanning posts...")
        posts = self.scanner.scan_posts()

        # Filter to markdown posts only (for now)
        markdown_posts = [p for p in posts if p.is_markdown]
        print(f"  Found {len(markdown_posts)} markdown posts")

        # Build lookup table for internal links
        self.converter.set_posts_lookup(markdown_posts)

        # Generate content
        self.generate_posts(markdown_posts)
        self.generate_year_archives(markdown_posts)
        self.generate_tag_pages(markdown_posts)
        self.generate_root_index(markdown_posts)
        self.generate_pages()

        print(f"\n✓ Gemini capsule generated successfully!")
        print(f"  Total posts: {len(markdown_posts)}")
        print(f"  Years: {len(YearOrganizer.get_years(markdown_posts))}")
        print(f"  Tags: {len(TagAggregator.get_tag_list(markdown_posts))}")

    def _create_directories(self):
        """Create output directory structure."""
        dirs = [
            self.config.output_dir,
            os.path.join(self.config.output_dir, 'blog'),
            os.path.join(self.config.output_dir, 'tags'),
        ]

        # Add year directories
        for year in range(2011, datetime.now().year + 1):
            dirs.append(os.path.join(self.config.output_dir, 'blog', str(year)))

        for d in dirs:
            os.makedirs(d, exist_ok=True)

    def generate_posts(self, posts: List[PostMetadata]):
        """
        Generate gemini post files.

        Args:
            posts: List of post metadata
        """
        print("\nGenerating posts...")

        for post in posts:
            # Read post content
            try:
                with open(post.filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"  ✗ Error reading {post.filepath}: {e}")
                continue

            # Convert to gemtext
            gemtext = self.converter.convert_post(post, content)

            # Write to output file
            output_path = os.path.join(
                self.config.output_dir,
                'blog',
                post.year,
                post.gemini_filename
            )

            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(gemtext)
                print(f"  ✓ {post.year}/{post.gemini_filename}")
            except Exception as e:
                print(f"  ✗ Error writing {output_path}: {e}")

        print(f"  Generated {len(posts)} posts")

    def generate_year_archives(self, posts: List[PostMetadata]):
        """
        Generate year archive index files.

        Args:
            posts: List of post metadata
        """
        print("\nGenerating year archives...")

        # Group posts by year using YearOrganizer
        years = YearOrganizer.group_by_year(posts)

        for year, year_posts in sorted(years.items(), reverse=True):
            # Sort posts by date (newest first)
            year_posts_sorted = sorted(year_posts, key=lambda p: p.date, reverse=True)

            # Build index.gmi content
            builder = GemtextBuilder()

            # Add breadcrumb navigation
            builder.add_link("/", "← Home")
            builder.add_link("/blog/", "← Blog")
            builder.add_blank_line()

            # Add title
            builder.add_heading(f"Posts from {year}", level=1)
            builder.add_blank_line()

            # List posts
            for post in year_posts_sorted:
                builder.add_link(
                    f"{post.gemini_path}",
                    f"{post.date_str} - {post.title}"
                )

            # Write index.gmi file
            output_path = os.path.join(
                self.config.output_dir,
                'blog',
                year,
                'index.gmi'
            )

            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(builder.build())
                print(f"  ✓ {year}/index.gmi ({len(year_posts)} posts)")
            except Exception as e:
                print(f"  ✗ Error writing {output_path}: {e}")

        print(f"  Generated {len(years)} year archives")

    def generate_tag_pages(self, posts: List[PostMetadata]):
        """
        Generate tag pages.

        Args:
            posts: List of post metadata
        """
        print("\nGenerating tag pages...")

        # Collect tags using TagAggregator
        tags_dict = TagAggregator.collect_tags(posts)
        tag_list = TagAggregator.get_tag_list(posts)

        # Generate tags index page
        self._generate_tags_index(tag_list, tags_dict)

        # Generate individual tag pages
        for tag in sorted(tag_list):
            tag_posts = tags_dict[tag]
            self._generate_tag_page(tag, tag_posts)

        print(f"  Generated {len(tag_list)} tag pages")

    def _generate_tags_index(self, tag_list: List[str], tags_dict: Dict):
        """Generate tags/index.gmi with list of all tags."""
        builder = GemtextBuilder()

        # Add breadcrumb navigation
        builder.add_link("/", "← Home")
        builder.add_blank_line()

        # Add title
        builder.add_heading("Tags", level=1)
        builder.add_blank_line()

        # List all tags with post counts
        for tag in sorted(tag_list):
            count = len(tags_dict[tag])
            builder.add_link(
                f"/tags/{tag}.gmi",
                f"{tag} ({count} posts)"
            )

        # Write tags/index.gmi
        output_path = os.path.join(self.config.output_dir, 'tags', 'index.gmi')
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(builder.build())
            print(f"  ✓ tags/index.gmi")
        except Exception as e:
            print(f"  ✗ Error writing {output_path}: {e}")

    def _generate_tag_page(self, tag: str, tag_posts: List[PostMetadata]):
        """Generate individual tag page."""
        builder = GemtextBuilder()

        # Add breadcrumb navigation
        builder.add_link("/", "← Home")
        builder.add_link("/tags/", "← Tags")
        builder.add_blank_line()

        # Add title
        builder.add_heading(f"Tag: {tag}", level=1)
        builder.add_blank_line()

        # Sort posts by date (newest first)
        sorted_posts = sorted(tag_posts, key=lambda p: p.date, reverse=True)

        # List posts
        for post in sorted_posts:
            builder.add_link(
                f"{post.gemini_path}",
                f"{post.date_str} - {post.title}"
            )

        # Write tags/[tagname].gmi
        output_path = os.path.join(self.config.output_dir, 'tags', f'{tag}.gmi')
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(builder.build())
            print(f"  ✓ tags/{tag}.gmi ({len(tag_posts)} posts)")
        except Exception as e:
            print(f"  ✗ Error writing {output_path}: {e}")

    def generate_root_index(self, posts: List[PostMetadata]):
        """
        Generate root index.gmi file.

        Args:
            posts: List of post metadata
        """
        print("\nGenerating root index...")

        # Generate main index.gmi
        self._generate_main_index(posts)

        # Generate blog/index.gmi with year list
        self._generate_blog_index(posts)

    def _generate_main_index(self, posts: List[PostMetadata]):
        """Generate main index.gmi file."""
        builder = GemtextBuilder()

        # Add ASCII art header
        builder.add_text(self.converter.ascii_header)
        builder.add_blank_line()

        # Add title and description
        builder.add_heading("ecliptik", level=1)
        builder.add_text("Personal tech blog - cloud, DevOps, retro computing, small web protocols")
        builder.add_blank_line()

        # Add sitemap section
        builder.add_heading("Site Map", level=2)
        builder.add_link("/about.gmi", "About")
        builder.add_link("/contact.gmi", "Contact")
        builder.add_link("/blog/", "Blog")
        builder.add_link("/tags/", "Tags")
        builder.add_blank_line()

        # Add recent posts section
        builder.add_heading("Recent Posts", level=2)
        recent_posts = sorted(posts, key=lambda p: p.date, reverse=True)[:self.config.max_recent_posts]
        for post in recent_posts:
            builder.add_link(
                post.gemini_path,
                f"{post.date_str} - {post.title}"
            )
        builder.add_blank_line()

        # Add external links section
        builder.add_heading("Other Protocols", level=2)
        builder.add_link("https://www.ecliptik.com", "Web (HTTPS)")
        builder.add_link("gopher://gopher.club:70/1/users/ecliptik/", "Gopher")
        builder.add_blank_line()

        # Add footer
        builder.add_text("Made with Jekyll and gemini_generator.py")

        # Write index.gmi
        output_path = os.path.join(self.config.output_dir, 'index.gmi')
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(builder.build())
            print(f"  ✓ index.gmi")
        except Exception as e:
            print(f"  ✗ Error writing {output_path}: {e}")

    def _generate_blog_index(self, posts: List[PostMetadata]):
        """Generate blog/index.gmi with year list."""
        builder = GemtextBuilder()

        # Add breadcrumb navigation
        builder.add_link("/", "← Home")
        builder.add_blank_line()

        # Add title
        builder.add_heading("Blog", level=1)
        builder.add_blank_line()

        # Get years and post counts
        years = YearOrganizer.group_by_year(posts)

        # List years with post counts (newest first)
        builder.add_heading("Posts by Year", level=2)
        for year in sorted(years.keys(), reverse=True):
            count = len(years[year])
            builder.add_link(
                f"/blog/{year}/",
                f"{year} ({count} posts)"
            )

        # Write blog/index.gmi
        output_path = os.path.join(self.config.output_dir, 'blog', 'index.gmi')
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(builder.build())
            print(f"  ✓ blog/index.gmi")
        except Exception as e:
            print(f"  ✗ Error writing {output_path}: {e}")

    def generate_pages(self):
        """Generate static pages (about, contact)."""
        print("\nGenerating static pages...")

        # Define pages to convert
        pages = ['about.md', 'contact.md']

        for page_file in pages:
            page_path = os.path.join(self.config.pages_dir, page_file)

            if not os.path.exists(page_path):
                print(f"  ⚠ Skipping {page_file} (not found)")
                continue

            # Read page content
            try:
                with open(page_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"  ✗ Error reading {page_path}: {e}")
                continue

            # Convert to gemtext (without metadata header)
            gemtext = self._convert_static_page(content, page_file)

            # Write output file
            output_filename = page_file.replace('.md', '.gmi')
            output_path = os.path.join(self.config.output_dir, output_filename)

            try:
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(gemtext)
                print(f"  ✓ {output_filename}")
            except Exception as e:
                print(f"  ✗ Error writing {output_path}: {e}")

    def _convert_static_page(self, content: str, filename: str) -> str:
        """
        Convert static page to gemtext.

        Args:
            content: Page content
            filename: Filename for context

        Returns:
            Gemtext content
        """
        # Create a minimal metadata object for conversion
        from datetime import datetime
        metadata = PostMetadata(
            title=filename.replace('.md', '').title(),
            date=datetime.now(),
            tags=[],
            category='page',
            description='',
            slug=filename.replace('.md', ''),
            year='',
            filepath='',
            is_markdown=True
        )

        # Convert markdown to gemtext
        gemtext = self.converter.markdown_to_gemtext(content, metadata)

        # Add navigation footer
        builder = GemtextBuilder()
        builder.add_text(gemtext)
        builder.add_blank_line()
        builder.add_blank_line()
        builder.add_link("/", "← Home")

        return builder.build()


# ============================================================================
# CLI Entry Point (for testing)
# ============================================================================

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Generate Gemini capsule content')
    parser.add_argument('--host', default='localhost', help='Gemini host (default: localhost)')
    parser.add_argument('--port', type=int, default=1965, help='Gemini port (default: 1965)')
    parser.add_argument('--base-url', help='Full base URL (overrides host/port)')
    parser.add_argument('--force', action='store_true', help='Force regeneration of all content')
    parser.add_argument('--output-dir', default='_gemini', help='Output directory')

    args = parser.parse_args()
    config = GeminiConfig.from_args(args)
    generator = GeminiGenerator(config)
    generator.generate_all()
