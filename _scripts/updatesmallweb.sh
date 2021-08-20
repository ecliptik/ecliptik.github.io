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
gemini_tags="${gemini_root}/_tags"
gemini_layouts="${gemini_root}/_layouts"
gemini_header="${gemini_layouts}/gem_header"
gemini_footer="${gemini_layouts}/gem_footer"

#Re-genrate tag pages every run
if [ -d "${gemini_tags}" ]; then
  rm -fr "${gemini_tags}"
  mkdir -p "${gemini_tags}"
fi

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
  cumulative_tags="${alltags} ${post_tags}"
  alltags=$(echo "${cumulative_tags}" | sort -u)
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
  cat "${output_head}" "${output_tmp}" | grep -v '"fig:"'> "${output}"

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
  md2gemini -w -d "${outdir}" -b ${gemini_baseurl} -f -l paragraph -s "${clean_file}"

  #Build post with header and footer
  cat "${gemini_header}" > "${output_tmp}"
  echo "#${post_title}" >>  "${output_tmp}"
  echo "### ${post_date} | %TAGS%" >> "${output_tmp}"

  echo "" >> "${output_tmp}"
  cat "${outdir}/${output}" >> "${output_tmp}"
  echo "" >> "${output_tmp}"
  echo "" >> "${output_tmp}"
  echo "### Tags" >> "${output_tmp}"
  echo "" >> "${output_tmp}"

  #Generate list of tag pages for post
  for tag in ${post_tags}; do
    tags="#${tag} ${tags}"
    post_tag_page="${gemini_tags}/${tag}.gmi"
    #Create tag page if new, otherwise append to it
    if [ ! -f ${post_tag_page} ]; then
      echo "Creating tag page ${post_tag_page}"
      cat "${gemini_header}" > "${post_tag_page}"
      echo "# ${tag}" >> "${post_tag_page}"
      echo "" >> "${post_tag_page}"
    fi
    #Add page to tag page, skip if it's already been added
    if grep "${post_title}" "${post_tag_page}" >/dev/null; then
      :
    else
      echo "=> ${gemini_baseurl}/_posts/${output} ${post_title}" >> "${post_tag_page}"
    fi
    #Add tag link to bottom of gemlog post
    echo "=> ${gemini_baseurl}/_tags/${tag}.gmi ${tag}" >> "${output_tmp}"
  done

  cat "${gemini_footer}" >> "${output_tmp}"
  #Replace %TAGS% token with accumulated tags
  sed -i -e "s/%TAGS%/${tags}/g" "${output_tmp}"

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
    title=$(head -n 10 "${post}" | grep -i "title:" | awk -F: '{print $2}' | xargs)
    link=$(echo "${post}" | awk -F/ '{print $NF}')
    printf '0%s\t./%s\n' "${title}" "${link}" >> "${gophermap}"
  done

  #Append footer with html link
  cat "${gopher_footer}" >> "${gophermap}"
}

#Function to create a list of posts from a directory stored in an array
#used for archive page to inclue all posts
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
  # Create gemlog recent posts
  gemposts=(${recent_posts[@]})
  gemindex="${gemini_root}/gemlog.gmi"
  echo "Creating gemlog index: ${gemindex}"
  cat "${gemini_header}" > "${gemindex}"
  echo "# Ecliptik's Gemlog" >> "${gemindex}"
  echo "## Latest Posts" >> "${gemindex}"
  echo "" >> "${gemindex}"
  gem_posts
  echo "" >> "${gemindex}"
  echo "=> ${gemini_baseurl}/_posts/index.gmi Gemlog Archive"  >> "${gemindex}"
  echo "=> ${gemini_baseurl}/_tags/index.gmi Gemlog Tags"  >> "${gemindex}"
  echo "=> ${gemini_baseurl}/_posts/feed.xml Gemfeed" >> "${gemindex}"
  echo "" >> "${gemindex}"
  cat "${gemini_footer}" >> "${gemindex}"

  # Create archive gem index
  gemposts=(${rev_all[@]})
  gemindex="${gemini_root}/_posts/index.gmi"
  gem_tag_index="${gemini_root}/_tags/index.gmi"
  echo "Creating archive index: ${gemindex}"
  cat "${gemini_header}" > "${gemindex}"
  echo "" >> "${gemindex}"
  echo "# Ecliptik's Gemlog Archive" >> "${gemindex}"
  echo "" >> "${gemindex}"
  echo "## Tags" >> "${gemindex}"
  echo "" >> "${gemindex}"
  echo "=> ${gemini_baseurl}/_tags/index.gmi Gemlog Tags"  >> "${gemindex}"
  echo "" >> "${gemindex}"
  echo "## Posts" >> "${gemindex}"
  echo "" >> "${gemindex}"
  gem_posts
  echo "" >> "${gemindex}"
  cat "${gemini_footer}" >> "${gemindex}"
}

create_gemfeed () {
  author="ecliptik"
  feed_title="Ecliptik's Gemlog"
  email="gemini@accounts.ecliptik.com"
  feedout="feed.xml"

  #Run gemfeed to generate a feed file
  #Requires https://tildegit.org/solderpunk/gemfeed
  gemfeed -a ${author} -b ${gemini_baseurl}/_posts/ -d ${gemini_posts} -e ${email} -t "${feed_title}" -o ${feedout}
}

create_tagindex () {
  tag_index="${gemini_tags}/index.gmi"
  echo "Creating tag index page: ${tag_index}"
  cat "${gemini_header}" > "${tag_index}"
  echo "# Tags" >> "${tag_index}"
  echo "" >> "${tag_index}"
  tagpages=(${gemini_tags}/*.gmi)
  for tagpage in "${tagpages[@]}" ; do
    #Skip adding the index.gmi since it's not a tag
    if [[ "${tagpage}" = "index.gmi" ]]; then
      :
    else
      tag_title="$(basename ${gemini_tags}/${tagpage} .gmi)"
      link="${gemini_baseurl}/_tags/$(basename ${tagpage})"
      echo "Adding tag link ${link}"
      tag_title="$(basename ${gemini_tags}/${tagpage} .gmi)"
      echo "=> ${link} ${tag_title}" >> "${tag_index}"
    fi
  done
  cat "${gemini_footer}" >> "${tag_index}"
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
    create_tagindex
    create_gemfeed
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
    create_tagindex
    create_gemfeed
    ;;
  *)
    echo "Unsupported posttype ${posttype}!"
    echo ""
    usage
    exit 1
    ;;
esac
