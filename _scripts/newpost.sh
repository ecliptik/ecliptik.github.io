#!/bin/bash
#Script to create basics of a new jekyll post

function usage {
        echo "Usage: $(basename $0) -t -c -l " 2>&1
        echo 'Create a blog post'
        echo '   -t TITLE     Title'
        echo '   -c CATEGORY  Category'
        echo '   -l TAGS      Tags'
        echo '   -h           This help message'
        exit 1
}

# if no input argument found, exit the script with usage
if [[ ${#} -eq 0 ]]; then
   usage
fi

# Define list of arguments expected in the input
optstring=":t:c:l:"

while getopts ${optstring} arg; do
  case ${arg} in
    t)
      title="${OPTARG}"
      ;;
    c)
      category="${OPTARG}"
      ;;
    l)
      tags="${OPTARG}"
      ;;
    ?)
      echo "Invalid option: -${OPTARG}."
      echo
      usage
      ;;
  esac
done


post=$(date +%Y-%m-%d)-$(echo "${title}" | sed -e "s/ /-/g").md

echo "---
layout: post
title: ${title}
category: ${category}
tags: ${tags}
---
" > ../_posts/${post}
