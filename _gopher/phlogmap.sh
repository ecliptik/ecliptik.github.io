#!/bin/bash

#Create gophermap of last 10 posts
#Originally from: https://johngodlee.github.io/2019/11/20/gopher.html

#Use layout file for header on gophermap
cat _layouts/phlog > gophermap

all=(_posts/*.txt)

# Reverse order of posts array
for (( i=${#all[@]}-1; i>=0; i-- )); do
  rev_all[${#rev_all[@]}]=${all[i]}
done

# Get 10 most recent posts
recent="${rev_all[@]:0:10}"

# Add recent post links to gophermap
for i in $recent; do
  line=$(head -n 4 $i | grep -i "title:" | awk -F: {'print $2'} | xargs)
  printf "0$line\t$i\n" >> gophermap
done

#Append footer with html link
echo "" >> gophermap
printf '%.0s_' {0..69} >> gophermap
echo "" >> gophermap
echo "hecliptik.com	URL:https://www.ecliptik.com" >> gophermap
