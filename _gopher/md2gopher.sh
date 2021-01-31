#!/bin/bash
#Convert a jekyll markdown post to a gophermap
# Will create a sub-directory with the name of the post and a gophermap
# converted to  70 columes with links. Tries to do basic http or gopher
# linking. May not work well, but works well enough.

# usage: ./md2gophermap.sh ../_posts/post-to-convert.md

#Know Bugs
#Pandoc does not wrap code blocks to the columns length and will get cut
#off when rendered in the gophermap.
#see: https://github.com/jgm/pandoc/issues/4302#issuecomment-360669013

#Take input and craft output file and directory vars for use later on
input=$1
outdir="_posts"
output="${outdir}/`basename -s .md ${input}`.txt"

mkdir -p ${outdir}

echo "converting ${input} to ${output}"
pandoc --from markdown --to plain --reference-links --reference-location=block --columns=70 -o ${output}.tmp ${input}

#Use the top of the original Markdow file to create a basic header in
#the gophermap
head -6 ${input} | grep -v "layout" | grep -v "category" > ${output}
echo "" >> ${output}
cat ${output}.tmp >> ${output}
rm -fr ${output}.tmp
