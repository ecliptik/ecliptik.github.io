#!/usr/bin/env python3

"""
smallweb_core.py - Reusable Abstractions for Small Web Protocols

Provides abstract base classes and shared utilities for generating content
for small web protocols (Gopher, Gemini, etc.). These abstractions allow
for code reuse across different protocol implementations.

Architecture:
- SmallWebConverter: Abstract base for protocol-specific converters
- PostScanner: Scan and parse Jekyll posts
- TagAggregator: Aggregate and organize tags
- YearOrganizer: Organize posts by year
- NavigationContext: Shared navigation context

Usage:
    from smallweb_core import SmallWebConverter, PostScanner

    class MyProtocolConverter(SmallWebConverter):
        def convert_post(self, metadata, content):
            # Protocol-specific implementation
            pass
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
import glob
import os
import re


# ============================================================================
# Shared Data Structures
# ============================================================================

@dataclass
class PostMetadata:
    """Structured metadata for a blog post (reusable across protocols)."""
    title: str
    date: datetime
    tags: List[str]
    category: str
    description: str
    slug: str
    year: str
    filepath: str
    is_markdown: bool
    redirect_from: Optional[str] = None

    @property
    def date_str(self) -> str:
        """Format date as YYYY-MM-DD."""
        return self.date.strftime('%Y-%m-%d')

    @property
    def gemini_filename(self) -> str:
        """Get gemini filename (slug.gmi)."""
        return f"{self.slug}.gmi"

    @property
    def gemini_path(self) -> str:
        """Get gemini path relative to capsule root."""
        return f"/blog/{self.year}/{self.slug}.gmi"


# ============================================================================
# Abstract Base Class for Protocol Converters
# ============================================================================

class SmallWebConverter(ABC):
    """
    Abstract base class for small web protocol converters.

    Subclasses implement protocol-specific conversion logic while
    sharing common utilities and structure.
    """

    def __init__(self, config):
        """Initialize converter with protocol-specific configuration."""
        self.config = config

    @abstractmethod
    def convert_post(self, metadata: PostMetadata, content: str) -> str:
        """
        Convert a single post to the target protocol format.

        Args:
            metadata: Post metadata
            content: Post content (raw markdown or HTML)

        Returns:
            Converted content in protocol format
        """
        pass

    @abstractmethod
    def build_index(self, posts: List[PostMetadata], title: str) -> str:
        """
        Build an index page listing posts.

        Args:
            posts: List of post metadata
            title: Index page title

        Returns:
            Index content in protocol format
        """
        pass

    @abstractmethod
    def format_link(self, title: str, path: str) -> str:
        """
        Format a link in the protocol's syntax.

        Args:
            title: Link title
            path: Link path

        Returns:
            Formatted link string
        """
        pass

    def clean_content(self, content: str) -> str:
        """Clean and normalize content (shared utility)."""
        # Remove multiple blank lines
        content = re.sub(r'\n{3,}', '\n\n', content)
        # Strip trailing whitespace
        content = '\n'.join(line.rstrip() for line in content.split('\n'))
        return content.strip()

    def extract_images(self, content: str) -> List[tuple]:
        """Extract image references from markdown content (shared utility)."""
        # Match markdown image syntax: ![alt](path)
        pattern = r'!\[([^\]]*)\]\(([^\)]+)\)'
        matches = re.findall(pattern, content)
        return [(alt, path) for alt, path in matches]


# ============================================================================
# Post Scanner (Reusable)
# ============================================================================

class PostScanner:
    """
    Scan Jekyll posts directory and extract metadata.

    This scanner is protocol-agnostic and can be used by any
    small web protocol generator.
    """

    def __init__(self, posts_dir: str = "_posts"):
        """Initialize scanner with posts directory path."""
        self.posts_dir = posts_dir

    def scan_posts(self) -> List[PostMetadata]:
        """
        Scan posts directory and extract metadata from all posts.

        Returns:
            List of PostMetadata objects
        """
        posts = []

        # Find all post files (markdown and HTML)
        post_files = glob.glob(os.path.join(self.posts_dir, '**', '*.md'), recursive=True)
        post_files += glob.glob(os.path.join(self.posts_dir, '**', '*.html'), recursive=True)

        for filepath in post_files:
            metadata = self._extract_metadata(filepath)
            if metadata:
                posts.append(metadata)

        return posts

    def _extract_metadata(self, filepath: str) -> Optional[PostMetadata]:
        """Extract metadata from a single post file."""
        frontmatter = self._parse_frontmatter(filepath)

        if not frontmatter:
            return None

        # Extract date from filename (YYYY-MM-DD format)
        filename = os.path.basename(filepath)
        date_match = re.match(r'(\d{4})-(\d{2})-(\d{2})-(.+)\.(md|html)', filename)

        if not date_match:
            print(f"Warning: Could not parse date from filename: {filename}")
            return None

        year, month, day, slug = date_match.groups()[:4]
        date = datetime(int(year), int(month), int(day))

        # Extract fields with fallbacks
        title = frontmatter.get('title', slug.replace('-', ' ').title())
        tags = frontmatter.get('tags', [])
        category = frontmatter.get('category', 'blog')
        description = frontmatter.get('description', '')
        redirect_from = frontmatter.get('redirect_from', None)
        is_markdown = filepath.endswith('.md')

        return PostMetadata(
            title=title,
            date=date,
            tags=tags,
            category=category,
            description=description,
            slug=slug,
            year=year,
            filepath=filepath,
            is_markdown=is_markdown,
            redirect_from=redirect_from
        )

    def _parse_frontmatter(self, filepath: str) -> Dict:
        """Parse YAML frontmatter from a post file."""
        try:
            with open(filepath, 'r', encoding='utf8') as f:
                content = f.read()

            # Parse frontmatter (works for both markdown and HTML)
            frontmatter = {}
            lines = content.split('\n')
            in_frontmatter = False

            for i, line in enumerate(lines):
                line = line.strip()

                if line == '---':
                    if not in_frontmatter and i == 0:
                        in_frontmatter = True
                        continue
                    elif in_frontmatter:
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
            print(f"Error parsing {filepath}: {e}")
            return {}


# ============================================================================
# Tag Aggregator (Reusable)
# ============================================================================

class TagAggregator:
    """
    Aggregate and organize posts by tags.

    Protocol-agnostic tag aggregation utility.
    """

    @staticmethod
    def collect_tags(posts: List[PostMetadata]) -> Dict[str, List[PostMetadata]]:
        """
        Collect all tags and group posts by tag.

        Args:
            posts: List of post metadata

        Returns:
            Dictionary mapping tag names to lists of posts
        """
        tags = {}
        for post in posts:
            for tag in post.tags:
                if tag not in tags:
                    tags[tag] = []
                tags[tag].append(post)
        return tags

    @staticmethod
    def get_posts_by_tag(posts: List[PostMetadata], tag: str) -> List[PostMetadata]:
        """
        Get all posts with a specific tag.

        Args:
            posts: List of post metadata
            tag: Tag name

        Returns:
            List of posts with the tag
        """
        return [post for post in posts if tag in post.tags]

    @staticmethod
    def get_tag_list(posts: List[PostMetadata]) -> List[str]:
        """
        Get list of unique tags from posts.

        Args:
            posts: List of post metadata

        Returns:
            Sorted list of unique tag names
        """
        tags = set()
        for post in posts:
            tags.update(post.tags)
        return sorted(tags)


# ============================================================================
# Year Organizer (Reusable)
# ============================================================================

class YearOrganizer:
    """
    Organize posts by year.

    Protocol-agnostic year organization utility.
    """

    @staticmethod
    def group_by_year(posts: List[PostMetadata]) -> Dict[str, List[PostMetadata]]:
        """
        Group posts by year.

        Args:
            posts: List of post metadata

        Returns:
            Dictionary mapping year strings to lists of posts
        """
        years = {}
        for post in posts:
            year = post.year
            if year not in years:
                years[year] = []
            years[year].append(post)
        return years

    @staticmethod
    def get_posts_by_year(posts: List[PostMetadata], year: str) -> List[PostMetadata]:
        """
        Get all posts from a specific year.

        Args:
            posts: List of post metadata
            year: Year string (YYYY)

        Returns:
            List of posts from that year
        """
        return [post for post in posts if post.year == year]

    @staticmethod
    def get_years(posts: List[PostMetadata]) -> List[str]:
        """
        Get list of years with posts.

        Args:
            posts: List of post metadata

        Returns:
            Sorted list of year strings
        """
        years = set(post.year for post in posts)
        return sorted(years)


# ============================================================================
# Navigation Context (Reusable)
# ============================================================================

@dataclass
class NavigationContext:
    """
    Shared navigation context for building breadcrumbs and links.

    Can be used by any protocol generator to build consistent
    navigation structures.
    """
    current_path: str
    parent_paths: List[tuple]  # List of (title, path) tuples
    siblings: List[PostMetadata]
    children: List[str]

    @classmethod
    def from_post(cls, post: PostMetadata, all_posts: List[PostMetadata]):
        """
        Create navigation context from a post.

        Args:
            post: Current post
            all_posts: All posts for finding siblings

        Returns:
            NavigationContext object
        """
        # Build parent paths (home -> blog -> year)
        parent_paths = [
            ("Home", "/"),
            ("Blog", "/blog"),
            (post.year, f"/blog/{post.year}")
        ]

        # Find siblings (posts in same year)
        siblings = [p for p in all_posts if p.year == post.year and p != post]

        return cls(
            current_path=f"/blog/{post.year}/{post.slug}",
            parent_paths=parent_paths,
            siblings=siblings,
            children=[]
        )

    @classmethod
    def from_year(cls, year: str, all_posts: List[PostMetadata]):
        """
        Create navigation context from a year archive.

        Args:
            year: Year string
            all_posts: All posts for finding posts in year

        Returns:
            NavigationContext object
        """
        parent_paths = [
            ("Home", "/"),
            ("Blog", "/blog")
        ]

        # Children are posts in this year
        children_posts = [p for p in all_posts if p.year == year]

        return cls(
            current_path=f"/blog/{year}",
            parent_paths=parent_paths,
            siblings=[],
            children=[p.slug for p in children_posts]
        )

    @classmethod
    def from_tag(cls, tag: str, all_posts: List[PostMetadata]):
        """
        Create navigation context from a tag page.

        Args:
            tag: Tag name
            all_posts: All posts for finding posts with tag

        Returns:
            NavigationContext object
        """
        parent_paths = [
            ("Home", "/"),
            ("Tags", "/tags")
        ]

        # Children are posts with this tag
        children_posts = [p for p in all_posts if tag in p.tags]

        return cls(
            current_path=f"/tags/{tag}",
            parent_paths=parent_paths,
            siblings=[],
            children=[p.slug for p in children_posts]
        )


# ============================================================================
# Utility Functions
# ============================================================================

def slugify(text: str) -> str:
    """
    Convert text to URL-friendly slug.

    Args:
        text: Text to slugify

    Returns:
        Slugified text
    """
    slug = text.lower().strip()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[-\s]+', '-', slug)
    return slug


def extract_date_from_filename(filename: str) -> Optional[datetime]:
    """
    Extract date from Jekyll post filename.

    Args:
        filename: Post filename (YYYY-MM-DD-slug.ext)

    Returns:
        datetime object or None if parsing fails
    """
    match = re.match(r'(\d{4})-(\d{2})-(\d{2})-', filename)
    if match:
        year, month, day = match.groups()
        return datetime(int(year), int(month), int(day))
    return None


# ============================================================================
# Example Usage (for documentation)
# ============================================================================

if __name__ == '__main__':
    print("smallweb_core.py - Reusable abstractions for small web protocols")
    print()
    print("This module provides:")
    print("  - SmallWebConverter: Abstract base class for protocol converters")
    print("  - PostScanner: Scan and parse Jekyll posts")
    print("  - TagAggregator: Organize posts by tags")
    print("  - YearOrganizer: Organize posts by years")
    print("  - NavigationContext: Build navigation breadcrumbs")
    print()
    print("See gopher_generator.py for example implementation")
    print("Future: gemini_generator.py will reuse these abstractions")
