#!/bin/bash
# @VS@ source _file & 

# Interval in minutes
interval=$(( 60 ))

# Change to the repository directory
cd /home/tyler/Documents/repos/Dissertation || { echo "Error: Unable to change directory."; exit 1; }

# Create progress directory if it doesn't exist
progress_dir="/tmp/progress"
mkdir -p "$progress_dir"

# Get the current hash and initialize progress file with timestamp
initial_hash=$(git rev-parse HEAD)
latest=$(find "$progress_dir" -maxdepth 1 -type f -name "*.txt" | wc -l)
latest=$((latest + 1))
progress_file="${progress_dir}/${latest}.txt"
echo "$initial_hash,$(date +%s),$(date +"%Y-%m-%d %H:%M")" > "$progress_file"

# Main loop: run nwa every interval, check for hash changes, and update progress file if needed
while true; do
  current_hash=$(git rev-parse HEAD)
  if [ "$current_hash" != "$initial_hash" ]; then
    # Hash changed: create a new progress file with the new hash as header and timestamp
    latest=$(find "$progress_dir" -maxdepth 1 -type f -name "*.txt" | wc -l)
    latest=$((latest + 1))
    progress_file="${progress_dir}/${latest}.txt"
    initial_hash="$current_hash"
    echo "HASH: $initial_hash, $(date)" > "$progress_file"
  fi

#   echo "----- $(date) -----, $(date)" >> "$progress_file"
  nw 2>&1 | while IFS= read -r line; do
    echo "$line,$(date +%s),$(date +"%Y-%m-%d %H:%M")"
  done >> "$progress_file"
  
  sleep $interval
done
