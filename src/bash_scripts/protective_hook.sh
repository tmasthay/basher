#!/bin/bash

# Array of protected branches
protected_branches=("main" "master" "release" "production" "julia_interface_bug")

# Array of allowed branches
allowed_branches=("develop" "feature" "bugfix")

# Get the name of the branch being pushed to
current_branch=$(git rev-parse --abbrev-ref HEAD)

# Function to check if a branch is in a list
is_in_list() {
  local branch=$1
  shift
  local list=("$@")
  for item in "${list[@]}"; do
    if [ "$branch" = "$item" ]; then
      return 0
    fi
  done
  return 1
}

# Check if the current branch is in the array of protected branches
if is_in_list "$current_branch" "${protected_branches[@]}"; then
  echo "Error: You are trying to push to a protected branch: $current_branch"
  exit 1
fi

# Check if the current branch is in the array of allowed branches
if ! is_in_list "$current_branch" "${allowed_branches[@]}"; then
  echo "Error: You are trying to push to a branch that is not allowed: $current_branch"
  exit 1
fi

# Allow the push if the branch is not protected and is allowed
exit 0