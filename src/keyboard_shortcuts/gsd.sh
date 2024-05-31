#!/bin/bash

gsd() {
    date --rfc-3339='date' | awk -F'-' '{print $2,$3,$1}' | sed 's/ /\//g' | xclip -selection clipboard
}

gsd
