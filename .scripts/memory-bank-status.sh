#!/bin/bash
# Memory Bank status script para Linux
echo "Status do Memory Bank (Linux):"
for file in memory-bank/*.md; do
  echo -e "\033[1;33m$(basename "$file"):\033[0m"
  head -n 3 "$file"
  echo

done
exit 0
