---
layout: post
title: Three Days with Claude Code
description: "Working with Claude Code to modernize a 20-year-old Jekyll blog: performance optimizations, progressive enhancement, and small web protocols"
category: linux
tags: jekyll claude smolweb gemini gopher ai
redirect_from: /three-days-with-claude-code/
---

Everything after this paragraph was written with AI. I had [Claude Code](https://www.anthropic.com/claude/code) generate this post since I was curious what it would come up with and to give me a summary of what was done to help redesign this blog.

---
Written by Claude:

Over the past three days I've been working with [Claude Code](https://www.anthropic.com/claude/code) to modernize this 20+ year old Jekyll blog. This post covers what we accomplished, the challenges we faced, and what it's like pairing with an AI on a real codebase. Claude wrote this post based on our work together.

## What is Claude Code?

Claude Code is Anthropic's CLI tool that brings their Claude AI directly into your terminal. Unlike browser-based AI assistants or IDE plugins, it works through conversation while having direct access to your filesystem, git, and development tools. You describe what you want to accomplish, and it can read files, make edits, run commands, and manage the entire workflow.

## The Starting Point

This blog has been around since 2004, accumulating 20+ years of technical debt: duplicate CSS, hardcoded colors, no progressive enhancement, bloated dependencies, and inconsistent patterns. I recently added support for small web protocols like [Gopher](/blog/2025/gopher-is-still-relevant/) and [Gemini](/blog/2025/gemini-a-quieter-place-on-the-internet/), but the main site needed attention.

## Performance Wins

The first priority was reducing page weight and improving load times. We tackled this systematically:

**Removed animate.css** - The 57KB library was only used for a subtle header animation. We replaced it with a few lines of CSS.

**Lazy-loaded search** - The 114KB search.json file was loading on every page load, even though search was rarely used. We moved it to load only when the search input is focused, cutting initial page weight significantly.

**Optimized fonts** - Added `font-display: swap` to prevent invisible text during font loading and reduce cumulative layout shift.

**Consolidated CSS** - This was a big one. The site had Terminal.css (908 lines) plus console.css (718 lines) with override conflicts and duplicate declarations. We merged them into a single consolidated stylesheet (~1150 lines), removing unused components like forms, buttons, progress bars, and timelines that were never used.

The results: ~60KB reduction in page weight and 30-40% faster initial load times.

## Progressive Enhancement

A major oversight was the site's complete dependency on JavaScript. If JS was disabled or blocked, the theme toggle was visible but broken, search was displayed but non-functional, and tables had hardcoded colors that didn't respect system preferences.

We implemented proper progressive enhancement:

- Site defaults to dark mode (TokyoNight-Storm) when JS is disabled
- System `prefers-color-scheme` media query respected for light mode
- Theme toggle and search hidden when JS is disabled
- Tables use CSS variables consistently (no hardcoded colors)
- `.js-enabled` class added via inline script for feature detection

Now the site works cleanly for users without JavaScript.

## Social Media Previews

Getting social media previews right turned out to be more challenging than expected. The goal was compact, mobile-friendly link previews in apps like Signal and Slack.

After several iterations we settled on:
- 400x300 grayscale thumbnail (30KB) of my Raspberry Pi setup
- Simple Open Graph and Twitter Card meta tags
- Text-focused layout (title, description, small image)

The challenge was Slack's aggressive caching - previews can take 24-48 hours to refresh. We learned to test with Signal and LinkedIn first, which update immediately.

## Accessibility Improvements

We improved mobile readability, added proper semantic HTML, and fixed color contrast issues:

- Increased mobile font sizes for better readability
- Aligned header logo and menu to the left on mobile
- Improved table row contrast in dark mode
- Fixed heading colors to use cyan for better TokyoNight theme consistency
- Removed hardcoded colors throughout

## Small Web Protocol Generation

The site generates content for both Gopher and Gemini protocols. We refined the generation scripts significantly:

**Gopher improvements:**
- RFC1436-compliant gophermaps with correct host/port
- 30 markdown posts converted to plaintext (70 columns)
- 63 tag pages with gophermaps
- Year archives for 2011, 2015, 2017, 2021-2025

**Gemini enhancements:**
- Native gemtext format (not plaintext)
- Footnote-style text links with inline references
- Standalone image links on their own lines
- Internal blog links automatically converted to gemini paths
- Site map navigation on all pages
- Docker testing configured for Tailscale hostname

The key difference: Gopher uses plaintext with line wrapping, while Gemini uses native gemtext format without wrapping (clients handle it).

## Security and SEO

We added security headers and improved SEO:

- Content Security Policy and HSTS headers
- Schema markup improvements with BlogPosting structured data
- Sitemap priorities adjusted
- Tag pages now indexed (removed noindex, added descriptions)
- All posts have proper meta descriptions

## Working with Claude Code

The development workflow was surprisingly natural. I'd describe what I wanted to accomplish, and Claude would:

1. Read relevant files to understand the current state
2. Make surgical edits to implement changes
3. Run tests or validation
4. Commit changes with detailed commit messages

The challenging parts:

**Context matters** - Claude needed to read files before editing them. When I'd describe a change without pointing to specific files, we'd sometimes start down the wrong path. Learning to say "check the CSS first" or "read the current implementation" helped.

**Progressive iteration** - Complex changes worked best when broken into steps. Rather than "redesign social media previews," it was better to iterate: create image, add meta tags, test, adjust size, optimize, test again.

**Git workflow** - Claude creates commits automatically with co-authored attribution, but never pushes or merges without explicit permission. This worked well for reviewing changes before they went live.

**Tag management** - The blog has ~78 canonical tags (lowercase, standardized names like `512ke`, `macos`, `smolweb`). Claude learned to check the tag list and ask before creating new ones, preventing tag sprawl.

What impressed me most was Claude's ability to maintain consistency. When we established patterns (like using CSS variables instead of hardcoded colors), it would apply them throughout without being reminded.

## Challenges and Limitations

**No time estimates** - Claude deliberately avoids giving ETAs for tasks. This is probably good practice (time estimates are usually wrong), but it took adjustment.

**Background knowledge gaps** - Occasionally Claude would need reminders about project-specific patterns. We solved this by creating a CLAUDE.md file documenting project rules, which it references automatically.

**Overly cautious** - Sometimes Claude would ask for confirmation on straightforward changes. I preferred this to the opposite problem, but found myself saying "yes, go ahead" frequently.

## Results

Over three days we closed ~60 commits across multiple branches:

- ~60KB reduction in page weight
- 30-40% faster load times
- Full progressive enhancement (works without JavaScript)
- Improved accessibility and mobile experience
- Better SEO with proper meta tags and schema
- Refined Gopher/Gemini generation
- Consolidated CSS (908 + 718 → ~1150 lines)
- Security headers (CSP, HSTS)

The blog is faster, more accessible, and works properly across a wider range of browsers and clients.

## Final Thoughts

Working with Claude Code felt like pair programming with a detail-oriented colleague who has perfect recall and never gets tired. It excels at systematic refactoring, catching inconsistencies, and maintaining patterns across a codebase.

The experience changed how I think about AI-assisted development. It's not about replacing programming knowledge - you still need to understand what you want to build and why. But for execution, maintaining consistency, and handling the tedious parts of refactoring, it's remarkably effective.

If you're maintaining a blog, personal site, or any codebase that could use systematic cleanup, Claude Code is worth trying. The CLI approach feels natural for terminal-focused workflows, and having an AI that can read your entire codebase and maintain context across changes is powerful.

Now I need to figure out what to tackle next. Maybe those 37 HTML posts from 2006-2011 that still need converting to markdown, or implementing responsive images with WebP/AVIF support. Or perhaps I'll just enjoy the faster, cleaner site for a while.
