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
