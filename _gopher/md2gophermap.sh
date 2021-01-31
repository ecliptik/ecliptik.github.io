#!/bin/bash
#Convert a jekyll markdown post to a gophermap
#Will create a sub-directory with the name of the post and a gophermap
#converted to  70 columns with links. Tries to do basic http or gopher
#linking. May not work well, but works well enough.

# usage: ./md2gophermap.sh ../_posts/post-to-convert.md

#Know Bugs
#Pandoc does not wrap code blocks to the columns length and will get cut
#off when rendered in the gophermap.
#see: https://github.com/jgm/pandoc/issues/4302#issuecomment-360669013

#Take input and craft output file and directory vars for use later on
input=$1
output=`basename ${input}`
outdir=`basename -s .md ${output}`

echo "converting ${input}"
pandoc --from markdown --to markdown --reference-links --reference-location=block --columns=70 -o ${output} ${input}

#Do some IFS changes in order to properly parse individual lines after conversion
IFSORIG=${IFS}
IFS="
"

#Create gophermap

##HTML link syntax
#hecliptik.com	URL:https://www.ecliptik.com

##Gopher link syntax
#1rawtext.club	/	rawtext.club	70

#Go through the file line-by-line looking for http or gopher linkes and convert
for line in `cat ${output}`; do
  IFS=${IFSORIG}
  if echo "${line}" | egrep -e "^.+\[.+\]:.+" >/dev/null; then

    case ${line} in
      *http*)
        itemname=`echo ${line} |sed -r 's/\[(.*)\]/\1/' | awk -F: {'print $1'} |xargs`
        itemlink=`echo ${line} |awk -F] {'print $2'} | sed -e "s%:\ %%"`
        item="h${itemname}\tURL:${itemlink}"
      ;;
      *gopher*)
        itemname=`echo ${line} |sed -r 's/\[(.*)\]/\1/' | awk -F: {'print $1'} |xargs`
        itemserver=`echo ${line} |awk -F/ {'print $3'} | awk -F: {'print $1'}`
        itemlink=`echo ${line} |awk -F/ {'print $4'}`
        item="1${itemname}\t/${itemlink}\t${itemserver}\t70"
    esac
#Set IFS to new line in order to remove leading spaces
 IFS="
"

    #Escape all special chars so they're replaced in sed
    linemung=$(echo ${line} | sed -e 's`[][\\/.*^$]`\\&`g')
    itemmung=$(echo ${item} | sed -e 's`[][\\/.*^$]`\\&`g')

    #Replace markdown blocks with gophermap
    sed -i -e "s/${linemung}/${itemmung}/" ${output}
    sed -i -e "s/\\\t/\t/g" ${output}
 fi
done

#Make the subdirectory
mkdir -p ${outdir}

#Use the top of the original Markdown file to create a basic header
head -6 ${input} | grep -v "layout" | grep -v "category" > ${outdir}/gophermap
echo "" >> ${outdir}/gophermap
cat ${output} >> ${outdir}/gophermap

#Convert --- lines to underscore
sed -i -E "s/^--.+$/$(printf '%.0s_' {0..69})/g" ${outdir}/gophermap
sed -i -E "s/^==.+$/$(printf '%.0s_' {0..69})/g" ${outdir}/gophermap

#Remove the pandoc output file to clean up
rm -fr ${output}
