# Deprecated Scripts

These scripts have been replaced by `manage.py` for better maintainability, consistency, and feature completeness.

## Why Deprecated

**newpost.sh**
- Missing `description` field (required for SEO and social media)
- No support for year-based directories (`_posts/YYYY/`)
- Missing `redirect_from` field for backward compatibility
- Hardcoded relative path (`../_posts/`) requiring execution from `_scripts/`

**tag_generator.py**
- Integrated into `manage.py tags` command
- Same functionality with better error handling and reporting

**updatesmallweb.sh**
- Complex 338-line bash script
- Will be ported to Python in future `manage.py gopher/gemini` commands
- Continue using this script until Python replacement is ready

**markdown2sw.sh**
- Single-file conversion for gopher/gemini
- Will be replaced by future `manage.py gopher/gemini` commands
- Code duplication with updatesmallweb.sh

**md2gophermap.sh**
- Old gophermap creator
- Known bugs (code blocks not wrapping properly)
- Will be replaced by future `manage.py gopher` command

## Can I Still Use Them?

Yes, but not recommended for new work:

- **newpost.sh** → Use `python3 _scripts/manage.py post` instead
- **tag_generator.py** → Use `python3 _scripts/manage.py tags` instead
- **updatesmallweb.sh** → Continue using until `manage.py gopher/gemini` are implemented
- **markdown2sw.sh** → Use updatesmallweb.sh or wait for `manage.py` implementation
- **md2gophermap.sh** → Use updatesmallweb.sh instead

## Migration Guide

### Old newpost.sh
```bash
# Old way (deprecated)
cd _scripts
./newpost.sh -t "Post Title" -c linux -l "tag1 tag2"
```

### New manage.py
```bash
# New way (from repo root)
python3 _scripts/manage.py post -t "Post Title" -c linux -d "Description here" --tags tag1 tag2

# Or use interactive mode
python3 _scripts/manage.py post
```

### Old tag_generator.py
```bash
# Old way
python3 _scripts/tag_generator.py
```

### New manage.py
```bash
# New way
python3 _scripts/manage.py tags

# Or update everything
python3 _scripts/manage.py all
```

## Timeline

- **2026-01-19**: Scripts moved to deprecated/
- **Future**: updatesmallweb.sh and markdown2sw.sh will be ported to Python
- **Future**: These scripts may be removed after manage.py is fully stable

## Support

If you need to use these scripts and encounter issues:

1. Consider switching to `manage.py` instead
2. Check the main `_scripts/README.md` for current documentation
3. Report issues if `manage.py` is missing functionality you need
