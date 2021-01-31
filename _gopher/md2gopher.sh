#!/bin/bash
#Convert a jekyll markdown post to plaintext suitable for gopher,
# converted to  70 columns

# usage: ./md2gopher.sh ../_posts/post-to-convert.md

#Take input and craft output file and directory vars for use later on
input=$1
outdir="_posts"
output="${outdir}/`basename -s .md ${input}`.txt"

mkdir -p ${outdir}

echo "converting ${input} to ${output}"
pandoc --from markdown --to plain --reference-links --reference-location=block --columns=70 -o ${output}.tmp ${input}

#Use the top of the original Markdown file to create a basic header
head -6 ${input} | grep -v "layout" | grep -v "category" > ${output}
echo "" >> ${output}
cat ${output}.tmp >> ${output}
rm -fr ${output}.tmp
