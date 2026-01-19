# Stylesheet Consolidation Plan

## Current State
- **terminal-0.7.1.min.css** (908 lines): Third-party Terminal.css framework
- **console.css** (718 lines): Custom styles with heavy overrides

## Problems
1. **Duplication**: Both files define font stacks, terminal components, link styles, media queries
2. **Maintenance burden**: console.css constantly overrides terminal-0.7.1.css
3. **Confusion**: CLAUDE.md doesn't mention terminal-0.7.1.css at all
4. **Unused code**: Terminal.css includes forms, buttons, cards, timelines, alerts - none are used

## Goal
Create a single, consolidated `console.css` that:
- Contains only components actually used
- Eliminates all Terminal.css dependencies
- Reduces overall CSS size by ~30-40%
- Simplifies development workflow

## Used Terminal.css Classes
Based on template analysis:
- `.terminal` (body class)
- `.terminal-nav`, `.terminal-header-line`, `.terminal-prompt-line`
- `.terminal-logo`, `.terminal-menu`, `.terminal-prompt`
- `.btn-ghost` (theme toggle button)
- `.container`
- `.logo`

## Components to Preserve from Terminal.css
1. **Base styles**: CSS reset, box-sizing, selection
2. **Typography**: Body, headings, paragraphs, lists
3. **Links**: Base link behavior
4. **Code blocks**: pre, code styling
5. **Terminal components**: Only those listed above
6. **Tables**: Basic table styling
7. **Images**: Image sizing and centering
8. **Media queries**: Responsive behavior

## Components to Remove (Unused)
1. Forms and inputs (fieldset, input, textarea, autofill)
2. Buttons (btn-default, btn-error, btn-primary, btn-small, btn-group)
3. Progress bars
4. Cards (terminal-card)
5. Timelines (terminal-timeline)
6. Alerts (terminal-alert)
7. Media objects (terminal-media)
8. Avatars (terminal-avatarholder)
9. Placeholder (terminal-placeholder)
10. TOC styles (terminal-toc) - site uses custom toc__list

## Consolidation Strategy

### Phase 1: Analysis ✓
- [x] Identify all CSS classes used in templates
- [x] Determine which Terminal.css components are essential
- [x] List unused components

### Phase 2: Create Consolidated Stylesheet
1. Start with current console.css as base
2. Add essential Terminal.css components that aren't overridden:
   - Base resets and box model
   - List styling (ul/ol with bullets/numbers)
   - Code block styling
   - Table styling
3. Remove Terminal.css-specific overrides (no longer needed)
4. Organize into logical sections:
   - CSS Custom Properties (themes)
   - Font faces
   - Base & Reset
   - Typography
   - Links
   - Code & Pre
   - Lists
   - Tables
   - Images
   - Layout (container, terminal components)
   - Header & Navigation
   - Footer
   - Search
   - Syntax highlighting
   - Media queries

### Phase 3: Update References
1. Remove terminal-0.7.1.min.css references from:
   - _layouts/default.html (link tags)
2. Keep only console.css (and console.min.css for production)
3. Delete terminal-0.7.1.min.css file

### Phase 4: Update Documentation
1. Update CLAUDE.md:
   - Remove any terminal.css references
   - Simplify CSS workflow section (only console.css now)
   - Update minification instructions

### Phase 5: Testing
1. Build site locally with Docker
2. Verify all pages render correctly:
   - Homepage
   - Blog post pages
   - Tag pages
   - Year archives
   - About/Contact pages
3. Test theme toggle functionality
4. Verify responsive behavior (mobile/desktop)
5. Check syntax highlighting still works

### Phase 6: Minification
1. Minify new consolidated console.css
2. Update default.html to use console.min.css for production

## Expected Benefits
1. **~30-40% smaller CSS**: Remove ~300-400 lines of unused code
2. **Simpler development**: Edit one file, not worry about override order
3. **Better maintainability**: All styles in one place, logically organized
4. **Clearer codebase**: No mystery third-party framework
5. **Faster loading**: One stylesheet instead of two

## File Size Estimates
- **Before**: terminal-0.7.1.min.css (minified) + console.css (~1626 lines total)
- **After**: console.css (~1000-1100 lines estimated)
- **Reduction**: ~500-600 lines (~30-37%)

## Rollback Plan
If issues arise:
1. Git branch allows easy rollback
2. terminal-0.7.1.min.css preserved in git history
3. Can restore references in default.html

## Success Criteria
- [ ] Site builds without errors
- [ ] All pages render identically to current version
- [ ] Theme toggle works
- [ ] Mobile responsive layout intact
- [ ] Search functionality preserved
- [ ] Syntax highlighting unchanged
- [ ] CSS file size reduced by 25%+
- [ ] Only one stylesheet referenced in HTML
