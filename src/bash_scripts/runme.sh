#!/bin/bash
# @VS@ echo "runme.sh: binding for easy injection of commands in VS code. @VS@ X in any of the first 30 lines of code in a file will X with your custom keyboard shortcut!" keybindings.json instructions can found in _file.
# Add the following to your keybindings.json file in vscode.
#   {
#     "key": "ctrl+meta+g",
#     "command": "workbench.action.terminal.sendSequence",
#     "args": {
#       "text": "source $BASHER/src/bash_scripts/runme.sh ${file}\u000D"
#     }
#   }

# Ensure the script is being sourced
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    echo "This script is intended to be sourced, not executed directly."
    return 1
fi

# Get the active file path from VS Code (passed as an argument)
file_path="$1"
dir_path=$(dirname "$file_path")
file_extension="${file_path##*.}"

# Extract the command from the @VS@ directive, replace _file and _dir placeholders, and execute it
run_command=$(
    head -n 30 "$file_path" |
    grep -m 1 -E "^[ \t]*[#//]*[ \t]*@VS@" |
    sed 's/^[ \t]*[#//]*[ \t]*@VS@[ \t]*//' |
    sed "s|_file|$file_path|g" |
    sed "s|_dir|$dir_path|g"
)

# If no @VS@ command is found, set default commands based on file type
if [ -z "$run_command" ]; then
    case "$file_extension" in
        py)
            run_command="cd \"$dir_path\" && python \"$file_path\""
            ;;
        cpp)
            exe_target=$(basename "$file_path" .cpp)
            OPTS="--std=c++20"
            run_command="cd \"$dir_path\" && g++ $OPTS \"$file_path\" -o $exe_target && ./$exe_target"
            ;;
        c)
            run_command="cd \"$dir_path\" && gcc \"$file_path\" -o \"$(basename \"$file_path\" .c)\" && \"./$(basename \"$file_path\" .c)\""
            ;;
        sh)
            run_command="cd \"$dir_path\" && bash \"$file_path\""
            ;;
        *)
            echo "No @VS@ directive or default command available for file type .$file_extension."
            return 1
            ;;
    esac
fi

red='\e[31m'
green='\e[32m'
reset='\e[0m'

STARS="${red}$(printf '%.0s*' {1..80})${reset}"

# Execute the command
PREVIEW_COMMAND=0
if [[ $PREVIEW_COMMAND == 1 ]]; then
    echo -e "$STARS"
    echo -e "${green}$run_command${reset}"
    echo -e "$STARS"
fi
eval "$run_command"