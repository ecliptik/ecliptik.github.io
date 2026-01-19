#!/bin/bash
#Script to convert Markdown (usually Jekyll) to a small webformat of gopher or gemini

function usage {
  echo "Usage: $(basename "$0") -t -f" 2>&1
  echo "Convert a blog post to gopher, gemini, or both"
  echo "   -t TYPE     [gopher|gemini|all]"
  echo "   -f FILE     file to convert"
  echo "   -h          This help message"
  exit 1
}

# if no input argument found, exit the script with usage
if [[ ${#} -eq 0 ]]; then
   usage
fi

##Variables
###Gopher
gopher_root="../_gopher"
gopher_posts="${gopher_root}/_posts"
gopher_layouts="${gopher_root}/_layouts"
gopher_header="${gopher_layouts}/phlog_header"
gopher_footer="${gopher_layouts}/phlog_footer"

###Gemini
gemini_baseurl="gemini://rawtext.club/~ecliptik"
gemini_root="../_gemini"
gemini_posts="${gemini_root}/_posts"
gemini_layouts="${gemini_root}/_layouts"
gemini_header="${gemini_layouts}/gem_header"
gemini_footer="${gemini_layouts}/gem_footer"

#Function to cleanup file before conversion; stripping html, fixing elements, etc
common () {
  echo "Converting post ${filename} to ${posttype}"
  echo "Cleaning file: ${filename}"
  clean_file="./$(basename "${filename}")"
  #clean_file="./$(basename \"${filename}\")"

  #Cleanup images so they're bare markdown
  sed -e "s/{:width=.*)$//g" "${filename}" | sed -e "s/\[\!/\!/g" > "${clean_file}"

   #Make outdir if it doesn't exist
  if [ ! -d "${outdir}" ]; then
    mkdir -p "${outdir}"
  fi
}

#Function to convert md post to gopher  plaintext and 70 columns
#Uses pandoc (>2.11.4 recommended)
markdown2gopher () {

  #Strip of .md and create a .txt file
  output="${outdir}/$(basename -s .md "${filename}").txt"
  #Create temp file
  output_tmp="${output}.tmp"
  output_head="${output}.head"

  #Use pandoc to convert from markdown to plaintext
  pandoc --from markdown --to plain --reference-links --reference-location=block --columns=70 -o "${output_tmp}" "${clean_file}"

  #Use the top of the original Markdown file to create a basic header
  head -6 "${filename}" | grep -v "layout" | grep -v "category" > "${output_head}"
  echo "" >> "${output_head}"
  cat "${output_head}" "${output_tmp}" >> "${output}"

  #Cleanup temp head files
  rm -fr "${output_head}" "${output_tmp}"
}

#Function to convert md post to gemini
#Uses md2gemini: https://github.com/makeworld-the-better-one/md2gemini
markdown2gemini () {
  #Convert post using md2gemini
  md2gemini -w -d "${outdir}" -f -l paragraph -s -b "${gemini_baseurl}" "./${clean_file}"
}

# Define list of arguments expected in the input
optstring=":t:f:"

while getopts "${optstring}" arg; do
  case ${arg} in
    t)
      posttype="${OPTARG}"
      ;;
    f)
      filename="${OPTARG}"
      ;;
    ?)
      echo "Invalid option: -${OPTARG}."
      echo ""
      usage
      ;;
  esac
done

if [ -z "${filename}" ]; then
  echo "Required argument filename is missing"
  echo ""
  usage
  exit 1
fi

#Check that the file to convert exists
if [ ! -f "${filename}" ]; then
  echo "File: ${filename} doesn't exist!"
  echo ""
  usage
  exit 1
fi

case ${posttype} in
  gopher)
    outdir="${gopher_posts}"
    common
    markdown2gopher
    ;;
  gemini)
    outdir="${gemini_posts}"
    common
    markdown2gemini
    ;;
  all)
    posttype="gopher"
    outdir="${gopher_posts}"
    common
    markdown2gopher

    posttype="gemini"
    outdir="${gemini_posts}"
    common
    markdown2gemini
    ;;
  *)

    echo "Unsupported posttype ${posttype}!"
    echo ""
    usage

    exit 1
    ;;
esac

#Cleanup temp clean file
if [ -f "./${clean_file}" ]; then
  rm -fr "${clean_file}"
fi
