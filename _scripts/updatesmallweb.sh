#!/bin/bash

#Converts all markdown posts under ../_posts for gopher and gemini
#Creates a gophermap and/or gmi with links to the 10 most recent posts
#Influence from: https://johngodlee.github.io/2019/11/20/gopher.html

#!/bin/bash
#Script to convert Markdown (usually Jekyll) to a small webformat of gopher or gemini

function usage {
  echo "Usage: $(basename "$0") -t -u " 2>&1
  echo "Convert a blog post to gopher, gemini, or both"
  echo "   -t TYPE     [gopher|gemini|all]"
  echo "   -h          This help message"
  exit 1
}

# if no input argument found, exit the script with usage
if [[ ${#} -eq 0 ]]; then
   usage
fi

##Variables
###Common
posts_root="../_posts"

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
  clean_file="./$(basename "${filename}")"

  #Extract date

  #Cleanup images so they're bare markdown
  sed -e "s/{:width=.*)$//g" "${filename}" | sed -e "s/\[\!/\!/g" > "${clean_file}"

  #Get title, category, tags, date
  post_title=$(grep "title:" -m1 "${clean_file}" | awk -F: '{print $2}')
  post_category=$(grep "category:" -m1 "${clean_file}" | awk -F: '{print $2}')
  post_tags=$(grep "tags:" -m1 "${clean_file}" | awk -F: '{print $2}')
  post_date=$(echo "${clean_file}" | sed -e "s%./%%g" | awk -F- '{print $1"-"$2"-"$3}')
}

#Function to convert md post to gopher plaintext and 70 columns
#Uses pandoc (>2.11.4 recommended)
markdown2gopher () {
  #Strip of .md and create a .txt file
  mkdir -p "${outdir}"
  output="${outdir}/$(basename -s .md "${filename}").txt"
  #Create temp file
  output_tmp="${output}.tmp"
  output_head="${output}.head"

  #Use pandoc to convert from markdown to plaintext
  pandoc --from markdown --to plain --reference-links --reference-location=block --columns=70 -o "${output_tmp}" "${clean_file}"

  #Use the top of the original Markdown file to create a basic header

  echo "___________________________________________" > "${output_head}"
  echo "title:${post_title}" >> "${output_head}"
  echo "tags:${post_tags}" >> "${output_head}"
  echo "date: ${post_date}" >> "${output_head}"
  echo "___________________________________________" >> "${output_head}"
  echo "" >> "${output_head}"
  cat "${output_head}" "${output_tmp}" > "${output}"

  #Cleanup temp head files
  rm -fr "${output_head}" "${output_tmp}" "${clean_file}"
}

#Function to convert md post to gemini
#Uses md2gemini: https://github.com/makeworld-the-better-one/md2gemini
markdown2gemini () {
  #Convert post using md2gemini
  mkdir -p "${outdir}"
  output="$(basename -s .md "${filename}").gmi"
  output_tmp="${output}.tmp"
  md2gemini -w -d "${outdir}" -f -l paragraph -s "${clean_file}"

  #Generate list of tags for post
  for tag in ${post_tags}; do
    tags="${tags} #${tag}"
  done

  #Build post with header and footer
  cat "${gemini_header}" > "${output_tmp}"
  echo "### ${post_date} | ${tags}" >> "${output_tmp}"
  echo "#${post_title}" >>  "${output_tmp}"

  echo "" >> "${output_tmp}"
  cat "${outdir}/${output}" >> "${output_tmp}"
  echo "" >> "${output_tmp}"
  cat "${gemini_footer}" >> "${output_tmp}"

  #Copy updated post to final location
  mv "${output_tmp}" "${outdir}/${output}"
  rm -fr "${clean_file}"
  unset tags
}

count_posts () {
  # Reverse order of posts array
  unset rev_all
  for (( i=${#smposts[@]}-1; i>=0; i-- )); do
    rev_all[${#rev_all[@]}]=${smposts[i]}
  done

  # Get 10 most recent posts
  recent_posts=("${rev_all[@]:0:10}")
}

create_gophermap () {
  #Add header to gophermap
  gophermap="${gopher_posts}/gophermap"
  cat "${gopher_header}" > "${gophermap}"
  echo "Creating gophermap: ${gophermap}"

  # Add recent post links to gophermap
  for post in "${recent_posts[@]}"; do
    title=$(head -n 4 "${post}" | grep -i "title:" | awk -F: '{print $2}' | xargs)
    link=$(echo "${post}" | awk -F/ '{print $NF}')
    printf '0%s\t./%s\n' "${title}" "${link}" >> "${gophermap}"
  done

  #Append footer with html link
  cat "${gopher_footer}" >> "${gophermap}"
}

#Function to create a list of posts from a directory stored in an array
gem_posts () {
  #Loop through posts array
  for post in "${gemposts[@]}"; do
    date=$(basename "${post}" | awk -F- '{print $1"-"$2"-"$3}')
    title=$(basename -s .gmi "${post}" | sed -e "s/${date}-\(.*\)/\1/" | sed -e "s/-/ /g")
    linktext=$(basename "${post}")
    link="${gemini_baseurl}/_posts/${linktext}"

    #Skip linking the post if it's the index
    if [[ "${title}" = "index" ]]; then
      :
    else
      #=> gemini://rawtext.club/~ecliptik/posts/2021-01-31-Making-a-Gopherhole-and-Phlog.gmi 2021-01-31-Making-a-Gopherhole-and-Phlog
      echo "=> ${link} ${date} ${title}" >> "${gemindex}"
    fi
  done
}

#Create gem index files for latest posts and archive
create_gemindex () {
  echo "Creating gemindex: ${gemindex}"

  # Create gemlog recent posts
  gemposts=(${recent_posts[@]})
  gemindex="${gemini_root}/gemlog.gmi"
  echo "Creating gemindex: ${gemindex}"
  cat "${gemini_header}" > "${gemindex}"
  echo "# Gemlog" >> "${gemindex}"
  echo "## Latest Posts" >> "${gemindex}"
  echo "" >> "${gemindex}"
  gem_posts
  echo "" >> "${gemindex}"
  echo "=> ${gemini_baseurl}/_posts/index.gmi Gemlog Archive"  >> "${gemindex}"
  echo "" >> "${gemindex}"
  cat "${gemini_footer}" >> "${gemindex}"

  # Create archive gem index
  gemposts=(${rev_all[@]})
  gemindex="${gemini_root}/_posts/index.gmi"
  echo "Creating gemindex: ${gemindex}"
  cat "${gemini_header}" > "${gemindex}"
  echo "# Gemlog Archive" >> "${gemindex}"
  echo "" >> "${gemindex}"
  gem_posts
  echo "" >> "${gemindex}"
  cat "${gemini_footer}" >> "${gemindex}"
}

# Define list of arguments expected in the input
optstring=":t:"

while getopts "${optstring}" arg; do
  case ${arg} in
    t)
      posttype="${OPTARG}"
      ;;
    ?)
      echo "Invalid option: -${OPTARG}."
      echo ""
      usage
      ;;
  esac
done

#Get all markdown posts
posts=("${posts_root}"/*.md)

case ${posttype} in
  gopher)
    outdir="${gopher_posts}"
    for filename in ${posts[*]}; do
      common
      markdown2gopher
    done
    smposts=("${gopher_posts}"/*.txt)
    count_posts
    create_gophermap
    ;;
  gemini)
    outdir="${gemini_posts}"
    for filename in ${posts[*]}; do
      common
      markdown2gemini
    done
    smposts=("${gemini_posts}"/*.gmi)
    count_posts
    create_gemindex
    ;;
  all)
    posttype="gopher"
    outdir="${gopher_posts}"
    for filename in ${posts[*]}; do
      common
      markdown2gopher
    done
    smposts=("${gopher_posts}"/*.txt)
    count_posts
    create_gophermap

    posttype="gemini"
    outdir="${gemini_posts}"
    for filename in ${posts[*]}; do
      common
      markdown2gemini
    done
    smposts=("${gemini_posts}"/*.gmi)
    count_posts
    create_gemindex
    ;;
  *)
    echo "Unsupported posttype ${posttype}!"
    echo ""
    usage
    exit 1
    ;;
esac
